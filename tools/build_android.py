#!/usr/bin/env python3
"""Build the Android apps: android/NAME.apk for every app in
tools/build_calc_files.py (and android/web/NAME.html, the same app as one
web page).

    python3 tools/build_android.py            # all apps
    python3 tools/build_android.py CIRCUITS   # one app

Each app is the calculator program itself (hp-prime/NAME.txt), translated
to JavaScript by tools/ppl2js.py and run by tools/android/runtime.js in a
full-screen WebView, with the calculator's keys on screen below it.  The
translation is checked against the simulator by tools/test_android.py.

Needs the Android SDK (platform 34 and build-tools 34.0.0) in
$ANDROID_HOME (default /opt/android-sdk), a JDK and Node.  It does not use
Gradle: aapt2 packs the resources, javac and d8 compile the one Java class,
and apksigner signs with tools/android/apps.keystore, which is kept out of
the repository (the script makes one if it is missing).  Android installs
an update over an app only when both have the same key.
"""
import base64
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_calc_files import APPS  # noqa: E402
from ppl2js import translate  # noqa: E402
from ppl_sim import FONT_FILE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "tools", "android")
OUT = os.path.join(ROOT, "android")
SDK = os.environ.get("ANDROID_HOME", "/opt/android-sdk")
BT = os.path.join(SDK, "build-tools", "34.0.0")
JAR = os.path.join(SDK, "platforms", "android-34", "android.jar")
KEYSTORE = os.path.join(HERE, "apps.keystore")
KEYPASS = os.environ.get("APPS_KEYPASS", "hpprime-apps")
VERSION_CODE = 1          # raise for every release that changes an app
VERSION_NAME = "1.0"
ICON_SIZES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{pkg}">
  <application android:label="{label}" android:icon="@mipmap/ic_launcher"
      android:allowBackup="true" android:theme="@android:style/Theme.Material.NoActionBar">
    <activity android:name=".MainActivity" android:exported="true"
        android:configChanges="orientation|screenSize|screenLayout|smallestScreenSize|keyboard|keyboardHidden|uiMode|density"
        android:windowSoftInputMode="adjustResize">
      <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
      </intent-filter>
    </activity>
  </application>
</manifest>
"""

ACTIVITY = """package {pkg};

import android.app.Activity;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

// A full-screen WebView running the app page in assets/index.html.  (No
// inner classes: this d8 cannot read the ones javac 21 writes.)
public class MainActivity extends Activity implements Runnable {{
    private WebView web;

    @Override
    protected void onCreate(Bundle state) {{
        super.onCreate(state);
        getWindow().setStatusBarColor(0xFF12141C);
        getWindow().setNavigationBarColor(0xFF12141C);
        web = new WebView(this);
        web.setBackgroundColor(0xFF12141C);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setTextZoom(100);
        web.addJavascriptInterface(new Bridge(this), "Android");
        web.setWebViewClient(new WebViewClient());
        setContentView(web);
        web.loadUrl("file:///android_asset/index.html");
    }}

    // the app's EXIT closes the activity (run on the UI thread by Bridge)
    public void run() {{
        finish();
    }}

    // Back closes a dialog, or acts as the calculator's Esc key
    @Override
    public void onBackPressed() {{
        web.evaluateJavascript("window.pplBack && window.pplBack()", null);
    }}

    @Override
    protected void onDestroy() {{
        if (web != null) web.destroy();
        super.onDestroy();
    }}
}}

class Bridge {{
    private final MainActivity act;

    Bridge(MainActivity act) {{
        this.act = act;
    }}

    @JavascriptInterface
    public void exit() {{
        act.runOnUiThread(act);
    }}
}}
"""


def run(*cmd, **kw):
    p = subprocess.run(list(cmd), capture_output=True, text=True, **kw)
    if p.returncode != 0:
        raise RuntimeError(" ".join(cmd[:2]) + " failed:\n" + p.stdout[-3000:] + p.stderr[-3000:])
    return p.stdout


def page(name):
    """the app as one self-contained HTML page"""
    src = open(os.path.join(ROOT, "hp-prime", name + ".txt"), encoding="utf-8").read()
    program = translate(src).replace("</", "<\\/")
    runtime = open(os.path.join(HERE, "runtime.js"), encoding="utf-8").read()
    font = base64.b64encode(open(FONT_FILE, "rb").read()).decode()
    html = open(os.path.join(HERE, "shell.html"), encoding="utf-8").read()
    parts = {"{{TITLE}}": name, "{{FONT}}": font, "{{RUNTIME}}": runtime, "{{PROGRAM}}": program}
    out, pos = [], 0
    while True:
        k = html.find("{{", pos)
        if k < 0:
            break
        end = html.index("}}", k) + 2
        out += [html[pos:k], parts[html[k:end]]]
        pos = end
    return "".join(out + [html[pos:]])


def keystore():
    if not os.path.exists(KEYSTORE):
        run("keytool", "-genkeypair", "-keystore", KEYSTORE, "-alias", "apps", "-keyalg", "RSA",
            "-keysize", "2048", "-validity", "36500", "-storepass", KEYPASS, "-keypass", KEYPASS,
            "-dname", "CN=HP Prime class apps, O=Subheat-subcool-app")


def build(app):
    name = app["name"]
    pkg = "io.github.christophercasteel2." + name.lower()
    html = page(name)
    os.makedirs(os.path.join(OUT, "web"), exist_ok=True)
    with open(os.path.join(OUT, "web", name + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    with tempfile.TemporaryDirectory() as tmp:
        J = lambda *p: os.path.join(tmp, *p)  # noqa: E731
        os.makedirs(J("assets"))
        with open(J("assets", "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        for dens, px in ICON_SIZES.items():
            os.makedirs(J("res", "mipmap-" + dens))
            app["icon"](J("res", "mipmap-" + dens, "ic_launcher.png"), px)
        with open(J("AndroidManifest.xml"), "w") as f:
            f.write(MANIFEST.format(pkg=pkg, label=name))
        src_dir = J("src", *pkg.split("."))
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "MainActivity.java"), "w") as f:
            f.write(ACTIVITY.format(pkg=pkg))
        run(os.path.join(BT, "aapt2"), "compile", "--dir", J("res"), "-o", J("res.zip"))
        run(os.path.join(BT, "aapt2"), "link", "-o", J("base.apk"), "-I", JAR,
            "--manifest", J("AndroidManifest.xml"), "-A", J("assets"), J("res.zip"),
            "--min-sdk-version", "21", "--target-sdk-version", "34",
            "--version-code", str(VERSION_CODE), "--version-name", VERSION_NAME)
        os.makedirs(J("classes"))
        run("javac", "-nowarn", "-Xlint:-options", "-source", "8", "-target", "8",
            "-bootclasspath", JAR, "-d", J("classes"), os.path.join(src_dir, "MainActivity.java"))
        classes = [os.path.join(d, f) for d, _, fs in os.walk(J("classes")) for f in fs]
        os.makedirs(J("dex"))
        run(os.path.join(BT, "d8"), "--min-api", "21", "--lib", JAR, "--output", J("dex"), *classes)
        with zipfile.ZipFile(J("base.apk"), "a", zipfile.ZIP_DEFLATED) as z:
            z.write(J("dex", "classes.dex"), "classes.dex")
        run(os.path.join(BT, "zipalign"), "-p", "-f", "4", J("base.apk"), J("aligned.apk"))
        apk = os.path.join(OUT, name + ".apk")
        run(os.path.join(BT, "apksigner"), "sign", "--ks", KEYSTORE, "--ks-pass", "pass:" + KEYPASS,
            "--key-pass", "pass:" + KEYPASS, "--out", apk, J("aligned.apk"))
        run(os.path.join(BT, "apksigner"), "verify", apk)
        idfile = apk + ".idsig"
        if os.path.exists(idfile):
            os.remove(idfile)
    print(f"{name + '.apk':14} {os.path.getsize(apk):8} bytes  ({pkg})")


def main():
    names = sys.argv[1:]
    if not shutil.which("node"):
        sys.exit("needs Node (to check the translated programs)")
    keystore()
    os.makedirs(OUT, exist_ok=True)
    for app in APPS:
        if not names or app["name"] in names:
            build(app)
    print(f"written to {OUT}")


if __name__ == "__main__":
    main()

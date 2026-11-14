"""contact sheets of the PDF pages, for checking the layout: python3 sheet.py first last"""
import subprocess, sys, glob, os
from PIL import Image
a, b = int(sys.argv[1]), int(sys.argv[2])
res = int(sys.argv[3]) if len(sys.argv) > 3 else 60
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "out")
for f in glob.glob(os.path.join(out, "s-*.png")): os.remove(f)
subprocess.run(["pdftoppm", "-r", str(res), "-f", str(a), "-l", str(b), "-png", os.path.join(here, "Applied_Technical_Math.pdf"), os.path.join(out, "s")], stderr=subprocess.DEVNULL)
fs = sorted(glob.glob(os.path.join(out, "s-*.png")))
ims = [Image.open(f) for f in fs]
w, h = ims[0].size
cols = min(4, len(ims)); rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (cols * (w + 6), rows * (h + 6)), "#888")
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * (w + 6), (i // cols) * (h + 6)))
sh.save(os.path.join(out, "sheet.png")); print(sh.size)

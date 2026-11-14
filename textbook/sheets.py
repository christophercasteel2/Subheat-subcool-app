"""every page of the PDF as contact sheets of 8, for proofreading: out/all_NN.png"""
import subprocess, glob, os
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "out")
for f in glob.glob(os.path.join(out, "a-*.png")) + glob.glob(os.path.join(out, "all_*.png")): os.remove(f)
subprocess.run(["pdftoppm", "-r", "75", "-png", os.path.join(here, "Applied_Technical_Math.pdf"), os.path.join(out, "a")], stderr=subprocess.DEVNULL)
fs = sorted(glob.glob(os.path.join(out, "a-*.png")))
for k in range(0, len(fs), 8):
    ims = [Image.open(f) for f in fs[k:k + 8]]
    w, h = ims[0].size
    sh = Image.new("RGB", (4 * (w + 6), 2 * (h + 6)), "#888")
    for i, im in enumerate(ims): sh.paste(im, ((i % 4) * (w + 6), (i // 4) * (h + 6)))
    sh.save(os.path.join(out, f"all_{k // 8 + 1:02d}.png"))
print(len(fs), "pages")

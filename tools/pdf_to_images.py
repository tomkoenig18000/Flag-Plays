#!/usr/bin/env python3
"""One-off: render the playbook PDF (one play per page, page N = play N) to docs/plays/NN.webp (+ 480px docs/thumbs/ for the grid).

usage: python3 tools/pdf_to_images.py path/to/Flag_Football_Plays.pdf
needs poppler's pdftoppm + Pillow. The PDF itself is git-ignored.
"""
import subprocess, sys, tempfile, pathlib
from PIL import Image
pdf = sys.argv[1]
out = pathlib.Path(__file__).parent.parent / 'docs' / 'plays'; out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as t:
    subprocess.run(['pdftoppm', '-r', '150', '-png', pdf, f'{t}/p'], check=True, stderr=subprocess.DEVNULL)
    for f in sorted(pathlib.Path(t).glob('p-*.png')):
        n = int(f.stem.split('-')[1])
        Image.open(f).convert('RGB').save(out / f'{n:02d}.webp', 'WEBP', quality=72, method=6)
        im = Image.open(out / f'{n:02d}.webp'); th = out.parent / 'thumbs'; th.mkdir(exist_ok=True)
        im.resize((480, round(im.height * 480 / im.width)), Image.LANCZOS).save(th / f'{n:02d}.webp', 'WEBP', quality=70, method=6)
        print('play', n)

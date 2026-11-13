"""Kontrol kareleri tek gorselde: python sheet.py <out.jpg> <sutun> <kare_genisligi> dosyalar..."""
import sys, skia
out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); files = sys.argv[4:]
imgs = [skia.Image.open(f) for f in files]
th = int(tw * imgs[0].height() / imgs[0].width()); rows = (len(imgs) + cols - 1) // cols
surf = skia.Surface(cols * tw, rows * th); cv = surf.getCanvas(); cv.clear(skia.ColorBLACK)
for i, im in enumerate(imgs):
    cv.drawImageRect(im, skia.Rect.MakeXYWH((i % cols) * tw, (i // cols) * th, tw, th), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
surf.makeImageSnapshot().save(out, skia.kJPEG, 88)

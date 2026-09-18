#!/usr/bin/env python3
"""
Social share image for O'Connell Automotive.

    python3 make-og.py

Writes images/og.jpg at 1200x630, the size Facebook, Messenger, iMessage, X and
LinkedIn all crop from.

This matters more than usual here. His growth plan is Facebook community groups,
Marketplace and people texting the link to a neighbor. A link with no preview
image is a gray box, and a gray box does not get tapped.

Design rules for a card that is often seen at 300px wide in a feed:
  - phone number large enough to read without opening the link
  - four short lines maximum
  - one accent color, high contrast
"""
import os, subprocess

HERE   = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BRAND  = "O'Connell Automotive"
PHONE  = "(779) 396-4746"
CITY   = "Kankakee, IL"

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face{{font-family:x}}
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{width:1200px;height:630px;background:#16130F;color:#F1ECE4;overflow:hidden;
    font-family:-apple-system,"Helvetica Neue",Helvetica,Arial,sans-serif;position:relative}}
  .bar{{position:absolute;left:0;top:0;bottom:0;width:18px;background:#E8622A}}
  .inner{{padding:78px 80px 0 118px;height:100%;display:flex;flex-direction:column}}
  .eyebrow{{font-size:25px;font-weight:700;letter-spacing:.20em;text-transform:uppercase;
    color:#D8A23A;margin-bottom:28px}}
  h1{{font-size:104px;line-height:.96;font-weight:800;text-transform:uppercase;
    letter-spacing:-.025em;margin-bottom:26px}}
  h1 .o{{color:#E8622A}}
  .sub{{font-size:35px;color:#A2978A;line-height:1.35;max-width:820px}}
  .foot{{margin-top:auto;padding-bottom:64px;display:flex;align-items:center;gap:26px}}
  .phone{{background:#E8622A;color:#160D06;font-size:46px;font-weight:800;
    padding:18px 34px;border-radius:10px;letter-spacing:-.01em}}
  .tag{{font-size:26px;color:#A2978A;font-weight:600}}
  .mark{{position:absolute;right:76px;top:68px;width:190px;opacity:.97}}
</style></head><body>
  <div class="bar"></div>
  <img class="mark" src="brand/logo-badge.svg">
  <div class="inner">
    <div class="eyebrow">Auto Repair &#183; {CITY}</div>
    <h1>I fix cars<br>in <span class="o">Kankakee</span>.</h1>
    <div class="sub">One mechanic. Brakes, batteries, radiators,<br>check engine lights.</div>
    <div class="foot">
      <div class="phone">{PHONE}</div>
      <div class="tag">Call or text &#183; evenings and weekends</div>
    </div>
  </div>
</body></html>"""

if __name__ == "__main__":
    # the badge lives in site/brand/, copy it next to the temp html so the relative src resolves
    src_badge = os.path.join(HERE, "..", "brand", "logo-badge.svg")
    dst_badge = os.path.join(HERE, "brand", "logo-badge.svg")
    if os.path.exists(src_badge) and not os.path.exists(dst_badge):
        open(dst_badge, "w", encoding="utf-8").write(open(src_badge, encoding="utf-8").read())

    tmp = os.path.join(HERE, "_og.html")
    open(tmp, "w", encoding="utf-8").write(HTML)
    png = os.path.join(HERE, "images", "_og.png")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    f"--screenshot={png}", "--window-size=1200,630", f"file://{tmp}"],
                   check=True, capture_output=True)
    os.remove(tmp)

    # JPEG keeps it under the size where chat apps refuse to fetch a preview
    from PIL import Image
    im = Image.open(png).convert("RGB")
    out = os.path.join(HERE, "images", "og.jpg")
    im.save(out, quality=88, optimize=True)
    os.remove(png)
    print(f"  images/og.jpg  {im.size[0]}x{im.size[1]}  {os.path.getsize(out)//1024} KB")

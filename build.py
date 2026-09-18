#!/usr/bin/env python3
"""
O'Connell Automotive static site generator.

    python3 build.py

VOICE NOTE. Joe writes in short, flat sentences with no decoration and no adjectives
doing work that facts should do. First person, never "we". No superlatives. The copy
below is written to sound like him, not like an agency. If you edit it and it starts
sounding polished, it is wrong. Full voice guide in the agency brand doc.

SEO sits underneath the voice, never on top of it: geography in the title, H1 and
H2s, one heading per service, a served-areas block, and LocalBusiness JSON-LD.

REPLACE: markers are decisions Joe has not made. deploy-site.sh refuses to publish
if placeholders remain AND noindex has been removed.
"""
import json, os

BRAND       = "O'Connell Automotive"          # REPLACE: confirm, see brand/BRANDING-AND-NAMES.md
PHONE_HUMAN = "(779) 396-4746"
PHONE_E164  = "+17793964746"
CITY        = "Kankakee"
STATE       = "IL"
SITE        = "REPLACE: https://oconnellautomotive.com"
NOINDEX     = True
ASSET_V     = "2"

TOWNS = ["Kankakee", "Bourbonnais", "Bradley", "Manteno", "Momence", "Herscher",
         "Grant Park", "St. Anne", "Chebanse", "Aroma Park", "Limestone", "Peotone"]

# What a mechanic with his own tools can genuinely take on. Each gets its own
# heading, which is how a service page earns rankings without keyword stuffing.
SERVICES = [
    ("Brake repair", "brakes",
     "Pads, rotors, calipers, hoses and lines. Grinding, squealing, a soft pedal or a shudder "
     "when you stop. Most common job there is and the one people ride out too long."),
    ("Oil changes and fluids", "oil",
     "Oil and filter, transmission fluid, coolant, differentials, power steering. "
     "Cheap to do on time. Expensive not to."),
    ("Batteries, alternators and starters", "battery",
     "Clicks and will not turn over, dash lights flickering, dead every morning. I test the "
     "whole charging system instead of just selling you a battery."),
    ("Radiators and cooling", "cooling",
     "Radiators, water pumps, thermostats, hoses, heater cores. If the temp gauge is climbing, "
     "stop driving it and call me. Overheating turns a small bill into an engine."),
    ("Check engine light and diagnostics", "diag",
     "I scan it and then tell you what it actually means. A code points at a system, not a "
     "part, and plenty of places will sell you the part."),
    ("Suspension and steering", "suspension",
     "Struts, shocks, control arms, ball joints, tie rods, sway bar links, wheel bearings. "
     "Clunking over bumps, wandering on the highway, a hum that changes when you turn."),
    ("Belts, hoses and leaks", "belts",
     "Serpentine belts, tensioners, idlers, pulleys. Squeal on a cold start, or a puddle under "
     "the car you want identified before it gets worse."),
    ("Tune ups and ignition", "tuneup",
     "Spark plugs, coils, wires, filters. Misfire, rough idle, no power on a hill, gas mileage "
     "falling off a cliff."),
    ("Sensors and electrical", "electrical",
     "Oxygen sensors, mass airflow, crank and cam sensors, wiring faults. The stuff that makes "
     "a car run wrong without anything looking broken."),
    ("Pre purchase inspections", "ppi",
     "Buying something off Marketplace? Bring it by before you hand over the money. Cheapest "
     "hour you will ever spend."),
]

# Saying what you do not do is how a one man shop earns trust, and it saves phone calls.
NOT_DOING = [
    ("Transmission rebuilds and internal engine work",
     "Needs a lift and a bench. I will tell you who to call."),
    ("Alignments and tire mounting",
     "Takes a rack and a tire machine. I can do the suspension work first, then send you to get it aligned."),
    ("Air conditioning service",
     "Handling refrigerant takes certification and a recovery machine. I do not guess at AC."),
    ("Body work, paint and glass",
     "Different trade entirely."),
]

WORK = [
    dict(img="images/sienna-front-end.jpg", w=1050, h=1400,
         alt="Toyota Sienna with front bumper, headlights and grille removed for a radiator replacement",
         title="Radiator replacement, Toyota Sienna 3.3 V6",
         body="Front end comes apart to get the radiator out on these. Bumper cover, headlights, "
              "upper support. Old radiator is on the floor, drained, pan still under it."),
    dict(img="images/radiator-out.jpg", w=1400, h=1050,
         alt="Removed car radiator standing against a garage wall next to a spare tire",
         title="The old one, out",
         body="Same job. This is what came out of it. You should always get to look at the part "
              "you paid to replace."),
]

# Stock, clearly labeled. Faceless detail shots only. A stock photo of a person on a
# one man shop's site reads as the owner, which would be misleading.
STOCK = [
    ("images/stock/brakes.jpg", 1400, 935, "Disc brake rotor and caliper on a vehicle"),
    ("images/stock/engine.jpg", 1400, 933, "Hands working on a car engine"),
    ("images/stock/battery.jpg", 1400, 934, "Car battery with jumper cables attached in an engine bay"),
    ("images/stock/tools.jpg", 1400, 933, "Hand selecting a wrench from an organized toolbox"),
]

CSS = """
:root{--ground:#16130F;--surface:#211C16;--raised:#2B251D;--ink:#F1ECE4;--muted:#A2978A;
--line:#3A3227;--accent:#E8622A;--brass:#D8A23A;--max:68rem}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--ground);color:var(--ink);
font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;padding-bottom:5.5rem}
.wrap{max-width:var(--max);margin:0 auto;padding:0 1.25rem}
h1,h2,h3{margin:0 0 .5rem;line-height:1.1;letter-spacing:-.02em;text-wrap:balance}
h1{font-size:clamp(2rem,6.5vw,3.6rem);font-weight:800;text-transform:uppercase}
h2{font-size:clamp(1.45rem,4vw,2.1rem);font-weight:800;text-transform:uppercase}
h3{font-size:1.02rem;font-weight:700}
p{margin:0 0 1rem;max-width:64ch}a{color:var(--accent)}
.eyebrow{font-size:.76rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--brass);margin:0 0 .7rem}
header{border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.9rem 0;flex-wrap:wrap}
.bar img{height:46px;width:auto;display:block}
.bar a.call{background:var(--accent);color:#160D06;text-decoration:none;font-weight:800;padding:.6rem 1rem;border-radius:.3rem;white-space:nowrap}
.hero{padding:3.25rem 0 2.75rem;border-bottom:1px solid var(--line)}
.hero p.lede{font-size:clamp(1.05rem,2.2vw,1.28rem);max-width:48ch}
.cta{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.6rem}
.btn{display:inline-block;text-decoration:none;font-weight:800;padding:.85rem 1.4rem;border-radius:.3rem;background:var(--accent);color:#160D06}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}
.strip{display:flex;flex-wrap:wrap;gap:.5rem 1.75rem;padding:1.1rem 0;color:var(--muted);font-size:.92rem}
.strip b{color:var(--ink)}
section{padding:3rem 0;border-bottom:1px solid var(--line)}
.svc{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:.4rem;overflow:hidden;margin-top:1.6rem}
@media(min-width:38rem){.svc{grid-template-columns:1fr 1fr}}
@media(min-width:60rem){.svc{grid-template-columns:1fr 1fr 1fr}}
.svc>div{background:var(--surface);padding:1.15rem}
.svc p{color:var(--muted);font-size:.92rem;margin:.3rem 0 0}
.gal{display:grid;align-items:start;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:.4rem;overflow:hidden;margin-top:1.5rem}
@media(min-width:44rem){.gal{grid-template-columns:repeat(4,1fr)}}
.gal img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover}
.job{margin-top:1.5rem;background:var(--surface);border:1px solid var(--line);border-radius:.4rem;overflow:hidden}
@media(min-width:48rem){.job{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr)}}
.job img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;background:var(--raised)}
@media(min-width:48rem){.job img{height:100%;aspect-ratio:auto;max-height:24rem}}
.job .copy{padding:1.4rem;display:flex;flex-direction:column;justify-content:center}
.job .copy p{color:var(--muted);margin:0}
ul.plain{padding-left:1.1rem;margin:1.2rem 0 0}
.plain li{margin:0 0 .8rem;color:var(--muted);max-width:64ch}.plain li b{color:var(--ink)}
.towns{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.2rem}
.towns span{background:var(--surface);border:1px solid var(--line);border-radius:2rem;padding:.35rem .85rem;font-size:.88rem;color:var(--muted)}
.note{background:var(--raised);border-left:3px solid var(--brass);padding:1rem 1.15rem;border-radius:.25rem;color:var(--muted);margin-top:1.4rem}
.note b{color:var(--ink)}
.fine{color:var(--muted);font-size:.82rem;margin-top:.75rem}
footer{padding:2.25rem 0 2.75rem;color:var(--muted);font-size:.9rem}
footer a{color:var(--ink)}
.dock{position:fixed;left:0;right:0;bottom:0;z-index:20;display:flex;gap:1px;background:var(--line);border-top:1px solid var(--line)}
.dock a{flex:1;text-align:center;padding:1.05rem .5rem;text-decoration:none;font-weight:800;background:var(--accent);color:#160D06}
.dock a.alt{background:var(--raised);color:var(--ink)}
@media(min-width:48rem){.dock{display:none}body{padding-bottom:0}}
"""

def page():
    robots = '  <meta name="robots" content="noindex, nofollow">\n' if NOINDEX else ''
    title = f"Auto Repair in {CITY}, {STATE} | {BRAND}"
    desc = (f"Independent mechanic in {CITY}, {STATE}. Brakes, oil changes, batteries, radiators, "
            f"check engine lights and suspension. One mechanic, straight answers, evenings and "
            f"weekends. Call or text {PHONE_HUMAN}.")

    svc = "\n".join(f'      <div id="{sid}"><h3>{n}</h3><p>{d}</p></div>' for n, sid, d in SERVICES)
    notdo = "\n".join(f'        <li><b>{n}.</b> {d}</li>' for n, d in NOT_DOING)
    gal = "\n".join(
        f'      <img src="{src}?v={ASSET_V}" loading="lazy" width="{w}" height="{h}" alt="{alt}">'
        for src, w, h, alt in STOCK)
    jobs = "\n".join(
        f'''    <article class="job">
      <img src="{j["img"]}?v={ASSET_V}" width="{j["w"]}" height="{j["h"]}" loading="lazy" alt="{j["alt"]}">
      <div class="copy"><h3>{j["title"]}</h3><p>{j["body"]}</p></div>
    </article>''' for j in WORK)
    towns = "\n".join(f'        <span>{t}</span>' for t in TOWNS)

    schema = {
        "@context": "https://schema.org", "@type": "AutoRepair", "name": BRAND,
        "telephone": PHONE_E164,
        "areaServed": [{"@type": "City", "name": f"{t}, {STATE}"} for t in TOWNS],
        "address": {"@type": "PostalAddress", "addressLocality": CITY,
                    "addressRegion": STATE, "addressCountry": "US"},
        "priceRange": "$$",
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
             "opens": "17:00", "closes": "21:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Saturday","Sunday"], "opens": "08:00", "closes": "18:00"}],
    }

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{robots}  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{SITE}/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <link rel="icon" href="brand/logo-mark.svg">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps(schema)}</script>
</head>
<body>

<header>
  <div class="wrap bar">
    <img src="brand/logo-horizontal-dark.svg?v={ASSET_V}" alt="{BRAND}, auto repair in {CITY}, {STATE}">
    <a class="call" href="tel:{PHONE_E164}">Call or text {PHONE_HUMAN}</a>
  </div>
</header>

<main>
  <div class="hero">
    <div class="wrap">
      <p class="eyebrow">Auto repair &#183; {CITY}, {STATE}</p>
      <h1>I fix cars in {CITY}.</h1>
      <p class="lede">I am Joe. One mechanic, my own tools, working on cars for people around
      {CITY}. You call me, I work on it, I hand it back and I tell you what I found. Nobody in
      between.</p>
      <div class="cta">
        <a class="btn" href="tel:{PHONE_E164}">Call {PHONE_HUMAN}</a>
        <a class="btn ghost" href="sms:{PHONE_E164}">Text me</a>
      </div>
      <div class="strip">
        <span><b>Evenings and weekends</b></span>
        <span><b>You bring it to me</b></span>
        <span><b>Cash, Zelle, Venmo, Cash App</b></span>
      </div>
    </div>
  </div>

  <section id="services">
    <div class="wrap">
      <p class="eyebrow">What I do</p>
      <h2>Car repair in {CITY} and the towns around it.</h2>
      <p>If you are not sure what is wrong, just tell me what it is doing. A video of the noise
      tells me more than anything you could write down.</p>
      <div class="svc">
{svc}
      </div>
      <div class="gal">
{gal}
      </div>
      <p class="fine">Photos in this row are stock images showing the kind of work, used until Joe
      has his own picture of each job. Real jobs are below.</p>
    </div>
  </section>

  <section id="work">
    <div class="wrap">
      <p class="eyebrow">Real jobs</p>
      <h2>My actual work.</h2>
      <p>These are mine, out of my own garage. Not somebody else's shop.</p>
{jobs}
      <div class="note"><b>REPLACE: more job photos needed.</b> One job here right now. Two or three
      more, with a before and after, is the difference between this page working and not.</div>
    </div>
  </section>

  <section id="why">
    <div class="wrap">
      <p class="eyebrow">Why one mechanic</p>
      <h2>Same guy every time.</h2>
      <p>Big shops move you through whoever is open and hand you to a service writer who has never
      seen your car. Here it is one person. The guy who figured out what was wrong is the guy who
      fixed it and the guy who hands you the keys.</p>
      <ul class="plain">
        <li><b>You talk to the mechanic.</b> Not a counter, not a call center. Question about the
        repair? You are already talking to whoever did it.</li>
        <li><b>I learn your car.</b> Second time out, I already know what I put on it and what I
        told you to watch.</li>
        <li><b>No upsell sheet.</b> I will tell you what it needs now, what can wait and what you
        can leave alone. A lot can wait. Somebody should tell you that.</li>
        <li><b>You see the old parts.</b> Every job. If I say the rotors were done, they will be
        sitting there.</li>
        <li><b>Word of mouth is the whole business.</b> Most of my work comes from somebody sending
        somebody. That only holds up if I do right by the person in front of me.</li>
      </ul>
    </div>
  </section>

  <section id="not">
    <div class="wrap">
      <p class="eyebrow">Being straight with you</p>
      <h2>What I will send you elsewhere for.</h2>
      <p>I would rather tell you up front than take your money and figure it out after.</p>
      <ul class="plain">
{notdo}
      </ul>
    </div>
  </section>

  <section id="areas">
    <div class="wrap">
      <p class="eyebrow">Where I work</p>
      <h2>{CITY} and the surrounding towns.</h2>
      <p>You bring the car to me. If you are not sure whether you are too far out, just ask.</p>
      <div class="towns">
{towns}
      </div>
    </div>
  </section>

  <section id="contact">
    <div class="wrap">
      <p class="eyebrow">Get it looked at</p>
      <h2>Tell me what it is doing.</h2>
      <p>Fastest thing is a text with the year, make and model and what is going on. Send a video of
      the noise if you can.</p>
      <div class="cta">
        <a class="btn" href="tel:{PHONE_E164}">Call {PHONE_HUMAN}</a>
        <a class="btn ghost" href="sms:{PHONE_E164}">Text me</a>
      </div>
      <div class="note">
        <b>Hours:</b> evenings and weekends, by appointment. Drop it off or leave it with me and get
        it when it is done.<br>
        <b>Payment:</b> cash, Zelle, Venmo or Cash App when you pick the car up.
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <p><b>{BRAND}</b><br>Auto repair in {CITY}, {STATE} and the surrounding towns.<br>
    Call or text <a href="tel:{PHONE_E164}">{PHONE_HUMAN}</a></p>
    <p style="font-size:.84rem">Independent and locally owned. Not affiliated with any dealership or
    repair chain. Some photos on this page are stock images used to illustrate services.</p>
  </div>
</footer>

<nav class="dock">
  <a href="tel:{PHONE_E164}">Call</a>
  <a class="alt" href="sms:{PHONE_E164}">Text</a>
</nav>

</body>
</html>
'''

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    html = page()
    open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(html)
    if NOINDEX:
        open(os.path.join(here, "robots.txt"), "w", encoding="utf-8").write("User-agent: *\nDisallow: /\n")
    print(f"wrote index.html ({len(html):,} bytes)")
    print(f"noindex: {NOINDEX}   placeholders: {html.count('REPLACE:')}   services: {len(SERVICES)}")

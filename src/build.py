#!/usr/bin/env python3
"""Builds the static site in ../public from content.json.

Usage:  python3 src/build.py
Edit src/content.json (works, lyrics, sources, links, legal data), then rebuild and commit.
"""
import json, os, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "public")
D = json.load(open(os.path.join(ROOT, "content.json"), encoding="utf-8"))
E = lambda s: html.escape(s, quote=True)

SC_PARAMS = "&color=%23151413&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false"


def sc_src(item):
    # player_src = the src from SoundCloud's embed code, cut before "&color=" (style params are set here)
    return item["player_src"] + SC_PARAMS


def sc_slot(item, title):
    return f'''<div class="sc" lang="de" data-src="{E(sc_src(item))}" data-title="{E(title)}">
  <div class="sc-ph">
    <p class="mono dim">SoundCloud · Player nicht geladen</p>
    <p>Beim Laden des Players werden Daten an SoundCloud übertragen und Cookies gesetzt. <a href="/datenschutz#soundcloud">Datenschutz</a></p>
    <div class="acts mono">
      <button class="btn" type="button" data-sc-once>Player laden</button>
      <button class="textbtn" type="button" data-sc-always>Immer erlauben</button>
      <a href="{E(item["soundcloud"])}" target="_blank" rel="noopener">Auf SoundCloud öffnen ↗</a>
    </div>
  </div>
</div>'''


def film(img, alt, label, glow=False, eager=False):
    return f'''<div class="film" role="img" aria-label="{E(alt)}">
  <div class="weave"><img class="photo" src="{img}" alt="" width="1200" height="1200"{'' if eager else ' loading="lazy"'} decoding="async">{'<div class="slitglow"></div>' if glow else ''}</div>
  <div class="expo"></div><div class="leak"></div>
  <svg class="grain" aria-hidden="true"><filter id="g{os.path.basename(img).split(".")[0]}"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#g{os.path.basename(img).split(".")[0]})"/></svg>
  <div class="scratch s1"></div><div class="scratch s2"></div>
  <div class="dust d1"></div><div class="dust d2"></div><div class="dust d3"></div>
  <div class="label">{E(label)}</div>
</div>'''


def secs(d):
    m, s = d.split(":")
    return int(m) * 60 + int(s)


def head(title, desc, path):
    return f'''<!doctype html>
<html lang="{'de' if path != '/' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://minor-damage.de{path}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="https://minor-damage.de/assets/img/album.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#E6E3DC">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/schibsted-grotesk-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>'''


def site_head(nav):
    links = "".join(f'<a href="{h}">{t}</a>' for t, h in nav)
    return f'''<header class="site-head mono">
  <a href="/" style="border:0" class="dim">Register — {pad3(len(D["works"]))} entries · {pad3(len([w for w in D["works"] if w["status"]=="accessible"]))} accessible</a>
  <nav aria-label="Sections">{links}</nav>
</header>'''


def pad3(n):
    return f"{n:03d}"


BANNER = '''<div class="consent" id="consent" lang="de" role="region" aria-label="Datenschutz-Einstellungen" hidden>
  <div class="wrap">
    <p>Diese Seite bindet Player von SoundCloud ein. Beim Laden werden Daten (u. a. Ihre IP-Adresse) an SoundCloud übertragen und Cookies gesetzt; dabei ist eine Übermittlung in Drittländer möglich. Ohne Ihre Einwilligung wird nichts von SoundCloud geladen. Sie können Ihre Entscheidung jederzeit über „Datenschutz-Einstellungen“ ändern. <a href="/datenschutz">Datenschutzerklärung</a></p>
    <div class="acts">
      <button class="btn" type="button" data-accept>SoundCloud erlauben</button>
      <button class="btn" type="button" data-reject>Ablehnen</button>
    </div>
  </div>
</div>'''


def foot():
    return f'''<footer class="site-foot mono">
  <span>PREHEAT</span>
  <span class="dim">A work by Minor Damage</span>
  <span class="links"><a href="/impressum">Impressum</a><a href="/datenschutz">Datenschutz</a><button class="textbtn" type="button" data-consent-settings>Datenschutz-Einstellungen</button><span class="dim">2026</span></span>
</footer>'''


def tail():
    return f'''{BANNER}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''


# ——— index ———
def build_index():
    A, W = D["album"], D["works"]
    total = sum(secs(w["duration"]) for w in W)
    rows = []
    for w in W:
        n = w["no"]
        heat = '<span class="trace-line" aria-hidden="true" style="left:46.8%;top:-22px;bottom:-22px"></span>' if w["trace"] == "heat" else ""
        ref = "".join(f"<li>{E(x)}</li>" for x in ["Brüder Grimm", "Kinder- und Hausmärchen", w["khm"], "Ausgabe letzter Hand, 1857", "Hg. Heinz Rölleke"])
        ctx = "".join(f"<p>{E(c)}</p>" for c in w["context"])
        rows.append(f'''<div id="entry-{n}">
  <button class="row trace-{w["trace"]}" type="button" data-file-toggle aria-expanded="false" aria-controls="file-{n}">
    <span class="c-no mono">{n}</span>
    <span class="c-thumb thumbwrap"><span class="thumb"><img src="{w["thumb"]}" alt="" width="480" height="480" loading="lazy" decoding="async"></span>{heat}</span>
    <span class="c-title">{E(w["title"])}</span>
    <span>{E(w["tale"])}</span>
    <span class="c-khm mono">{E(w["khm"])}</span>
    <span>{E(w["scene"])}</span>
    <span class="c-year mono">{w["year"]}</span>
    <span class="mono" data-toggle-label>Open file +</span>
  </button>
  <article class="file" id="file-{n}" aria-label="{n} {E(w["title"])}, {E(w["tale"])}, {E(w["khm"])}" hidden>
    <div class="file-bar mono">
      <span><span class="dim">Archive / </span>{n}<span class="dim"> / File</span></span>
      <button class="textbtn" type="button" data-file-close="file-{n}">Close file —</button>
    </div>
    <div class="artefact">
      <div class="art">
        {film(w["image"], "Artefact " + n + ": " + w["alt"], n + " · still · loop to follow", glow=(w["trace"] == "heat"))}
        <div class="caption mono dim"><span>A — Artefact · still</span><span>Loop not yet deposited</span></div>
      </div>
      <div class="side">
        <h3>{E(w["title"])}</h3>
        <dl class="mono meta">
          <dt>Object</dt><dd>{E(w["object"])}</dd>
          <dt>Duration</dt><dd>{w["duration"]}</dd>
          <dt>Source</dt><dd>{E(w["khm"])}</dd>
          <dt>Tale</dt><dd>{E(w["tale"])}</dd>
          <dt>Scene</dt><dd>{E(w["scene"])}</dd>
          <dt>Motif</dt><dd>{E(w["motif"])}</dd>
          <dt>Year</dt><dd>{w["year"]}</dd>
          <dt>Status</dt><dd>Accessible</dd>
        </dl>
        <div class="sect"><span class="mono dim">Context</span><div class="ctx">{ctx}</div></div>
        <div class="sect"><span class="mono dim">Audio</span>{sc_slot(w, "SoundCloud: " + w["title"])}</div>
      </div>
    </div>
    <div class="source">
      <div class="ref"><span class="mono dim">B — Primary source</span><ul class="mono">{ref}</ul></div>
      <blockquote lang="de">{E(w["source"])}</blockquote>
    </div>
    <div class="lyrics-row"><span class="mono dim">C — Lyrics</span><p class="lyrics">{E(w["lyrics"])}</p></div>
  </article>
</div>''')

    coming = "".join(f'''<div class="item"><div class="mono"><span>{E(c["khm"])}</span><span class="dim">{E(c["tale"])}</span><span class="dim" style="margin-top:10px">Pending</span></div><blockquote lang="de">{E(c["fragment"])}</blockquote></div>''' for c in D["coming"])
    credits = "".join(f"<dt>{E(a)}</dt><dd>{E(b)}</dd>" for a, b in D["credits"])

    page = head("PREHEAT — Minor Damage",
                "PREHEAT isolates moments from the Grimm tales and translates them into sound and moving images. A work by Minor Damage.", "/")
    page += f'''
<div class="wrap">
{site_head([("Works", "#archive"), ("Listen", "#album"), ("Process", "#process")])}
<main id="main">
  <div class="wordrow"><h1 class="wordmark">PREHEAT</h1><span class="mono dim">Archive / 2026–</span></div>

  <section class="opening" id="album" aria-label="Album PREHEAT">
    <div class="art">{film(A["image"], "Album PREHEAT: " + A["alt"], "001–005 · album · 2026", eager=True)}</div>
    <div class="side">
      <dl class="mono meta">
        <dt>No.</dt><dd>{A["no"]}</dd>
        <dt>Object</dt><dd>Album</dd>
        <dt>Title</dt><dd>{A["title"]}</dd>
        <dt>Tracks</dt><dd>{len(W)}</dd>
        <dt>Duration</dt><dd>{total//60}:{total%60:02d}</dd>
        <dt>Year</dt><dd>{A["year"]}</dd>
      </dl>
      {sc_slot(A, "SoundCloud: PREHEAT (album)")}
      <a class="mono" href="#archive" style="align-self:flex-start">Archive 001–005 →</a>
    </div>
  </section>

  <section class="note" aria-label="Project note">
    <span class="mono dim">Project note / 001</span>
    <div class="body">
      <p>PREHEAT isolates moments from the Grimm tales and translates them into sound and moving images.</p>
      <p>The story is not retold.</p>
      <p>The event itself is never shown.</p>
      <p>We remain in the second before or the second after.</p>
    </div>
  </section>

  <section class="archive" id="archive" aria-label="Archive">
    <div class="sec-head"><h2>Archive</h2><span class="mono dim">{pad3(len(W))} entries · {pad3(len(W))} accessible</span></div>
    <div class="row row-head mono dim" aria-hidden="true"><span class="c-no">No.</span><span class="c-thumb">Loop</span><span>Title</span><span>Tale</span><span class="c-khm">Source</span><span>Scene</span><span class="c-year">Year</span><span>Status</span></div>
    {"".join(rows)}
    <div class="rule-top"></div>
  </section>

  <section class="pending" id="pending" aria-label="Coming soon">
    <div class="sec-head"><h2 class="small">Coming soon</h2><span class="mono dim">Source material · pending</span></div>
    {coming}
  </section>

  <section class="block" id="process" aria-label="Process">
    <span class="mono dim">Process</span>
    <div class="body">
      <p class="lead">PREHEAT is a work by Minor Damage.</p>
      <dl class="mono meta credits">{credits}</dl>
      <p class="mono dim">Production notes — generative audio and image tools: [documentation to follow]</p>
      <p class="mono dim">Grimm texts quoted from: Brüder Grimm, Kinder- und Hausmärchen. Ausgabe letzter Hand, 1857. Hg. Heinz Rölleke.</p>
    </div>
  </section>

  <section class="block" id="channels" aria-label="Channels">
    <span class="mono dim">Channels</span>
    <div class="body mono"><span><span class="dim">Listen — </span><a href="{E(A["soundcloud"])}" target="_blank" rel="noopener">SoundCloud ↗</a></span></div>
  </section>
</main>
{foot()}
</div>
'''
    page += tail()
    return page


def legal_page(path, title, h1, body):
    page = head(title, title, path)
    page += f'''
<div class="wrap">
<header class="site-head mono"><a href="/" style="border:0">PREHEAT</a><nav aria-label="Sections"><a href="/#archive">Works</a><a href="/#album">Listen</a><a href="/#process">Process</a></nav></header>
<main id="main" class="legal">
<h1>{h1}</h1>
{body}
</main>
{foot()}
</div>
'''
    return page + tail()


def sec(title, inner, id_=""):
    return f'<section{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><h2>{title}</h2><div class="body">{inner}</div></section>'


L = D["legal"]
EMAIL = L["email"] or "[E-MAIL-ADRESSE]"
ADDR = f'<address>{E(L["name"])}<br>{E(L["street"])}<br>{E(L["city"])}<br>{E(L["country"])}</address>'
CONTACT = f'<p>Telefon: {E(L["phone"])}<br>E-Mail: <a href="mailto:{E(EMAIL)}">{E(EMAIL)}</a></p>'

IMPRESSUM = "".join([
    sec("Angaben gemäß § 5 DDG", ADDR),
    sec("Kontakt", CONTACT),
    sec("Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV", f'<p>{E(L["name"])}, Anschrift wie oben.</p>'),
    sec("Projekt", "<p>PREHEAT ist ein Werk von Minor Damage.</p>"),
    sec("Urheberrecht", "<p>Musik, Texte, Bilder und Gestaltung dieser Website sind urheberrechtlich geschützt. Jede Verwendung außerhalb der Grenzen des Urheberrechts bedarf der vorherigen Zustimmung.</p><p>Die Märchentexte der Brüder Grimm sind gemeinfrei. Sie werden zitiert nach: Brüder Grimm, Kinder- und Hausmärchen. Ausgabe letzter Hand, 1857. Hg. Heinz Rölleke.</p><p>Schriften: Schibsted Grotesk und IBM Plex Mono, SIL Open Font License 1.1.</p>"),
])

DATENSCHUTZ = "".join([
    sec("1. Verantwortlicher", f"<p>Verantwortlich für die Datenverarbeitung auf dieser Website im Sinne der Datenschutz-Grundverordnung (DSGVO):</p>{ADDR}{CONTACT}"),
    sec("2. Überblick", "<p>Diese Website ist ein künstlerisches Projekt ohne Benutzerkonten, Formulare, Newsletter oder Analyse-Werkzeuge. Personenbezogene Daten werden nur verarbeitet, soweit es für die Auslieferung der Website technisch erforderlich ist, wenn Sie uns kontaktieren oder wenn Sie dem Laden der SoundCloud-Player zustimmen.</p>"),
    sec("3. Hosting und Server-Logs", "<p>Die Website wird bei Vercel Inc., 440 N Barranca Avenue #4133, Covina, CA 91723, USA, gehostet. Beim Aufruf der Website verarbeitet Vercel automatisch technische Daten, die Ihr Browser übermittelt, insbesondere IP-Adresse, Datum und Uhrzeit des Zugriffs, aufgerufene Seite, Referrer, Browsertyp und Betriebssystem sowie daraus abgeleitete ungefähre Standortinformationen (Stadt, Land).</p><p>Zweck ist die Auslieferung der Website sowie die Gewährleistung von Stabilität und Sicherheit. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; unser berechtigtes Interesse liegt im sicheren und fehlerfreien Betrieb der Website.</p><p>Vercel verarbeitet diese Daten in unserem Auftrag auf Grundlage eines Vertrags zur Auftragsverarbeitung (Art. 28 DSGVO, Data Processing Addendum). Dabei kann eine Übermittlung in die USA erfolgen. Vercel ist nach dem EU-U.S. Data Privacy Framework zertifiziert; die Übermittlung stützt sich auf den Angemessenheitsbeschluss der EU-Kommission (Art. 45 DSGVO). Weitere Informationen: <a href=\"https://vercel.com/legal/privacy-policy\" target=\"_blank\" rel=\"noopener\">Datenschutzerklärung von Vercel</a>.</p>"),
    sec("4. Cookies und lokale Speicherung", "<p>Diese Website selbst setzt keine Cookies und verwendet keine Analyse- oder Tracking-Werkzeuge.</p><p>Ihre Entscheidung zum Laden der SoundCloud-Player wird im lokalen Speicher Ihres Browsers (Local Storage) abgelegt, damit die Abfrage nicht bei jedem Besuch erneut erscheint. Diese Speicherung ist für den von Ihnen gewünschten Dienst unbedingt erforderlich (§ 25 Abs. 2 Nr. 2 TDDDG); Rechtsgrundlage für die damit verbundene Verarbeitung ist Art. 6 Abs. 1 lit. c DSGVO i. V. m. Art. 7 Abs. 1 DSGVO (Nachweis der Einwilligung). Sie können den Eintrag jederzeit über die Einstellungen Ihres Browsers löschen.</p><p>Schriftarten werden von dieser Website selbst ausgeliefert; es findet keine Verbindung zu externen Schriftanbietern statt.</p>"),
    sec("5. SoundCloud-Player", "<p>Auf dieser Website können Player des Dienstes SoundCloud eingebunden werden. Anbieter ist die SoundCloud Global Limited &amp; Co. KG, Karl-Marx-Straße 101, 12043 Berlin.</p><p>Die Player werden erst geladen, wenn Sie dem zugestimmt haben – entweder dauerhaft über die Abfrage („SoundCloud erlauben“) oder einmalig für einen einzelnen Player („Player laden“). Vorher wird keine Verbindung zu SoundCloud aufgebaut.</p><p>Nach dem Laden erhält SoundCloud insbesondere Ihre IP-Adresse, Informationen über Ihr Endgerät und Ihren Browser, die aufgerufene Seite sowie Informationen über die Wiedergabe. SoundCloud setzt Cookies bzw. vergleichbare Technologien. Sind Sie bei SoundCloud angemeldet, kann SoundCloud die Nutzung Ihrem Konto zuordnen. SoundCloud kann Daten auch in Länder außerhalb des Europäischen Wirtschaftsraums übermitteln; nach eigenen Angaben stützt sich SoundCloud dabei auf Standardvertragsklauseln der EU-Kommission.</p><p>Rechtsgrundlage ist Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG). Sie können Ihre Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen, indem Sie unten auf der Seite „Datenschutz-Einstellungen“ wählen und „Ablehnen“ klicken.</p><p>Weitere Informationen: <a href=\"https://soundcloud.com/pages/privacy\" target=\"_blank\" rel=\"noopener\">Datenschutzerklärung von SoundCloud</a>.</p>", "soundcloud"),
    sec("6. Externe Links", "<p>Diese Website enthält Links zu SoundCloud. Erst wenn Sie einem solchen Link folgen, werden Daten an den jeweiligen Anbieter übertragen; für die Verarbeitung dort ist der jeweilige Anbieter verantwortlich.</p>"),
    sec("7. Kontakt", "<p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung der Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO, bei Anfragen zu einem Vertrag Art. 6 Abs. 1 lit. b DSGVO. Die Daten werden gelöscht, sobald sie für die Bearbeitung nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>"),
    sec("8. Ihre Rechte", "<p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO (Art. 21). Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen (Art. 7 Abs. 3 DSGVO).</p><p>Sie haben außerdem das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren (Art. 77 DSGVO), zum Beispiel bei der Berliner Beauftragten für Datenschutz und Informationsfreiheit.</p>"),
    sec("Stand", f"<p>{E(L['updated'])}</p>"),
])

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#151413"/><rect x="15" y="5" width="2" height="22" fill="#C3733C"/></svg>\n'


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


write("index.html", build_index())
write("impressum.html", legal_page("/impressum", "Impressum — PREHEAT / Minor Damage", "Impressum", IMPRESSUM))
write("datenschutz.html", legal_page("/datenschutz", "Datenschutzerklärung — PREHEAT / Minor Damage", "Datenschutz&shy;erklärung", DATENSCHUTZ))
write("favicon.svg", FAVICON)
write("robots.txt", "User-agent: *\nAllow: /\n")
print("built", OUT)

"""Refresh the "Latest insights" block on the home page.

Copies the first three cards from insights/index.html (newest first)
into index.html between the latest-insights markers, and sets the home
page's lastmod in sitemap.xml to today's date.
Run from the site root: python3 .github/scripts/latest_insights.py
"""
import datetime, re, sys, zoneinfo

START, END = "<!-- latest-insights:start -->", "<!-- latest-insights:end -->"
COLOURS = ["blue", "grn", "red"]

insights = open("insights/index.html", encoding="utf-8").read()
cards = re.findall(
    r'<div class="route"><div class="route-num">\d+</div>'
    r'<div class="route-icon" style="background:var\(--ms-\w+\)"></div>'
    r'(<h3 class="route-title">.*?</h3><div class="route-desc">.*?</div>'
    r'<a href="[^"]+" class="route-link">.*?</a></div>)', insights, re.S)[:3]
if len(cards) < 3:
    sys.exit("Fewer than three cards found on the Insights page")

block = START + '<div class="routes three">' + "".join(
    f'<div class="route"><div class="route-num">{i + 1:02d}</div>'
    f'<div class="route-icon" style="background:var(--ms-{COLOURS[i]})"></div>{c}'
    for i, c in enumerate(cards)) + "</div>" + END

home = open("index.html", encoding="utf-8").read()
if home.count(START) != 1 or home.count(END) != 1:
    sys.exit("Latest insights markers not found exactly once in index.html")
new_home = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda m: block, home, flags=re.S)

if new_home != home:
    open("index.html", "w", encoding="utf-8").write(new_home)
    today = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/London")).date().isoformat()
    sm = open("sitemap.xml", encoding="utf-8").read()
    sm = re.sub(r"(<loc>https://businessapps\.adjona\.com/</loc><lastmod>)[^<]*",
                lambda m: m.group(1) + today, sm, count=1)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("Home page updated")
else:
    print("Home page already up to date")

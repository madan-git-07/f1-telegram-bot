"""F1 daily brief -> Telegram."""
import html
import os
import sys
from datetime import datetime, timedelta, timezone

import feedparser
import requests
from dotenv import load_dotenv

load_dotenv()

API = "https://api.jolpi.ca/ergast/f1/current"
NEWS_URL = "https://www.formula1.com/content/fom-website/en/latest/all.xml"
IST = timezone(timedelta(hours=5, minutes=30))  # India has no DST, so a fixed offset is fine
RACE_DURATION = timedelta(hours=3)
SESSIONS = {
    "FirstPractice": "Practice 1",
    "SecondPractice": "Practice 2",
    "ThirdPractice": "Practice 3",
    "SprintQualifying": "Sprint Qualifying",
    "SprintShootout": "Sprint Shootout",
    "Sprint": "Sprint",
    "Qualifying": "Qualifying",
}
failures = []


def get_json(path):
    r = requests.get(f"{API}{path}.json?limit=100", timeout=15)
    r.raise_for_status()
    return r.json()["MRData"]


def when(d):
    """Ergast {'date': ..., 'time': ...} dict -> aware datetime, or None."""
    if not d or "time" not in d:
        return None
    return datetime.fromisoformat(f"{d['date']}T{d['time']}".replace("Z", "+00:00"))


def schedule_section():
    now = datetime.now(timezone.utc)
    for race in get_json("")["RaceTable"]["Races"]:
        start = when(race)
        # Keep showing the current weekend until the race has actually finished.
        if start and start + RACE_DURATION >= now:
            break
    else:
        return "🏁 <b>Season over.</b>"

    sessions = [(label, when(race.get(key))) for key, label in SESSIONS.items()]
    sessions.append(("Race", start))
    lines = [f"🏎 <b>{html.escape(race['raceName'])}</b>"]
    for label, t in sorted((s for s in sessions if s[1]), key=lambda s: s[1]):
        lines.append(f"• {label}: {t.astimezone(IST):%a %d %b, %I:%M %p} IST")
    return "\n".join(lines)


def standings_section(kind, title):
    lists = get_json(f"/{kind}standings")["StandingsTable"]["StandingsLists"]
    if not lists:
        return f"<b>{title}</b>\nNo standings yet."

    def name(r):
        if kind == "driver":
            d = r["Driver"]
            return f"{d['givenName']} {d['familyName']}"
        return r["Constructor"]["name"]

    rows = lists[0][f"{kind.capitalize()}Standings"]
    lines = [f"<b>{title}</b>"]
    lines += [f"{r['position']}. {html.escape(name(r))} — {r['points']}" for r in rows]
    return "\n".join(lines)


def news_section():
    r = requests.get(NEWS_URL, timeout=15)  # feedparser has no timeout of its own
    r.raise_for_status()
    entries = feedparser.parse(r.content).entries[:5]
    if not entries:
        raise RuntimeError("feed returned no entries")
    lines = ["📰 <b>Headlines</b>"]
    for e in entries:
        lines.append(f'• <a href="{html.escape(e.link, quote=True)}">{html.escape(e.title)}</a>')
    return "\n".join(lines)


def safe(label, fn, *args):
    """One broken source must not take down the whole brief."""
    try:
        return fn(*args)
    except Exception as e:
        failures.append(label)
        print(f"{label} failed: {type(e).__name__}: {e}", file=sys.stderr)
        return f"<i>{label} unavailable.</i>"


def send(text):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage",
            json={
                "chat_id": os.environ["CHAT_ID"],
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=15,
        )
    except requests.RequestException as e:
        # Never print e itself: requests puts the URL (which contains the bot token) in the message.
        sys.exit(f"Telegram request failed: {type(e).__name__}")
    if not r.ok:
        sys.exit(f"Telegram rejected the message ({r.status_code}): {r.text[:300]}")


def main():
    text = "\n\n".join([
        safe("Schedule", schedule_section),
        safe("Driver standings", standings_section, "driver", "🏆 Driver Standings"),
        safe("Constructor standings", standings_section, "constructor", "🏭 Constructor Standings"),
        safe("Headlines", news_section),
    ])
    if "--dry" in sys.argv:
        print(text)
    else:
        send(text)
        print("Sent.")
    if failures:
        sys.exit(f"Sections failed: {', '.join(failures)}")  # red run in Actions, but the brief still went out


if __name__ == "__main__":
    main()

import os
from datetime import datetime

import fastf1
import pytz

# Create cache folder if needed
os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

IST = pytz.timezone("Asia/Kolkata")


def format_time(utc_time):
    """Convert UTC time to IST and format nicely."""
    if utc_time is None:
        return "TBD"

    # Ensure timezone-aware
    if utc_time.tzinfo is None:
        utc_time = utc_time.tz_localize("UTC")
    else:
        utc_time = utc_time.tz_convert("UTC")

    ist_time = utc_time.tz_convert(IST)

    return ist_time.strftime("%d %b %Y, %I:%M %p IST")


def get_next_event():
    current_year = datetime.now().year
    today = datetime.now()

    schedule = fastf1.get_event_schedule(current_year)

    for _, event in schedule.iterrows():
        event_date = event["EventDate"].to_pydatetime()

        if event_date >= today:
            return event

    return None


def get_schedule():
    event = get_next_event()

    if event is None:
        return "No more races this season."

    gp = fastf1.get_event(datetime.now().year, event["EventName"])

    message = []
    message.append(f"🏎 *{gp['EventName']}*")
    message.append("")

    for i in range(1, 6):
        session = gp.get(f"Session{i}")
        session_time = gp.get(f"Session{i}DateUtc")

        if session:
            message.append(
                f"• *{session}*: {format_time(session_time)}"
            )

    return "\n".join(message)


if __name__ == "__main__":
    print(get_schedule())
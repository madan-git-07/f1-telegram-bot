import os
from datetime import datetime

import fastf1

os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")


def get_next_event():
    current_year = datetime.now().year
    today = datetime.now()

    schedule = fastf1.get_event_schedule(current_year)

    for _, event in schedule.iterrows():
        if event["EventDate"].to_pydatetime() >= today:
            return event

    return None


def get_schedule():
    event = get_next_event()

    if event is None:
        return "No more races this season."

    gp = fastf1.get_event(datetime.now().year, event["EventName"])

    message = []

    message.append(f"🏎 {gp['EventName']}")
    message.append("")

    for i in range(1, 6):
        session = gp.get(f"Session{i}")

        if session:
            time = gp.get(f"Session{i}DateUtc")
            message.append(f"• {session}: {time}")

    return "\n".join(message)


if __name__ == "__main__":
    print(get_schedule())
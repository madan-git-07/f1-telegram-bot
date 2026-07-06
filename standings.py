import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1/current"


def get_driver_standings():
    url = f"{BASE_URL}/driverstandings.json"

    data = requests.get(url, timeout=10).json()

    standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

    message = ["🏆 Driver Standings\n"]

    for driver in standings[:11]:
        given = driver["Driver"]["givenName"]
        family = driver["Driver"]["familyName"]
        points = driver["points"]

        message.append(f"{driver['position']}. {given} {family} — {points} pts")

    return "\n".join(message)


def get_constructor_standings():
    url = f"{BASE_URL}/constructorstandings.json"

    data = requests.get(url, timeout=10).json()

    standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

    message = ["🏭 Constructor Standings\n"]

    for team in standings[:11]:
        name = team["Constructor"]["name"]
        points = team["points"]

        message.append(f"{team['position']}. {name} — {points} pts")

    return "\n".join(message)


if __name__ == "__main__":
    print(get_driver_standings())
    print()
    print(get_constructor_standings())
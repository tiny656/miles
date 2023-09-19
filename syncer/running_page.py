import json
import math
import urllib.request
import sys

def get_activities_download_path(running_page_repo: str) -> str:
  return "https://raw.githubusercontent.com/{repo}/master/src/static/activities.json".format(repo=running_page_repo)

def get_activities(running_page_repo: str) -> []:
  path = get_activities_download_path(running_page_repo)
  with urllib.request.urlopen(path) as url:
    return json.loads(url.read().decode())

def refresh_running_csv(activities: list):
  with open("running.csv", "w") as f:
    f.write("DT,distance(Km),heart,pace\n")
    for activity in activities:
      f.write("{date},{distance:.2f},{heart:.0f},{pace}\n".format(
        date=activity["start_date"],
        distance=activity["distance"]/1000.,
        heart=activity["average_heartrate"] if activity["average_heartrate"] else 0,
        pace=get_format_pace(activity["average_speed"]),
      ))

def get_format_pace(average_speed: float) -> str:
  pace = (1000.0 / 60.0) * (1.0 / average_speed)
  minutes = math.floor(pace)
  seconds = math.floor((pace - minutes) * 60.0)
  return "{}:{:02d}".format(minutes, seconds)

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        sys.exit(
            "args is not right, e.g. python running_page.py tiny656/running_page"
        )

    running_page_repo = args[1]
    activities = get_activities(running_page_repo)
    refresh_running_csv(activities)
import requests
from bs4 import BeautifulSoup
import csv

url = "https://belaes.by/images/karta/SZZ.svg"
r = requests.get(url, verify=False)
soup = BeautifulSoup(r.text, "lxml")

id_region_tranformator = {
    "tspan5239-3-2": "Белорусская АЭС",
    "tspan5239-3": "Чехи",
    "tspan5239-1": "Маркуны",
    "tspan5239-36": "Ольховка",
    "tspan5239-0": "Свирь",
    "tspan5239": "Подольцы",
    "tspan5239-6": "Гоза",
    "tspan5239-57": "Ворона",
    "tspan5239-5": "Вороняны",
    "tspan5239-62": "Чернишки",
    "tspan5239-2": "Рымдюры",
}

record = {}

for k, v in id_region_tranformator.items():
    radiation_level = soup.find("tspan", {"id": f"{k}"}).text.strip()

    record[v] = radiation_level
timestamp = soup.find("text", {"id": "maxTime"}).text.replace("  ", "").split(" ")
record["date"] = timestamp[0]
record["time"] = timestamp[1]

csv_columns = [
    "Белорусская АЭС",
    "Чехи",
    "Маркуны",
    "Ольховка",
    "Свирь",
    "Подольцы",
    "Гоза",
    "Ворона",
    "Вороняны",
    "Чернишки",
    "Рымдюры",
    "date",
    "time",
]
csv_file = "radiation.csv"

with open(csv_file, "a") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writerow(record)

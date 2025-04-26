import csv
import ssl
import urllib3
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += (
        ":HIGH:!DH:!aNULL"
    )
except AttributeError:
    pass

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount("https://", CustomHttpAdapter(ctx))
    return session

url = "https://belaes.by/images/karta/SZZ.svg"

record = {}

try:
    r = get_legacy_session().get(url, timeout=30)
    r.raise_for_status()
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

    for k, v in id_region_tranformator.items():
        radiation_level = soup.find("tspan", {"id": f"{k}"}).text.strip()
        record[v] = radiation_level

    timestamp = soup.find("text", {"id": "maxTime"}).text.replace("  ", "").split(" ")
    record["date"] = timestamp[0]
    record["time"] = timestamp[1]

except requests.exceptions.RequestException as e:
    print(f"Error while connecting... {e}")

    now = datetime.utcnow().strftime("%d.%m.%Y %H:%M")
    date, time = now.split(" ")
    record = {
        "Белорусская АЭС": "N/A",
        "Чехи": "N/A",
        "Маркуны": "N/A",
        "Ольховка": "N/A",
        "Свирь": "N/A",
        "Подольцы": "N/A",
        "Гоза": "N/A",
        "Ворона": "N/A",
        "Вороняны": "N/A",
        "Чернишки": "N/A",
        "Рымдюры": "N/A",
        "date": date,
        "time": time,
    }

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

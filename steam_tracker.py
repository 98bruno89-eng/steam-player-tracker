import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app_ids = [1237950, 2767030, 1172470, 872200, 291550, 2073850, 2357570]

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

for app_id in app_ids:
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
    response = requests.get(url)
    data = response.json()
    player_count = data["response"]["player_count"]
    cursor.execute(
        "INSERT INTO player_counts (app_id, player_count, timestamp) VALUES (%s, %s, NOW())",
        (app_id, player_count)
    )
conn.commit()
cursor.close()
conn.close()

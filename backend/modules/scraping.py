import requests
from bs4 import BeautifulSoup
import json
import time

# 🔤 Pages à scraper
letters = [f"let{chr(i)}" for i in range(ord('a'), ord('z')+1)]

dataset = []

for l in letters:
    url = f"http://tenymalagasy.org/bins/rootLists?o={l}"
    print(f"Scraping: {url}")

    response = requests.get(url)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    # 🔥 récupérer toutes les lignes
    rows = soup.find_all("tr")

    for row in rows:
        links = row.find_all("a")

        if len(links) >= 2:
            root = links[0].text.strip()
            derives = [a.text.strip() for a in links[1:] if a.text.strip()]

            # ✅ ICI on filtre
            if len(root) > 2 and len(derives) >= 1:
                dataset.append({
                    "racine": root,
                    "derives": derives
                })

    time.sleep(1)

# 🔁 supprimer doublons
unique_dataset = []
seen = set()

for item in dataset:
    if item["racine"] not in seen:
        seen.add(item["racine"])
        unique_dataset.append(item)

# 💾 sauvegarde
with open("malagasy_roots.json", "w", encoding="utf-8") as f:
    json.dump(unique_dataset, f, ensure_ascii=False, indent=2)

print("✅ Terminé !")
print("Total racines:", len(unique_dataset))
import requests

# โหลดฟอนต์ Chakra Petch (ดู Sci-Fi) และ Sarabun (อ่านง่าย)
fonts = {
    "Chakra.ttf": "https://github.com/google/fonts/raw/main/ofl/chakrapetch/ChakraPetch-Bold.ttf",
    "Sarabun.ttf": "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf"
}

for name, url in fonts.items():
    print(f"Downloading {name}...")
    r = requests.get(url)
    with open(name, 'wb') as f:
        f.write(r.content)
    print("Done.")

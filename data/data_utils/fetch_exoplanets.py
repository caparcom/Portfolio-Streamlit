import requests
from urllib.parse import quote 

ADQL = """
SELECT
pl_name,
pl_rade,
pl_bmasse,
pl_orbper,
pl_eqt,
st_teff,
st_rad
FROM ps
WHERE
pl_rade IS NOT NULL
AND pl_bmasse IS NOT NULL
AND pl_orbper IS NOT NULL"""

BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

encoded_query = quote(ADQL)

url = f"{BASE_URL}?query={encoded_query}&format=csv"

response = requests.get(url)
response.raise_for_status()

with open("data/raw/exoplanets.csv", "w", encoding="utf-8") as f:
    f.write(response.text)



import urllib.request
import os
from datetime import datetime

def Download():
    URL = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2024&type=Mean"
    DateAndTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if not os.path.exists("./DataCSV"):
        os.makedirs("./DataCSV")

    for ProvinceID in range(1, 28):
        url = URL.format(ProvinceID)
        FileName = f"NOAA_ID{ProvinceID}_{DateAndTime}.csv"
        FilePath = os.path.join("./DataCSV", FileName)

        try:
            urllib.request.urlretrieve(url, FilePath)
        except Exception as e:
            print(f"Помилка при скачуванні файлу для ProvinceID {ProvinceID}: {str(e)}")

    print("Файли успішно скачано.")

if __name__ == "__main__":
    Download()
import os
import tempfile
import requests

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-{:02d}.parquet"


def download_files():
    paths = []
    for i in range(1, 13):
        url = BASE_URL.format(i)
        local_path = f"file{i:02d}.parquet"
        r = requests.get(url, stream=True, timeout=120)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        paths.append(local_path)
        print(f"Downloaded: {url} -> {local_path}")
    return paths

def main():
    files = download_files()

if __name__ == "__main__":
    main()
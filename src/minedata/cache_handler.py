import json
import os
from json import JSONDecodeError
from pathlib import Path
from typing import Literal

import requests

from minedata import MinedataConfig


def check_if_cache_exists(cache_path: str) -> bool:
    check = os.path.exists(os.path.join(MinedataConfig.CACHE_DIR, cache_path))
    if not check:
        return False
    with open(os.path.join(MinedataConfig.CACHE_DIR, cache_path), "r") as f:
        data = f.read()
        if not data:
            check = False
    return check

def fetch_and_cache_data(path: str, use_cache: bool, file_type: Literal["json", "yml"]) -> dict:
    cache_check = check_if_cache_exists(path)
    if cache_check and use_cache:
        try:
            cache_file_path = os.path.join(MinedataConfig.CACHE_DIR, path)
            with open(cache_file_path, "r") as f:
                text = f.read()
                if file_type == "json":
                    data = json.loads(text)
                else:
                    data = text
                if data:
                    return data
        except PermissionError as e:
            print(f"Permission error while reading cache: {e}")
        except JSONDecodeError as e:
            print(text)
            print(path)

    full_url = MinedataConfig.REPO_URL + path
    try:
        response = requests.get(full_url)
        if file_type != "json":
            data = response.text
        else:
            data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSONDecodeError while fetching from: {full_url}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
        raise

    try:
        cache_file_path = Path(os.path.join(MinedataConfig.CACHE_DIR, path))
        parent = cache_file_path.parent
        os.makedirs(parent, exist_ok=True)
        with open(cache_file_path, "w") as f:
            if file_type == "json":
                f.write(json.dumps(data, indent=4))
            else:
                f.write(data)
    except PermissionError as e:
        print(f"Permission error while writing cache: {e}")

    return data
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import requests

from minedata import MinedataConfig
from minedata.cache_handler import check_if_cache_exists, fetch_and_cache_data
from minedata.versions import Version


def get_data_paths_from_repo() -> Optional[dict, None]:
    """Fetches the data paths JSON from the repository."""
    try:
        response = requests.get(MinedataConfig.REPO_DATA_PATHS())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        raise f"Error fetching data paths JSON from {MinedataConfig.REPO_DATA_PATHS()}.\nPlease check your internet connection or the repository and try again."

def get_cached_data_paths_json() -> dict:
    """Reads the cached data paths JSON from the local cache file."""
    with open(MinedataConfig.CACHE_DATA_PATHS(), "r", encoding="utf-8") as f:
        return json.load(f)

def get_data_paths(use_cache: bool) -> dict:
    """Gets the data paths, either from the cache or by fetching from the repository if the cache is not available."""
    if use_cache:
        existing = check_if_cache_exists(MinedataConfig.CACHE_DATA_PATHS())
        if existing:
            return get_cached_data_paths_json()
    with ThreadPoolExecutor(max_workers=1) as executor:
        repo_data_paths = executor.submit(get_data_paths_from_repo)
        data_paths = get_cached_data_paths_json()
        repo_data_paths = repo_data_paths.result()

    if data_paths != repo_data_paths:
        with open(MinedataConfig.CACHE_DATA_PATHS(), "w", encoding="utf-8") as f:
            json.dump(get_data_paths_from_repo(), f, indent=4)
        data_paths = repo_data_paths

    return data_paths

def get_data_from_path(version: Version, use_cache: bool) -> dict:
    data_paths = get_data_paths(use_cache)

    edition_data_path = data_paths.get(version.edition)
    if not edition_data_path:
        raise ValueError(f"No data paths found for edition: {version.edition}")

    version_data = edition_data_path.get(version.minecraft_version)
    if not version_data:
        raise ValueError(
            f"No data found for Minecraft version: {version.minecraft_version} in edition: {version.edition}")
    data = {}
    with ThreadPoolExecutor() as executor:
        for key, value in version_data.items():
            if key != "proto":
                path = f"data/{value}/{key}.json"
                file_type = "json"
            else:
                path = f"data/{value}/{key}.yml"
                file_type = "yml"
            data[key] = executor.submit(fetch_and_cache_data, path, use_cache, file_type)
    for key in data:
        data[key] = data[key].result()
    return data


def get_data(version: Version, use_cache: bool=True) -> dict:
    """Gets the data for the specified Minecraft version, using the cache if available."""
    try:
        return get_data_from_path(version, use_cache)
    except Exception as e:
        raise Exception(f"Error getting data for version {version}: {e}")





if __name__ == "__main__":
    print(get_data_paths())
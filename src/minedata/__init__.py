import json
import os

from platformdirs import PlatformDirs

class MinedataConfig:
    REPO_URL = "https://raw.githubusercontent.com/RyanStudioo/minedata-minecraft-data/refs/heads/master/"

    dirs = PlatformDirs("minedata")
    CACHE_DIR = dirs.user_cache_dir
    os.makedirs(CACHE_DIR, exist_ok=True)

    @classmethod
    def REPO_DATA_FOLDER(cls) -> str:
        return cls.REPO_URL + "data/"

    @classmethod
    def REPO_DATA_PATHS(cls) -> str:
        return cls.REPO_DATA_FOLDER() + "dataPaths.json"

    @classmethod
    def CACHE_DATA_FOLDER(cls) -> str:
        os.makedirs(os.path.join(cls.CACHE_DIR, "data"), exist_ok=True)
        return os.path.join(cls.CACHE_DIR, "data")

    @classmethod
    def CACHE_DATA_PATHS(cls) -> str:
        file_path = os.path.join(cls.CACHE_DATA_FOLDER(), "dataPaths.json")
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(json.dumps({}))
        return file_path

from .data_handling import get_data
from .versions import Version, Versions

if __name__ == "__main__":
    print(MinedataConfig.CACHE_DIR)
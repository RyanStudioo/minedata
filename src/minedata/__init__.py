class MinedataConfig:
    REPO_URL = "https://github.com/RyanStudioo/minedata-minecraft-data/tree/master/"

    @classmethod
    def REPO_DATA_FOLDER(cls) -> str:
        return cls.REPO_URL + "data/"

    @classmethod
    def REPO_DATA_PATHS(cls) -> str:
        return cls.REPO_DATA_FOLDER() + "dataPaths.json"
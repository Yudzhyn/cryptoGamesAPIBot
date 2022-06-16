LOGGING: dict = {
    "DEV_ENV": False,
    "DEV": {
        "PATH": r"./logs_dev.log",
        "MESSAGE": "%(asctime)s %(levelname)s %(module)s - "
                   "%(funcName)s: %(message)s",
    },

    "PROD": {
        "PATH": r"./logs.log",
        "MESSAGE": "%(asctime)s | %(message)s"
    },
    "FILE_CSV_NAME": "bets.csv",
}

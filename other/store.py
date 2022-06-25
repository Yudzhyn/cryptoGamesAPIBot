# for working with csv files
import csv

# check file exists
from os.path import exists

# for typing
from typing import List, Dict, Any

# for logging
import logging

logger: logging.Logger = logging.getLogger(__name__)


class StoreCSV:
    __slots__ = ["__file_csv_name", "__file_csv", "__writer"]

    HEADERS: List[str] = ["DateTime", "Coin", "BetValue", "Result",
                          "BaseBet", "UnderOver", "Win/Loss", "Profit",
                          "ProfitSinceRun", "Payout", "Balance",
                          "Strategy", "Other", ]

    def __init__(self, file_name: str = "bets.csv"):
        self.__file_csv_name: str = file_name

        __file_exists = exists(file_name)
        self.__file_csv = open(self.__file_csv_name, "a", newline='')
        self.__writer = csv.DictWriter(self.__file_csv,
                                       delimiter=';',
                                       fieldnames=StoreCSV.HEADERS,
                                       extrasaction='ignore')

        if not __file_exists:
            self.__writer.writeheader()

    def write(self, data: Dict[str, Any]) -> None:
        self.__writer.writerow(data)

    def __del__(self):
        self.__file_csv.close()

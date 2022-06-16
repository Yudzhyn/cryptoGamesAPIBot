# for working with csv files
import csv

# data class
from dataclasses import dataclass

# check file exists
from os.path import exists

# for typing
from typing import List, Any

# for logging
import logging

logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class StoreBetData:
    datetime: str
    coin: str
    bet_value: str
    result: str
    base_bet: str
    under_over: str
    number_wins_losses: str
    profit: str
    payout: float
    balance: str
    strategy: str
    other: str = ""

    def to_list(self) -> List[Any]:
        return [self.datetime, self.coin,
                self.bet_value, self.result,
                self.base_bet,
                self.under_over, self.number_wins_losses,
                self.profit, self.payout,
                self.balance, self.strategy,
                self.other]

    @staticmethod
    def get_header() -> List[str]:
        return ["DateTime", "Coin",
                "BetValue",
                "Result", "BaseBet",
                "UnderOver", "Win/Loss",
                "Profit", "Payout",
                "Balance", "Strategy",
                "Other", ]


class StoreCSV:
    __slots__ = ["__file_csv_name", "__file_csv", "__writer"]

    def __init__(self, file_name: str = "bets.csv"):
        self.__file_csv_name: str = file_name

        __file_exists = exists(file_name)
        self.__file_csv = open(self.__file_csv_name, "a", newline='')
        self.__writer = csv.writer(self.__file_csv, delimiter=';')

        if not __file_exists:
            self.__writer.writerow(StoreBetData.get_header())

    def write(self, data: StoreBetData) -> None:
        self.__writer.writerow(data.to_list())

    def __del__(self):
        self.__file_csv.close()

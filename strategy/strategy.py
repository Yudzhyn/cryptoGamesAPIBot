import abc
from auto_bot.bet_data import BetData
from typing import List, Optional


class Strategy(abc.ABC):

    # [+] ----------------------------- init ----------------------------- [+]
    @abc.abstractmethod
    def init_bet_data(self, bet_data: BetData):
        """Initial parameters of bet data"""

    # [+] ----------------------------- lose ----------------------------- [+]
    @abc.abstractmethod
    def calculate_if_lose(self, bet_data: BetData):
        """Calculate parameters of bet data if lose"""

    # [+] ----------------------------- win ------------------------------ [+]
    @abc.abstractmethod
    def calculate_if_win(self, bet_data: BetData):
        """Calculate parameters of bet data if win"""

    # [+] ------------------------- represent ---------------------------- [+]
    @abc.abstractmethod
    def __repr__(self):
        """Calculate parameters of bet data if win"""

    @abc.abstractmethod
    def __str__(self):
        """Calculate parameters of bet data if win"""


class UnderOverState:
    __slots__ = ["__state", "__number_change", "__states", "__internal_counter"]

    def __init__(self, number_change: int = 2):
        self.__state: Optional[bool] = None
        self.__states: Optional[List[bool]] = None
        self.__number_change: int = number_change
        self.__internal_counter: int = 0

    def init_state(self, state) -> None:
        self.__state: bool = state
        self.__states: List[bool] = \
            [state] * self.__number_change + [not state] * self.__number_change

    def next_state(self) -> bool:
        if not (self.__state or self.__states):
            raise ValueError("The state isn't initialized.")

        _state = self.__states[self.__internal_counter]
        self.__internal_counter += 1
        if self.__internal_counter >= len(self.__states):
            self.__internal_counter = 0
        return _state

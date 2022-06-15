import abc
from auto_bot.bet_data import BetData


class Strategy(abc.ABC):

    @abc.abstractmethod
    def init_bet_data(self, bet_data: BetData):
        """Initial parameters of bet data"""

    @abc.abstractmethod
    def calculate_if_lose(self, bet_data: BetData):
        """Calculate parameters of bet data if lose"""

    @abc.abstractmethod
    def calculate_if_win(self, bet_data: BetData):
        """Calculate parameters of bet data if win"""

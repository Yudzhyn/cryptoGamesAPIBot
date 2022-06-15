from dataclasses import dataclass
from random import choice


@dataclass
class BetData:
    bet: float
    base_bet: float
    under_over: bool = choice([True, False])
    number_losses_from_last_win: int = 0
    number_wins_from_last_lose: int = 0
    win: bool = False
    profit: float = 0.0
    payout: float = 1.02
    balance: float = 0.0

    def __repr__(self):
        return f"{'WIN' if self.win else 'LOSE'}; " \
               f"BET = {self.bet:.8f}; " \
               f"UNDER_OVER = {self.under_over}; " \
               f"PAYOUT = {self.payout}; " \
               f"BALANCE = {self.balance:.8f}; " \
               f"W/L = {self.number_wins_from_last_lose}/{self.number_losses_from_last_win}; "

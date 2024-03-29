from dataclasses import dataclass
from random import choice
from other.calculates import disable_e_notation

from typing import Optional, Any, Dict


@dataclass
class BetData:
    bet: float
    base_bet: float
    coin: str
    strategy: str
    datetime: Optional[str] = None
    under_over: bool = choice([True, False])
    number_losses_from_last_win: int = 0
    number_wins_from_last_lose: int = 0
    totally_wins: int = 0
    totally_losses: int = 0
    win: bool = False
    profit: float = 0.0
    profit_since_run: float = 0.0
    payout: float = 1.02
    balance: float = 0.0
    goal_balance: float = 0.0
    other: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "DateTime": str(self.datetime)[:-4],
            "Coin": self.coin,
            "BetValue": disable_e_notation(self.bet),
            "Result": "WIN" if self.win else "LOSE",
            "BaseBet": disable_e_notation(self.base_bet),
            "UnderOver": "OVER" if self.under_over else "UNDER",
            "Win/Loss": f"{self.number_wins_from_last_lose}/{self.number_losses_from_last_win}",
            "TotallyWin/Loss": f"{self.totally_wins}/{self.totally_losses}",
            "Profit": disable_e_notation(self.profit),
            "ProfitSinceRun": disable_e_notation(self.profit_since_run),
            "Payout": self.payout,
            "Balance": disable_e_notation(self.balance),
            "GoalBalance": disable_e_notation(self.goal_balance),
            "Strategy": self.strategy,
            "Other": self.other,
        }

    def __repr__(self):
        return f"{'WIN' if self.win else 'LOSE'}; " \
               f"BET = {disable_e_notation(self.base_bet)}; " \
               f"UNDER_OVER = {self.under_over}; " \
               f"PAYOUT = {self.payout}; " \
               f"BALANCE = {disable_e_notation(self.balance)}; " \
               f"W/L = {self.number_wins_from_last_lose}/{self.number_losses_from_last_win}; "

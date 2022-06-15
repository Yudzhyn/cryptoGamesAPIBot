# balance, bet
from crypto_account import CryptoAccount
from auto_bot.bet_data import BetData

# delay
from time import sleep

# strategies
from strategy import Strategy

# for typing
from typing import Optional, Dict

# for logging
import logging

logger: logging.Logger = logging.getLogger(__name__)


class AutoBetBot:
    __slots__ = ["__account", "__start_balance", "__goal_balance",
                 "__profit_from_run", "__totally_wins",
                 "__totally_losses", "__bet_data", "__strategy"]

    def __init__(self, account: CryptoAccount,
                 base_bet: float,
                 strategy: Strategy) -> None:
        self.__account: CryptoAccount = account
        self.__start_balance: Optional[float] = self.__account.balance

        if not self.__start_balance:
            logger.error(f"[-] Can't get balance of account. Error: {self.__account.error}")
            raise ValueError("Can't get balance of account")

        self.__profit_from_run: float = 0
        self.__totally_wins: int = 0
        self.__totally_losses: int = 0

        self.__bet_data: BetData = BetData(
            bet=base_bet,
            base_bet=base_bet,
            balance=self.__start_balance
        )

        self.__strategy: Strategy = strategy
        self.__strategy.init_bet_data(self.__bet_data)
        logger.info(f"[+] Init auto bet bot. Account: {self.__account}. Strategy: {self.__strategy}")

    def __handle_data(self, result: dict) -> None:
        self.__bet_data.profit = result["Profit"]
        self.__bet_data.win = result["Profit"] > 0.0
        self.__bet_data.balance = result["Balance"]
        self.__profit_from_run = self.__bet_data.balance - self.__start_balance

        if self.__bet_data.win:
            self.__totally_wins += 1
            self.__bet_data.number_wins_from_last_lose += 1
            self.__bet_data.number_losses_from_last_win = 0
        else:
            self.__totally_losses += 1
            self.__bet_data.number_losses_from_last_win += 1
            self.__bet_data.number_wins_from_last_lose = 0

    def __calculate_feedback(self) -> None:
        if self.__bet_data.win:
            self.__strategy.calculate_if_win(self.__bet_data)
        else:
            self.__strategy.calculate_if_lose(self.__bet_data)

    def __bet_once(self) -> None:

        result_bet: Optional[Dict[str, str or float]] = \
            self.__account.bet(value=self.__bet_data.bet,
                               payout=self.__bet_data.payout,
                               under_over=self.__bet_data.under_over)

        if not result_bet:
            logger.warning("[-] The error arose during bet!")

        self.__handle_data(result_bet)
        self.__calculate_feedback()

    def __is_balance_correct(self, goal_balance: float) -> bool:
        if goal_balance != 0.0 and self.__bet_data.balance >= goal_balance:
            logger.info(f"[+] The balance achieved {goal_balance}.")
            return False

        if self.__bet_data.bet > self.__bet_data.balance:
            logger.info("[-] The bet is more than balance.")
            return False

        return True

    def run(self, goal_balance: float = 0.0, delay: float = 0.1) -> None:
        if not self.__is_balance_correct(goal_balance):
            logger.info(f"[-] Auto bet bot can't run. "
                        f"Goal balance '{goal_balance}'. Delay '{delay}'")
            return

        logger.info(f"[+] Auto bet bot run. Goal balance '{goal_balance}'. Delay '{delay}'")

        while True:
            if not self.__is_balance_correct(goal_balance):
                break
            self.__bet_once()
            sleep(delay)

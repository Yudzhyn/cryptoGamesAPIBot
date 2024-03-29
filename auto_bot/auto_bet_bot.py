# balance, bet
from crypto_account import CryptoAccount
from auto_bot.bet_data import BetData

# delay
from time import sleep

# for storing bets
from configs import LOGGING
from other.store import StoreCSV
from datetime import datetime

# strategies
from strategy import Strategy

# for typing
from typing import Optional, Dict, Any

# tmp output
from vision.console import ConsoleOutput

# for logging
from other.calculates import disable_e_notation
import logging

logger: logging.Logger = logging.getLogger(__name__)


class AutoBetBot:
    __slots__ = ["__account", "__start_balance", "__goal_balance",
                 "__profit_from_run", "__totally_wins",
                 "__totally_losses", "__bet_data", "__strategy",
                 "__storer_csv", "__output", "__goal_balance"]

    def __init__(self, account: CryptoAccount,
                 base_bet: float,
                 strategy: Strategy) -> None:
        self.__account: CryptoAccount = account
        self.__start_balance: Optional[float] = self.__account.balance

        if not self.__start_balance:
            logger.error(f"[-] Can't get balance of account. Error: {self.__account.error}")
            raise ValueError("Can't get balance of account")

        self.__storer_csv: StoreCSV = StoreCSV(LOGGING["FILE_CSV_NAME"])

        self.__bet_data: BetData = BetData(
            bet=base_bet,
            base_bet=base_bet,
            balance=self.__start_balance,
            coin=self.__account.coin,
            strategy=str(strategy)
        )

        self.__strategy: Strategy = strategy
        self.__strategy.init_bet_data(self.__bet_data)

        self.__output: ConsoleOutput = ConsoleOutput()
        logger.info(f"[+] Init auto bet bot. Account: {self.__account}. Strategy: {self.__strategy}")

    def __handle_data(self, result: dict) -> None:
        self.__bet_data.datetime = datetime.now()
        self.__bet_data.profit = result["Profit"]
        self.__bet_data.profit_since_run = self.__bet_data.balance - self.__start_balance
        self.__bet_data.win = result["Profit"] > 0.0
        self.__bet_data.balance = result["Balance"]

        if self.__bet_data.win:
            self.__bet_data.totally_wins += 1
            self.__bet_data.number_wins_from_last_lose += 1
            self.__bet_data.number_losses_from_last_win = 0
        else:
            self.__bet_data.totally_losses += 1
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

        bet_data_dict: Dict[str, Any] = self.__bet_data.to_dict()
        self.__storer_csv.write(bet_data_dict)
        self.__output.print_bet(bet_data_dict)

        self.__calculate_feedback()

    def __is_balance_correct(self) -> bool:
        if self.__bet_data.goal_balance != 0.0 and self.__bet_data.balance >= self.__bet_data.goal_balance:
            logger.info(f"[+] The balance achieved {disable_e_notation(self.__bet_data.goal_balance)}.")
            self.__output.print_congratulation(f"The balance achieved "
                                               f"{disable_e_notation(self.__bet_data.goal_balance)}.")
            return False

        if self.__bet_data.bet > self.__bet_data.balance:
            logger.info("[-] The bet is more than balance.")
            self.__output.print_warning("The bet is more than balance.")
            return False

        return True

    def run(self, goal_balance: float = 0.0, delay: float = 0.1) -> None:
        self.__bet_data.goal_balance = goal_balance

        if not self.__is_balance_correct():
            logger.info(f"[-] Auto bet bot can't run. "
                        f"Goal balance '{disable_e_notation(self.__bet_data.goal_balance)}'"
                        f". Delay '{delay}'")
            return

        logger.info(f"[+] Auto bet bot run. "
                    f"Goal balance '{disable_e_notation(self.__bet_data.goal_balance)}'. "
                    f"Delay '{delay}'")

        while True:
            if not self.__is_balance_correct():
                break
            self.__bet_once()
            sleep(delay)

import os

from typing import Dict, Any
from prettytable import PrettyTable


class ConsoleOutput:

    def __init__(self):
        ConsoleOutput.clear_console()

    @classmethod
    def clear_console(cls):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    @staticmethod
    def print_bet(data: Dict[str, Any]) -> None:
        ConsoleOutput.clear_console()
        bet_table = PrettyTable(["Bet", "Base Bet", "Payout", "Result", "Under Over", "Wins/Losses"])
        balance_table = PrettyTable(["Balance", "Goal Balance", "Profit", "Wins/Losses (Totally)"])
        bet_table.add_row([
            data["BetValue"],
            data["BaseBet"],
            data["Payout"],
            data["Result"],
            data["UnderOver"],
            data["Win/Loss"],
        ])
        balance_table.add_row([
            data["Balance"],
            data["GoalBalance"],
            data["ProfitSinceRun"],
            data["TotallyWin/Loss"],
        ])
        print(bet_table)
        print(balance_table)

    @staticmethod
    def print_warning(message: str) -> None:
        warning_table = PrettyTable(["!!! WARNING !!!"])
        warning_table.add_row([message])
        print(warning_table)

    @staticmethod
    def print_congratulation(message) -> None:
        congratulation_table = PrettyTable(["+++ CONGRATULATION +++"])
        congratulation_table.add_row([message])
        print(congratulation_table)

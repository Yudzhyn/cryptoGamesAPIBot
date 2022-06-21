import os

# from typing import Callable, Dict
from prettytable import PrettyTable


class ConsoleOutput:

    def __init__(self):
        ConsoleOutput.clear_console()

    @classmethod
    def clear_console(cls):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    @staticmethod
    def print(data) -> None:
        ConsoleOutput.clear_console()
        bet_table = PrettyTable(["Bet", "Base Bet", "Payout", "Result", "Under Over", "Wins/Losses"])
        balance_table = PrettyTable(["Balance", "Goal Balance", "Profit", "Wins/Losses (Totally)"])
        bet_table.add_row([
            f"{data['bet']:.8f}",
            f"{data['base_bet']:.8f}",
            data["payout"],
            "WIN" if data["win"] else "LOSE",
            "Over" if data["under_over"] else "Under",
            f"{data['number_wins_from_last_lose']}/{data['number_losses_from_last_win']}"
        ])
        balance_table.add_row([
            f"{data['balance']:.8f}",
            f"{data['goal_balance']:.8f}",
            f"{data['profit']:.8f}",
            f"{data['totally_wins']}/{data['totally_losses']}"
        ])
        print(bet_table)
        print(balance_table)

    @staticmethod
    def print_warning(message: str) -> None:
        warning_table = PrettyTable(["WARNING"])
        warning_table.add_row([message])

    @staticmethod
    def print_congratulation(message) -> None:
        congratulation_table = PrettyTable(["CONGRATULATION"])
        congratulation_table.add_row([message])

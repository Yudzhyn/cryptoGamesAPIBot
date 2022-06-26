def disable_e_notation(number: float, count: int = 8) -> str:
    return f"{number:.{count}f}"


def percentage(number: float, percent: float) -> float:
    return number * percent / 100 + number


def calc_win_profit(value: float, payout: float) -> float:
    return value * payout - value

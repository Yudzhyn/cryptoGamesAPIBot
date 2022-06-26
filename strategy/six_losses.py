from strategy.strategy import Strategy, UnderOverState
from auto_bot.bet_data import BetData
from other.calculates import percentage


class SixLossesStrategy(Strategy):

    def __init__(self, payout: float = 1.3026):
        self.__payout: float = payout
        self.__increase_coef_percent: int = 300
        self.__state = UnderOverState(2)

    # [+] ----------------------------- init ----------------------------- [+]
    def init_bet_data(self, bet_feedback: BetData) -> None:
        bet_feedback.payout = self.__payout

        # for alternate changing under and over
        self.__state.init_state(bet_feedback.under_over)
        bet_feedback.under_over = self.__state.next_state()

    # [+] ----------------------------- lose ----------------------------- [+]
    def calculate_if_lose(self, bet_feedback: BetData) -> None:
        bet_feedback.under_over = self.__state.next_state()
        if bet_feedback.number_losses_from_last_win >= 6:
            bet_feedback.bet = bet_feedback.base_bet
            bet_feedback.number_losses_from_last_win = 0
        else:
            bet_feedback.bet = percentage(bet_feedback.bet,
                                          self.__increase_coef_percent)

    # [+] ----------------------------- win ------------------------------ [+]
    def calculate_if_win(self, bet_feedback: BetData) -> None:
        bet_feedback.under_over = self.__state.next_state()
        bet_feedback.bet = bet_feedback.base_bet

    # [+] ------------------------- represent ---------------------------- [+]
    def __repr__(self) -> str:
        return "<SixLosses (payout='{}')>".format(
            self.__payout
        )

    def __str__(self) -> str:
        return "SixLosses"

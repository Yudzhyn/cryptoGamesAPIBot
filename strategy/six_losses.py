from strategy.strategy import Strategy, UnderOverState
from auto_bot.bet_data import BetData
from other.calculates import percentage


class SixLossesStrategy(Strategy):

    def __init__(self, payout: float = 1.3026):
        self.__payout: float = payout
        self.__increase_coef_percent: int = 300
        self.__state = UnderOverState(2)

    def init_bet_data(self, bet_feedback_data: BetData) -> None:
        bet_feedback_data.payout = self.__payout
        self.__state.init_state(bet_feedback_data.under_over)
        bet_feedback_data.under_over = self.__state.next_state()

    def calculate_if_lose(self, bet_feedback_data: BetData) -> None:
        bet_feedback_data.under_over = self.__state.next_state()
        if bet_feedback_data.number_losses_from_last_win >= 6:
            bet_feedback_data.bet = bet_feedback_data.base_bet
            bet_feedback_data.number_losses_from_last_win = 0
        else:
            bet_feedback_data.bet = percentage(bet_feedback_data.bet,
                                               self.__increase_coef_percent)

    def calculate_if_win(self, bet_feedback_data: BetData) -> None:
        bet_feedback_data.under_over = self.__state.next_state()
        bet_feedback_data.bet = bet_feedback_data.base_bet

    def __repr__(self) -> str:
        return "<SixLosses (payout='{}')>".format(
            self.__payout
        )

    def __str__(self) -> str:
        return "SixLosses"

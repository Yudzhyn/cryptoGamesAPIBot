from strategy.strategy import Strategy, UnderOverState
from auto_bot.bet_data import BetData
from other.calculates import calc_win_profit


class YuriStrategy(Strategy):

    def __init__(self,
                 payout_base: float = 1.25,
                 limit_base_payout_bet: int = 3,
                 coef_inc_start_bet: float = 4.0,
                 limit_min_number_wins: int = 4,
                 payout_max: float = 8.25,
                 payout_min: float = 4.25,
                 payout_coef_decrease: float = 6,
                 percent_win: float = 0.01,
                 step_change_bet: float = 0.01):
        self.payout_base: float = payout_base
        self.limit_base_payout_bet: int = limit_base_payout_bet
        self.coef_inc_start_bet: float = coef_inc_start_bet
        self.limit_min_number_wins: int = limit_min_number_wins
        self.percent_win: float = percent_win
        self.step_change_bet: float = step_change_bet
        self.payout_max: float = payout_max
        self.payout_min: float = payout_min
        self.payout_coef_decrease: float = payout_coef_decrease

        self.__state = UnderOverState(2)

        self.__sum_lose_bet: float = 0.0
        self.__counter_local_wins: int = 0

    def __calc_bet(self, bet: float, payout: float, base_bet: float) -> float:

        calc_bet: float = base_bet

        while True:
            profit: float = calc_win_profit(calc_bet, payout)

            if (profit - bet) / profit >= self.percent_win:
                return calc_bet

            calc_bet += base_bet * self.step_change_bet

    # [+] ----------------------------- init ----------------------------- [+]
    def init_bet_data(self, bet_feedback: BetData) -> None:
        bet_feedback.payout = self.payout_base
        bet_feedback.bet = bet_feedback.base_bet * self.coef_inc_start_bet

        # for alternate changing under and over
        self.__state.init_state(bet_feedback.under_over)
        bet_feedback.under_over = self.__state.next_state()

    # [+] ----------------------------- lose ----------------------------- [+]
    def calculate_if_lose(self, bet_feedback: BetData) -> None:

        bet_feedback.under_over = self.__state.next_state()

        if self.__counter_local_wins >= self.limit_min_number_wins:
            self.__counter_local_wins = 0
            return

        self.__sum_lose_bet += bet_feedback.bet

        if bet_feedback.number_losses_from_last_win < self.limit_base_payout_bet:
            bet_feedback.payout = self.payout_base
        elif bet_feedback.payout == self.payout_base:
            bet_feedback.payout = self.payout_max
        else:
            bet_feedback.payout = \
                bet_feedback.payout - (bet_feedback.payout - self.payout_min) / self.payout_coef_decrease
            bet_feedback.payout = round(bet_feedback.payout, 2)

        bet_feedback.bet = self.__calc_bet(self.__sum_lose_bet,
                                           bet_feedback.payout,
                                           bet_feedback.base_bet)

        self.__counter_local_wins = 0

    # [+] ----------------------------- win ------------------------------ [+]
    def calculate_if_win(self, bet_feedback: BetData) -> None:
        bet_feedback.under_over = self.__state.next_state()

        bet_feedback.bet = bet_feedback.base_bet * self.coef_inc_start_bet
        bet_feedback.payout = self.payout_base
        self.__sum_lose_bet = 0.0
        self.__counter_local_wins += 1

    # [+] ------------------------- represent ---------------------------- [+]
    def __repr__(self) -> str:
        return "<Yuri (payout_base='{}' coef_inc_start_bet='{}' " \
               "limit_min_number_wins='{}' payout_max='{}'" \
               "payout_min='{}' payout_coef_decrease='{}'" \
               "percent_win='{}' step_change_bet='{}')>".format(
            self.payout_base,
            self.coef_inc_start_bet,
            self.limit_min_number_wins,
            self.payout_max,
            self.payout_min,
            self.payout_coef_decrease,
            self.percent_win,
            self.step_change_bet,
        )

    def __str__(self) -> str:
        return "Yuri"

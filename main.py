import configs

# =============================================================================
# ------------------------------ LOGGING CONFIG -------------------------------
# =============================================================================
import logging

logger: logging.Logger = logging.getLogger()

LOGGING_CONFIGS: dict = configs.LOGGING["DEV"] \
    if configs.LOGGING["DEV_ENV"] else configs.LOGGING["PROD"]

LOGGING_LEVEL: int = logging.DEBUG \
    if configs.LOGGING["DEV_ENV"] else logging.INFO

logging.basicConfig(filename=LOGGING_CONFIGS["PATH"],
                    level=LOGGING_LEVEL,
                    format=LOGGING_CONFIGS["MESSAGE"],
                    datefmt='%d-%m %H:%M:%S')

# =============================================================================
# ------------------------------- MAIN FUNCTION -------------------------------
# =============================================================================

if __name__ == "__main__":
    logger.info("[!] --------------------------------------- [!]")
    from crypto_account import CryptoAccount
    from auto_bot.auto_bet_bot import AutoBetBot
    from api_token import API_TOKEN
    from strategy import Strategy, SixLossesStrategy

    crypto_account: CryptoAccount = CryptoAccount(API_TOKEN, "BCH")
    strategy: Strategy = SixLossesStrategy()
    auto_bet_bch = AutoBetBot(account=crypto_account,
                              base_bet=0.00000100,
                              strategy=strategy)
    auto_bet_bch.run(goal_balance=0.000427000)

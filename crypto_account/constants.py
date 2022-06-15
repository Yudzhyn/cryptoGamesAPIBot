URL_BASE: str = "https://api.crypto.games/"

URL_FULL: dict = {
    "balance": {
        "method": "GET",
        "url":
            lambda coin, key: URL_BASE + f"v1/balance/{coin}/{key}",
        "content": ["Balance"],
    },

    "nextseed": {
        "method": "GET",
        "url":
            lambda coin, key: URL_BASE + f"v1/nextseed/{coin}/{key}",
        "content": ["NextServerSeedHash"],
    },

    "bet": {
        "method": "POST",
        "url":
            lambda coin, key: URL_BASE + f"v1/placebet/{coin}/{key}",
        "content": [
            "BetId", "Roll", "Target",
            "Profit", "Payout", "Balance",
        ]
    }

}

COIN_AVAILABLE_LIST: tuple = (
    "BTC", "ETH", "LTC",
    "SOL", "DGC", "MNR",
    "ETC", "DASH", "GAS",
    "BCH",
)

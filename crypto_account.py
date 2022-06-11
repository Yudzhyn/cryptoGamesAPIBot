# for send request to site
from requests import request
from requests.models import Response, ConnectionError

# for converting from json to dict
from json import loads as json_loads

# for creating hex string custom length
from secrets import token_hex

# urls addresses for http requests,
# list of available coins
from constants import URL_FULL as URLS, COIN_AVAILABLE_LIST

# custom errors
from enums import CryptoAccountError

# for typing
from typing import Dict, Callable, Optional, List

# for logging
import logging

logger: logging.Logger = logging.getLogger(__name__)


class CryptoAccount:
    __slots__ = ["__key_api", "coin", "error"]

    def __init__(self, key_api: str, coin: str) -> None:
        self.__key_api: str = key_api
        if coin in COIN_AVAILABLE_LIST:
            self.coin = coin
        else:
            logger.info(f"[-] Don't init crypto account. Coin {coin} is not available.")
            raise ValueError(f"Crypto Games don't support coin '{coin}'")

        logger.info(f"[+] Init crypto account. Coin: {coin}")

        self.error: Optional[CryptoAccountError] = None

    def __request(self, request_params: dict, data: Optional[dict] = None) -> Optional[dict]:

        url: str = request_params["url"]
        method: str = request_params["method"]

        try:
            response: Response = request(method, url=url, json=data)

            if response.status_code == 200:
                return json_loads(response.text)
            elif response.status_code == 422:
                self.error = CryptoAccountError.INVALID_INPUT_PARAMETERS
                logger.info(f"[-] Invalid input parameters for request. Data: {data}")
            else:
                self.error = CryptoAccountError.UNKNOWN_ERROR
                logger.info(f"[-] Unknown error. Status code: {response.status_code}")

        except ConnectionError:
            self.error = CryptoAccountError.CONNECTION_ERROR
            logger.info(f"[-] Connection error.")

    def __template_get_request(self, get_request_name: str) -> Optional[str]:
        request_params: Dict[str, str or Callable] = URLS[get_request_name].copy()
        request_params["url"] = request_params["url"](self.coin, self.__key_api)

        response: Optional[Dict[str, str or list]] = \
            self.__request(request_params)

        if response:
            content_key: str = request_params["content"][0]
            return response[content_key]

    def next_server_seed(self) -> Optional[str]:
        next_seed: Optional[str] = self.__template_get_request("nextseed")
        if next_seed:
            return next_seed

    @property
    def balance(self) -> Optional[float]:
        balance: Optional[str] = self.__template_get_request("balance")
        if balance:
            return float(balance)

    def bet(self, value: float, payout: float, under_over: bool) -> Optional[Dict]:

        request_params: Dict[str, str or Callable] = URLS["bet"].copy()

        request_params["url"] = \
            request_params["url"](self.coin, self.__key_api)

        client_seed_hash: str = token_hex(15)

        request_data: Dict[str, str] = {
            "Bet": value,
            "Payout": payout,
            "UnderOver": under_over,
            "ClientSeed": client_seed_hash
        }

        response: Optional[Dict[str, float or list]] = \
            self.__request(request_params, request_data)

        if response:
            content_keys: List[str] = request_params["content"]
            return {key: response[key] for key in content_keys} if response else None

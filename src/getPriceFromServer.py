#!/usr/bin/env python3
import requests


def getPriceFromServer(coinName: str, currencyName: str, kindName: str):
    """
    getPriceFromServer: get current price from a specific server.

    Input:
        coinName: str, a string for the name of coin you want to get the price
        currencyName: str, a string for the price currency
        kindName: str, a string for the price type

    Output:
        price: float, the price you query; false when error pops
    """
    try:
        price = float(requests.get(f'https://api.coinbase.com/v2/prices/{coinName}-{currencyName}/{kindName}').json()['data']['amount'])
        return price
    except:
        print("Error getting price for: {}".format(coinName))
        return False


if __name__ == '__main__':
    coinName = "BTC"
    currencyName = "USD"
    kindName = "buy"
    priceNow = getPriceFromServer(coinName, currencyName, kindName)
    print("Coin name: ", coinName)
    print("Currency name: ", currencyName)
    print("Price kind: ", kindName)
    print("Price now: ", priceNow)

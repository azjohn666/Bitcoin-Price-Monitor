#!/usr/bin/env python3
import os
import sys
sys.path.append(os.getcwd() + '/src')
import asyncio
from Monitor import Monitor


if __name__ == "__main__":
    # initialize a Monitor
    timeInterval = 5  # unit: second
    MyMonitor = Monitor(timeInterval)

    # inputs
    coinName = "BTC"
    currencyName = "USD"
    kindName = "buy"

    # run the monitor
    MyMonitor.run(coinName, currencyName, kindName)

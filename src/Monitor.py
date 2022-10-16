#!/usr/bin/env python3
import os
import sys
sys.path.append(os.getcwd() + '/src')
import time
import requests
import asyncio
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from getPriceFromServer import getPriceFromServer


class Monitor:
    timeInterval: float  # the time interval [sec] for updating data

    def __init__(self, timeInterval: float):
        """
        Constructor: Initialize an instance of Monitor.

        Input:
            timeInterval: float, the time interval [sec] for updating data
        """
        self.timeInterval = timeInterval

    def run(self, coinName: str, currencyName: str, kindName: str):
        """
        run: run the real-time price monitor. This is the main function entry point.

        Input:
            coinName: str, the name of coin you're concerned
            currencyName: str, the name of currency you're concerned
            kindName: str, the name of the price type, "buy" or "sell"
        """
        count = 0
        self.createRealtimeFig()
        self.priceList = np.array([])
        while count < 10:
        # while True:
            asyncio.run(self.doOnce(coinName, currencyName, kindName))
            # count = count + 1
            count += 1

    async def doOnce(self, coinName: str, currencyName: str, kindName: str):
        """
        doOnce: get the real-time price once, and the frequency is set to a certain value

        Input:
            coinName: str, the name of coin you're concerned
            currencyName: str, the name of currency you're concerned
            kindName: str, the name of the price type, "buy" or "sell"
        """
        t0 = time.time()
        self.updateRealtimeFig()
        plt.pause(1E-6)
        price = getPriceFromServer(coinName, currencyName, kindName)
        print(datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
        print(coinName + " price: " + str(price))
        self.priceList = np.append(self.priceList, price)
        t1 = time.time()
        await asyncio.sleep(max(self.timeInterval - (t1 - t0), 0))

    def createRealtimeFig(self):
        """
        createRealtimeFig: create a figure for real-time data visualization
        """
        # initilize an empty figure
        _, self.ax = plt.subplots(1, 1, figsize=(12, 10))
        plt.ion()
        plt.show()
        # figure settings
        self.figureSetting()
        plt.legend(self.handles, self.labels,
            bbox_to_anchor=(1,1), loc="upper right", framealpha=0.5)

    def updateRealtimeFig(self):
        """
        updateRealtimeFig: update the current figure once
        """
        # clear the current figure
        self.ax.clear()
        idxList = np.arange(self.priceList.shape[0])
        self.ax.plot(idxList, self.priceList, color="blue")
        # plot legends
        self.figureSetting()
        plt.legend(self.handles, self.labels,
            bbox_to_anchor=(1,1), loc="upper right", framealpha=0.5)

    def figureSetting(self):
        """
        figureSetting: set up the figure for current axis
        """
        # add labels on x and y axes of the figure
        self.ax.set_xlabel("time")
        self.ax.set_ylabel("Price [USD]")
        # set legends
        color = ["blue"]
        marker_list = ["None"]
        self.labels = ["BTC-USD"]
        f = lambda m,c: plt.plot([], [], marker=m, color=c, ls="None")[0]
        self.handles = [f(marker_list[i], color[i])
            for i in range(len(self.labels))]


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

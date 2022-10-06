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
    def __init__(self, timeInterval):
        """
        Constructor:
        """
        self.timeInterval = timeInterval

    def run(self, coinName: str, currencyName: str, kindName: str):
        """
        run:
        """
        count = 0
        self.createRealtimeFig()
        self.priceList = np.array([])
        while count < 10:
        # while True:
            asyncio.run(self.doOnce(coinName, currencyName, kindName))

    async def doOnce(self, coinName: str, currencyName: str, kindName: str):
        """
        doOnce:
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
        createRealtimeFig: 
        """
        _, self.ax = plt.subplots(1, 1, figsize=(12, 10))
        plt.ion()
        plt.show()
        # figure settings
        self.figureSetting()
        plt.legend(self.handles, self.labels,
            bbox_to_anchor=(1,1), loc="upper right", framealpha=0.5)

    def updateRealtimeFig(self):
        """
        updateRealtimeFig
        """
        self.ax.clear()
        idxList = np.arange(self.priceList.shape[0])
        self.ax.plot(idxList, self.priceList, color="blue")
        # plot legends
        self.figureSetting()
        plt.legend(self.handles, self.labels,
            bbox_to_anchor=(1,1), loc="upper right", framealpha=0.5)

    def figureSetting(self):
        """
        figureSetting:
        """
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

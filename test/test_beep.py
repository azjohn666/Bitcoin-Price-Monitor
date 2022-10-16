#!/usr/bin/env python3
import os
import sys
sys.path.append(os.getcwd() + '/src')
import winsound

if __name__ == "__main__":
    # set frequency to 1000 Hz
    freq = 1000
    # set beep duration to 2000 milliseconds
    duration = 5000
    # beep
    winsound.Beep(freq, duration)
    print("check this point")

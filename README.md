# 50-50

An asyncronous day trading script written in Python 3.

The script connects to the Interactive Brokers API and updates asyncronously in real time via two event handlers. 

The event handlers update a pandas dataframe which is continously looped over in search of patterns.

This script can trade real money, so be careful.



from ib_insync import *
import pandas as pd
import pandas_ta as ta
import nest_asyncio
import random
import datetime
from datetime import timezone
import json
import math
from statistics import mean
from statistics import median
import winsound
import traceback


# pnl_profit = pnl_profit(pnl_profit=False) #pickle as an object
# pnl_profit_dump = pickle.dumps(pnl_profit)

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)
nest_asyncio.apply()  # patch for asyncio to stop a loop error when trying to ib.sleep

# # calculate win rate
# completed_trades = ib.trades()
# trade_list = []
# for trade in completed_trades:
#     if trade.orderStatus.status == "Filled":  # make sure orders were filled and not cancelled
#         price = 0
#         qty = 0
#         for fill in trade.fills:  # calculate average_price
#             price += fill.execution.price * fill.execution.shares
#             qty += fill.execution.shares
#         avg_price = round(price / qty, 2)
#         trade_list.append({"symbol": trade.contract.symbol, "action": trade.order.action, "qty": qty, "price": avg_price, "time": trade.log[0].time})
#
# # trade_list = sorted(trade_list, key=lambda d: d['time'])  # sort the list based on time
# trade_list = sorted(trade_list, key=lambda d: (d['symbol'], d['time']))  # sort the list by symbol and time
# print(len(trade_list))
# win = 0
# loss = 0
# close_date = datetime.datetime.now(timezone.utc)
# for idx, trade in enumerate(trade_list):
#     try:
#         if trade["symbol"] == trade_list[idx + 1]["symbol"] and trade["time"] != close_date:
#             close_date = trade_list[idx + 1]["time"]  # set time of closing trade so we don't look at it again
#             if trade["action"] == "BUY":
#                 if trade["price"] < trade_list[idx + 1]["price"]:
#                     win += 1
#                 else:
#                     loss += 1
#             if trade["action"] == "SELL":
#                 if trade["price"] > trade_list[idx + 1]["price"]:
#                     win += 1
#                 else:
#                     loss += 1
#     except:
#         pass  # out of bounds
# print("win :", win, "loss :", loss)
# ib.disconnect()
# quit(0)

while True:
    time = datetime.datetime.now()
    if time.hour == 8:
        if time.minute >= 25:
            break
    else:
        break
    ib.sleep(3)
    print("waiting for 8:25")
# print("waiting for 8:30 is disabled")
def place_oca_orders(contract, order1, order2):
    orders = [order1, order2]
    oca = str(random.randint(100000000, 99999999999))
    orders = ib.oneCancelsAll(orders, oca, 1)
    print(orders)
    # ib.sleep(0)
    ib.placeOrder(contract, orders[0])
    print("order 1 submitted")
    ib.sleep(0)
    ib.placeOrder(contract, orders[1])
    print("order 2 submitted")
    # for order in orders:
    #     print("here")
    #     print(order)
    #     submitted_order = ib.placeOrder(contract, order)
    #     # ib.sleep(0)
    #     print(submitted_order)

    # ib.placeOrder(contract, order2)
    # ib.sleep(0)

    # if order_type == "open":
    # #     # order1 = StopOrder(desired_orders.action[0], desired_orders.totalQuantity[0], desired_orders.price[0])  #follow through
    # #     # order2 = StopOrder(desired_orders.action[1], desired_orders.totalQuantity[1], desired_orders.price[1])  #follow through
    # #     order1 = LimitOrder(desired_orders.action[0], desired_orders.totalQuantity[0], desired_orders.price[0])  # reversal
    # #     order2 = LimitOrder(desired_orders.action[1], desired_orders.totalQuantity[1], desired_orders.price[1])  # reversal
    # # elif order_type == "close":
    # #     order1 = StopOrder(desired_orders.action[0], desired_orders.totalQuantity[0], desired_orders.price[0])  # fixed stop order
    # #     ''' # trailing stop loss order
    # #     order1 = Order()
    # #     order1.action = desired_orders.action[0]
    # #     order1.orderType = "TRAIL"
    # #     order1.totalQuantity = desired_orders.totalQuantity[0]
    # #     order1.trailingPercent = trailingPercent
    # #     order1.trailStopPrice = desired_orders.price[0]
    # #     '''  # end trailing stop order
    # #
    # #     order2 = LimitOrder(desired_orders.action[1], desired_orders.totalQuantity[1], desired_orders.price[1])  # fixed limit order
    # orders = [order1, order2]
    # oca = str(random.randint(100000000, 99999999999))
    # ib.oneCancelsAll(orders, oca, 1)
    # if order_type == "open":
    #     ib.placeOrder(contract, order1)
    #     # cprint(order1)
    #     ib.sleep(0)
    #     ib.placeOrder(contract, order2)
    #     # cprint(order2)
    # elif order_type == "close":
    #     ib.placeOrder(contract, order1)
    #     # cprint(order1)
    #     ib.sleep(0)
    #     ib.placeOrder(contract, order2)
    #     # cprint(order2)
    # else:
    #     # cprint("it's too late to open new orders")
    #     # cprint("cancelling realtime subscription for " + bars.contract.localSymbol)
    #     pass
    #     # ib.cancelHistoricalData(bars)
    # # nest_asyncio.apply(ib.sleep(1))

def log(log_string):
    print(log_string)
    path = "json/" + "log.json"
    with open(path, 'r') as openfile:
        original_string = json.load(openfile)

    if log_string == "clearing log":
        new_string = ""
    else:
        new_string = original_string + '  -----  ' + log_string

    with open(path, 'w') as file_object:
        json.dump(new_string, file_object)

def close_position(percent):  # closes all positions
    # cancel all pending orders
    if len(ib.openOrders()) > 0:
        for order in ib.openOrders():
            ib.cancelOrder(order)
            ib.sleep(0)
            print("cancelling: " + order)
    # close all postions
    pos = util.df(ib.positions())
    if len(pos) > 0:
        for q in pos.index:
            if 'SPY' == getattr(pos.contract[q], 'symbol'):
                continue
            if 'SPY' != getattr(pos.contract[q],'symbol'):  # send order to close position # but don't close SPY or other long term investments
                if pos.position[q] > 0:
                    direction = 'SELL'
                else:
                    direction = 'BUY'
                contract = pos.contract[q]
                contract.exchange = 'SMART'  # set exchange to smart to prevent errors
                market_order = MarketOrder(direction, round(abs(pos.position[q]) * percent))
                ib.placeOrder(contract, market_order)
                ib.sleep(0)
                print("closing open positions for " + contract.symbol)


def close_single_position(closing_symbol):
    pos = util.df(ib.positions())
    if len(ib.openOrders()) > 0:  # cancel all pending orders
        for order in ib.openOrders():  # this closes all open orders
            ib.cancelOrder(order)
            ib.sleep(0)
    if len(pos) > 0:
        for q in pos.index:
            if 'SPY' == getattr(pos.contract[q], 'symbol'):
                continue
            if 'SPY' != getattr(pos.contract[q],
                                'symbol'):  # send order to close position # but don't close SPY or other long term investments
                if pos.position[q] > 0:
                    direction = 'SELL'
                else:
                    direction = 'BUY'
                contract = pos.contract[q]
                if contract.symbol == closing_symbol:
                    contract.exchange = 'SMART'  # set exchange to smart to prevent errors
                    market_order = MarketOrder(direction, abs(pos.position[q]))
                    ib.placeOrder(contract, market_order)
                    ib.sleep(0)


def change_order(orderId, price, contract):
    order = next((o for o in ib.openOrders() if o.orderId == orderId), None)
    if order:
        if order.orderType == "LMT":
            order.lmtPrice = price
        else:
            order.auxPrice = price
        ib.placeOrder(contract, order)
    # ib.sleep(0)


def place_single_order(desired_orders, contract, order_type):
    if order_type == "open":
        order1 = StopOrder(desired_orders.action[0], desired_orders.totalQuantity[0], desired_orders.price[0])
        ib.placeOrder(contract, order1)
        ib.sleep(0)
    if order_type == "close":
        order1 = StopOrder(desired_orders.action[0], desired_orders.totalQuantity[0], desired_orders.price[0])
        ib.placeOrder(contract, order1)
        ib.sleep(0)


def place_stop_order(action, qty, price):
    stop_order = StopOrder(action, qty, price)
    ib.placeOrder(contract, stop_order)
    ib.sleep(0)


def cancel_single_order(order):
    ib.cancelOrder(order)
    print("Order Id: " + str(order.orderId) + " cancelled")


def place_orders(desired_orders, contract, order_type, bars=0, trailingPercent=0):
    if order_type == "open":
        # order1 = StopOrder(desired_orders.action[0], desired_orders.totalQuantity[0], desired_orders.price[0])  #follow through
        # order2 = StopOrder(desired_orders.action[1], desired_orders.totalQuantity[1], desired_orders.price[1])  #follow through
        order1 = LimitOrder(desired_orders.action[0], desired_orders.totalQuantity[0],
                            desired_orders.price[0])  # reversal
        order2 = LimitOrder(desired_orders.action[1], desired_orders.totalQuantity[1],
                            desired_orders.price[1])  # reversal
    elif order_type == "close":
        order1 = StopOrder(desired_orders.action[0], desired_orders.totalQuantity[0],
                           desired_orders.price[0])  # fixed stop order
        ''' # trailing stop loss order
        order1 = Order()
        order1.action = desired_orders.action[0]
        order1.orderType = "TRAIL"
        order1.totalQuantity = desired_orders.totalQuantity[0]
        order1.trailingPercent = trailingPercent
        order1.trailStopPrice = desired_orders.price[0]
        '''  # end trailing stop order

        order2 = LimitOrder(desired_orders.action[1], desired_orders.totalQuantity[1],
                            desired_orders.price[1])  # fixed limit order
    orders = [order1, order2]
    oca = str(random.randint(100000000, 99999999999))
    ib.oneCancelsAll(orders, oca, 1)
    if order_type == "open":
        ib.placeOrder(contract, order1)
        # cprint(order1)
        ib.sleep(0)
        ib.placeOrder(contract, order2)
        # cprint(order2)
    elif order_type == "close":
        ib.placeOrder(contract, order1)
        # cprint(order1)
        ib.sleep(0)
        ib.placeOrder(contract, order2)
        # cprint(order2)
    else:
        # cprint("it's too late to open new orders")
        # cprint("cancelling realtime subscription for " + bars.contract.localSymbol)
        pass
        # ib.cancelHistoricalData(bars)
    # nest_asyncio.apply(ib.sleep(1))


def First_trade(symbol):  # returns boolean
    path = "json/" + "check_trade" + symbol + ".json"
    with open(path, 'r') as openfile:
        string = json.load(openfile)
    if string == "True":  # switching from string to boolean
        return True
    elif string == "False":
        return False


def set_first_trade(symbol):
    path = "json/" + "check_trade" + symbol + ".json"
    string = "True"
    with open(path, 'w') as file_object:  # open the file in write mode
        json.dump(string, file_object)


def record_direction(symbol, direction):
    path = "json/" + "direction" + symbol + ".json"
    string = str(direction)
    with open(path, 'w') as file_object:  # open the file in write mode
        json.dump(string, file_object)


def calculate_direction(symbols):  # symbols == symbols_direction
    total_symbols = len(symbols)
    sum = 0
    for symbol in symbols:
        path = "json/" + "direction" + symbol + ".json"
        with open(path, 'r') as openfile:
            string = json.load(openfile)
        if string == "1":  # switching from string to boolean
            sum += 1
        elif string == "-1":
            sum += -1
    percentage = round(sum / total_symbols, 2)
    return percentage


def record_time(hour, minute, second, percentage):
    path = "json/" + "record_percent.json"
    with open(path, 'r') as openfile:
        list = json.load(openfile)
    list.append(str(hour) + ":" + str(minute) + ":" + str(second) + " " + str(percentage))
    with open(path, 'w') as file_object:  # open the file in write mode
        json.dump(list, file_object)


# def onBarUpdate(bars: BarDataList, has_new_bar: bool):
#     contract = bars.contract
#     symbol = bars.contract.symbol
#     data = bars
#     # cprint(symbol)
#     # print(util.df(ib.portfolio()))
#     for symbol_x in symbols_atr:
#         if symbol == symbol_x[0]:
#             atr = symbol_x[1]
#
#     # atr = round(atr*2,2)
#
#     qty = int(round(risk / atr, 0))
#
#     '''
#     market_order = MarketOrder('BUY', qty)
#     trade = ib.placeOrder(contract, market_order)
#     ib.disconnect()
#     quit(0)
#     '''
#     # if has_new_bar == True:
#     df = util.df(data)
#     # print(df)
#     # sma = df.close.tail(50).mean()
#     # std_dev = df.close.tail(50).std() * 3
#     close = df.close.iloc[-1]
#     high = df.high.iloc[-1]
#     low = df.low.iloc[-1]
#     high_last_bar = 0  # blocks orders from sending until we're ready
#     low_last_bar = 99999999999999  # blocks orders from sending until we're ready
#     if len(df) > 1:  # the loop is spinning, but we're still waiting for data to arrive
#         high_last_bar = df.high.iloc[-2]
#         low_last_bar = df.low.iloc[-2]
#     open = df.open.iloc[-1]
#     pos = util.df(ib.positions())
#     # print(open_orders.to_string())
#     # print(high_last_bar)
#     # print(pos)
#
#     # Lets calculate PNL for our algo positions and exclude long term investments
#     pnl_acc_unrealized = round(getattr(pnl_account, 'unrealizedPnL'), 2)
#     pnl_acc_realized = round(getattr(pnl_account, 'realizedPnL'), 2)
#     pnl_spy_unrealized = round(getattr(pnl_SPY, 'unrealizedPnL'), 2)
#     pnl_spy_realized = round(getattr(pnl_SPY, 'realizedPnL'), 2)
#     # pnl = round((pnl_acc_unrealized+pnl_acc_realized) - (pnl_spy_unrealized+pnl_spy_realized),2)
#     # pnl = round((pnl_acc_unrealized + pnl_acc_realized) - pnl_spy_unrealized, 2)
#
#     pnl_acc_pnl = 0
#     pnl_spy_pnl = 0
#     if pd.isna(pnl_acc_unrealized) != True:  # check to make sure not nan
#         pnl_acc_pnl += pnl_acc_unrealized
#     if pd.isna(pnl_acc_realized) != True:
#         pnl_acc_pnl += pnl_acc_realized
#     if pd.isna(pnl_spy_unrealized) != True:
#         pnl_spy_pnl += pnl_spy_unrealized
#     pnl = round(pnl_acc_pnl - pnl_spy_pnl, 2)
#
#     if symbol == super_symbol:  # limit printing pnl
#         print(pnl)
#
#     # Lets get open orders and access them as a dataclass instead of an object
#     open_orders = ib.openTrades()
#     # print(open_orders)
#     orders = [ord.order for ord in open_orders]
#     orders = util.df(orders)
#     contracts = [con.contract for con in open_orders]
#     contracts = util.df(contracts)
#     orders_status = [stat.orderStatus for stat in open_orders]
#     orders_status = util.df(orders_status)
#     trailingPercent = 0
#
#     if len(open_orders) > 0:
#         open_orders = pd.concat([orders, contracts, orders_status], axis=1)  # combine dataframes into one
#         open_orders = open_orders.loc[:, ~open_orders.columns.duplicated()].copy()  # remove duplicate columns to prevent errors
#         for i in open_orders.index:
#             if open_orders.symbol[i] != symbol:
#                 open_orders = open_orders.drop([i])  # drop orders not related to the current symbol
#         # print(open_orders)
#         open_orders.reset_index(drop=True, inplace=True)  # reindex the dataframe after dropping rows
#         # open_orders = open_orders.reindex(range(len(open_orders))) # reindex the dataframe after dropping rows
#     # print(open_orders)
#
#     if pnl >= 99999:  # changed # check if we should close for a profit
#         if symbol == super_symbol:
#             close_all = close_position(pos, symbol, contract, open_orders)
#
#     x = datetime.datetime.now()
#     if x.hour == 14 and x.minute >= 55 and symbol == super_symbol:  # close remaining orders at the end of the day // use local time
#         close_all = close_position(pos, symbol, contract, open_orders)
#
#     desired_orders = []
#     order_type = "none"
#     # Check if we are in a trade
#     if contract not in [i.contract for i in ib.positions()]:
#         # print(contract)
#         # We are not in a trade - Look for a signal
#         # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP','price': round(low + atr/2,2), 'totalQuantity': qty, 'action': 'BUY'}) #round(low + atr/2,2)
#         # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(high - atr/2,2), 'totalQuantity': qty, 'action': 'SELL'})
#         # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(high_last_bar, 2),'totalQuantity': qty, 'action': 'BUY'}) #follow through  # round(low + atr/2,2)
#         # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(low_last_bar, 2),'totalQuantity': qty, 'action': 'SELL'}) #follow through
#         desired_orders.append(
#             {'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(high_last_bar, 2),
#              'totalQuantity': qty, 'action': 'SELL'})  # reversal
#         desired_orders.append(
#             {'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(low_last_bar, 2),
#              'totalQuantity': qty, 'action': 'BUY'})  # reversal
#         order_type = "open"
#         # print(desired_orders)
#         ''' we don't need to modify since we are trying for the opening range break
#         # Check if we need to modify orders
#         desired_orders_df = util.df(desired_orders)
#         if len(open_orders)>0:
#             for i in open_orders.index:
#                 for e in desired_orders_df.index:
#                     if open_orders.symbol[i] == desired_orders_df.symbol[e] and open_orders.orderType[i] == desired_orders_df.orderType[e] and open_orders.action[i] == desired_orders_df.action[e]:
#                         if open_orders.auxPrice[i] != desired_orders_df.price[e]:
#                             #print(open_orders.orderId[i],open_orders.auxPrice[i],desired_orders_df.price[e])
#                             #cprint("changing an order price")
#                             change_order(open_orders.orderId[i],desired_orders_df.price[e],contract)
#         '''
#
#     elif contract in [i.contract for i in ib.positions()]:
#         # We are in a trade
#         idx = pos.loc[pos['contract'] == contract].index[0]  # locate index of the contract
#         current_qty = pos.position[idx]
#         avgCost = round(pos.avgCost[idx], 2)
#         trailingPercent = ((atr / 2) / close) * 100
#         if current_qty > 0:
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(high - atr / 2, 2),'totalQuantity': abs(current_qty)*1, 'action': 'SELL'})
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(low + atr, 2),'totalQuantity': abs(current_qty), 'action': 'SELL'}) #round(low + atr, 2)
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(avgCost - (atr/2), 2),'totalQuantity': abs(current_qty)*1, 'action': 'SELL'}) #follow through
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(avgCost + (atr), 2),'totalQuantity': abs(current_qty), 'action': 'SELL'}) #follow through
#             desired_orders.append(
#                 {'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(avgCost - (atr * 3), 2),
#                  'totalQuantity': abs(current_qty) * 1, 'action': 'SELL'})  # reversal
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(avgCost + (atr/2), 2),'totalQuantity': abs(current_qty), 'action': 'SELL'}) #reversal
#             desired_orders.append(
#                 {'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(low + (atr / 2), 2),
#                  'totalQuantity': abs(current_qty), 'action': 'SELL'})  # reversal with trailing limit order
#
#         elif current_qty < 0:
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(low + atr / 2, 2),'totalQuantity': abs(current_qty)*1, 'action': 'BUY'})
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(high - atr, 2),'totalQuantity': abs(current_qty), 'action': 'BUY'})
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(avgCost + (atr/2), 2),'totalQuantity': abs(current_qty)*1, 'action': 'BUY'}) #follow through
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(avgCost - (atr), 2),'totalQuantity': abs(current_qty), 'action': 'BUY'}) #follow through
#             desired_orders.append(
#                 {'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(avgCost + (atr * 3), 2),
#                  'totalQuantity': abs(current_qty) * 1, 'action': 'BUY'})  # reversal
#             # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(avgCost - (atr/2), 2),'totalQuantity': abs(current_qty), 'action': 'BUY'}) #reversal
#             desired_orders.append(
#                 {'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(high - (atr / 2), 2),
#                  'totalQuantity': abs(current_qty), 'action': 'BUY'})  # reversal with trailing limit order
#         order_type = "close"
#
#         # Check if we need to modify orders
#         desired_orders_df = util.df(desired_orders)
#         # print(open_orders)
#         if len(open_orders) > 0 and order_type == "close":
#             for i in open_orders.index:
#                 for e in desired_orders_df.index:
#                     if open_orders.symbol[i] == desired_orders_df.symbol[e] and open_orders.orderType[i] == \
#                             desired_orders_df.orderType[e] and open_orders.action[i] == desired_orders_df.action[e]:
#                         if open_orders.orderType[i] == "LMT":
#                             # for trailing limit orders
#                             if current_qty > 0:
#                                 if open_orders.lmtPrice[i] > desired_orders_df.price[e]:  # for reversal
#                                     change_order(open_orders.orderId[i], desired_orders_df.price[e], contract)
#                             elif current_qty < 0:
#                                 if open_orders.lmtPrice[i] < desired_orders_df.price[e]:  # for reversal
#                                     change_order(open_orders.orderId[i], desired_orders_df.price[e], contract)
#                             ''' # for fixed limit orders
#                             if open_orders.lmtPrice[i] != desired_orders_df.price[e]:
#                                 #print(open_orders.orderId[i], open_orders.lmtPrice[i], desired_orders_df.price[e])
#                                 #cprint("changing an order price")
#                                 change_order(open_orders.orderId[i], desired_orders_df.price[e], contract)
#                             '''
#                         else:
#                             if open_orders.auxPrice[i] != desired_orders_df.price[e]:
#                                 # print(open_orders.orderId[i],open_orders.auxPrice[i],desired_orders_df.price[e])
#                                 # cprint("changing an order price")
#                                 change_order(open_orders.orderId[i], desired_orders_df.price[e], contract)
#
#     first_trade = First_trade(symbol)  # returns boolean
#
#     # wait for at least two records in the dataframe to prevent an indexing error. replace hour so last_bar_time prevents trading
#     if len(df) > 1:
#         last_bar_time = df.date.iloc[-2]  # get the time of the last bar in data
#     else:
#         last_bar_time = df.date.iloc[-1]  # get the time of the last bar in data
#         last_bar_time = last_bar_time.replace(hour=7)
#     # print(df)
#     # send new orders to open. last_bar_time == 30 if you want to select the first bar of the day
#     if last_bar_time.hour == 9 and last_bar_time.minute == 30 and first_trade == False and len(
#             desired_orders) > 0 and len(open_orders) == 0 and order_type == "open":  # use exchange time zone
#         if close > low_last_bar and close < high_last_bar:
#             desired_orders = util.df(desired_orders)
#             # cprint("sending orders")
#             place_orders(desired_orders, contract, order_type, bars, trailingPercent)
#             set_first_trade(symbol)  # change the first trade boolean
#
#     # send new orders to close
#     if len(desired_orders) > 0 and len(open_orders) == 0 and order_type == "close":
#         desired_orders = util.df(desired_orders)
#         # cprint("sending orders")
#         place_orders(desired_orders, contract, order_type, bars, trailingPercent)
#
#     # record if a stock is up or down and look for patterns
#     direction = "0"
#     if close > open:
#         direction = "1"
#     elif close < open:
#         direction = "-1"
#     record_direction(symbol, direction)
#     if symbol == super_symbol:
#         # percentage = calculate_direction(symbols) # returns percentage
#         percentage = calculate_direction(
#             symbols_direction)  # returns percentage // only uses symbols with a low enough spread
#         print(str(percentage * 100) + "% " + str(x.hour) + ":" + str(x.minute) + ":" + str(x.second))
#         if abs(percentage) == 1:
#             record_time(x.hour, x.minute, x.second, percentage)

# ib.sleep(2)


# Create contracts and subscribe to bars
# symbols = ['SPY', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'AMZN', 'AMD', 'META', 'NFLX', 'GOOGL', 'XOM', 'JPM', 'BAC', 'V',
#            'CVX', 'UNH', 'OXY', 'BA', 'INTC', 'BRK B', 'ADBE', 'JNJ', 'ENPH', 'LLY', 'MU', 'AVGO', 'MA', 'PYPL', 'COST',
#            'LRCX', 'TXN']
# symbols = ['TSLA', 'AAPL', 'NVDA', 'MSFT', 'AMZN', 'AMD', 'META', 'GOOGL', 'XOM', 'NFLX', 'V', 'JPM', 'OXY', 'JNJ',
#            'PYPL', 'CVX', 'BAC', 'INTC', 'CRM', 'WMT']
symbols = ["NVDA","TSLA","AMD","AAPL","SMCI","MSFT","META","AMZN","AVGO","GOOGL","MU",
           "ADBE","CMI","LLY","UNH","XOM","LIN","INTC","COST","CRM","NFLX","BA","V","PANW","JPM",
           "ORCL","BAC","QCOM","MRK","CVX","PFE","GE","HD","DIS","AMAT","ABBV","UBER",
           "BMY","WFC","PEP","MA","JNJ","LRCX","NKE","BKNG","CSCO","WMT","LULU","PYPL","TXN",
           "IBM","ACN","MS","C",]
# symbols = ['TSLA', 'AAPL', 'MSFT', 'NVDA', 'AMZN']
# symbols = ['TSLA', 'MSFT']
# symbols = ['MSFT']
# symbols = ['TSLA']
time_frame = 5

# symbols = ['TSLA']

account = 'DU4792662'  # paper money
# account = 'U7704220'  # real money

super_symbol = 'TSLA'  # control and limit actions in the loop with this symbol

# path = "json/" + "record_percent.json"
outside_command_path = "json/" + "outside_command.json"
with open(outside_command_path, 'w') as file_object:  # open the file in write mode
    string = ""
    json.dump(string, file_object)

path = "json/" + "close.json"
with open(path, 'w') as file_object:
    string = ""
    json.dump(string, file_object)

log("clearing log")

# list = []
# with open(path, 'w') as file_object:  # open the file in write mode
#     json.dump(list, file_object)
#
# for symbol in symbols:  # keep track if an opening trade has been made
#     path = "json/" + "check_trade" + symbol + ".json"
#     string = "False"
#     with open(path, 'w') as file_object:  # open the file in write mode
#         json.dump(string, file_object)
#
# for symbol in symbols:
#     path = "json/" + "direction" + symbol + ".json"
#     string = "0"
#     with open(path, 'w') as file_object:  # open the file in write mode
#         json.dump(string, file_object)

contracts = [Stock(symbol, 'SMART', 'USD') for symbol in symbols]
ib.qualifyContracts(*contracts)
# last_lengths = {}

#################################################################################################################
global df
df = pd.DataFrame(index=[c.symbol for c in contracts],
                  columns=['spread %', 'spread', 'vwap', 'mid_price', 'atr', 'set_time_vwap', 'vwap_1', 'vwap_2', 'vwap_3',
                           'previous_bar_high', 'previous_bar_low', 'symbol', 'pnl', 'direction', 'contract', 'sum_percent',
                           'banned', 'vwap_o', 'vwap_h', 'vwap_l', 'stairs', 'vwap_per_1', 'vwap_per_2', 'vwap_per_3',
                           'set_time_vwap_per', 'atr_count', 'set_time_atr', 'ticker_open', 'open', 'high', 'low', 'signal', 'in_trade', 'adx_signal',
                           'adx_dict', 'calculable', 'tradeable', 'wick_signal', 'wick_high', 'wick_low', 'wick_open', 'trade_bar'])
dict_spreads = {}
for c in contracts:
    new_dict = {c.symbol: []}
    dict_spreads.update(new_dict)


# df = pd.DataFrame(index = ["test"], data={'spread': [.00001], 'vwap': [1]})

# df = df.drop(["test"]).reset_index(drop=True)
def onBarUpdateNew(bars: BarDataList, has_new_bar: bool):
    xz = datetime.datetime.now()
    if xz.second % 1 != 0:  # reduce cpu load and only calculate every 2 seconds
        return
    global df
    contract = bars.contract
    symbol = bars.contract.symbol

    # # cancel subscriptions we don't need
    # bar_timeframe = int(''.join(filter(str.isdigit, bars.barSizeSetting)))  # search string '5 mins' for int
    # # print(bar_timeframe == time_frame)
    # if df.loc[symbol].calculable == "no" and not math.isnan(df.loc[symbol]["spread %"]) and symbol != symbols[0]:  # don't cancel the first symbol, it acts as a master symbol
    #     ib.cancelHistoricalData(bars)
    #     print(symbol, ": not tradeable, cancelling subscription")

    data = bars
    df_bars = util.df(data)
    try:  # sometimes bar data doesn't load for some amount of time
        df.loc[symbol].open = df_bars.iloc[-1].open
        df.loc[symbol].high = df_bars.iloc[-1].high
        df.loc[symbol].low = df_bars.iloc[-1].low
    except:
        pass
    previous_bar_time = (df_bars.iloc[-2].date).minute
    if previous_bar_time % time_frame == 0:
        df.loc[symbol].previous_bar_high = df_bars.iloc[-2].high
        df.loc[symbol].previous_bar_low = df_bars.iloc[-2].low
    # 2023-04-06 14:59:00-04:00
    # datetime_date = datetime.strptime(datetime_str, '%y-%m-%d %H:%M:%S')  # '%m/%d/%y %H:%M:%S'
    # print(df_bars.iloc[-2].date)
    # print(datetime_date)
    # print(df_bars.iloc[-1])

    # track recent movement to see if there is a pattern
    movement_dict[contract.symbol] = []
    movement_list = movement_dict[contract.symbol]
    count = 5  # add 5 bars to list
    indx = -1
    while count > 0:
        close_list = df_bars.iloc[indx].close
        open_list = df_bars.iloc[indx].open
        movement_list.append(close_list - open_list)  # add to end of list
        count -= 1
        indx -= 1

    # calculate ATR
    calc_bars = pd.DataFrame(bars)
    # print(len(calc_bars))
    atr_df = pd.DataFrame(columns=['atr'])  # erase old stuff
    atr_df.atr = ta.atr(high=calc_bars['high'].tail(750), low=calc_bars['low'].tail(750),
                        close=calc_bars['close'].tail(750), length=500, mamode='SMA')
    atr = round(atr_df.iloc[-1].atr, 4) # if atr is off, update useRTH (regular trading hours) when subscribing to historical data
    atr_1 = round(atr_df.iloc[-2].atr, 4)

    # if xz.hour == 8 and xz.minute < (30 + time_frame): # restrict updating ATR to first bar of the day, for early day trading.
    #     df.loc[symbol].atr = atr
    df.loc[symbol].atr = atr

    # look for possible wick patterns
    if df.loc[symbol].calculable == "yes":
        wick_string = "none"
        if df_bars.iloc[-1].high - df_bars.iloc[-1].open > atr*2:
            wick_string = "bull wick possible"
            df.loc[symbol].wick_high = df_bars.iloc[-1].high # update these highs and lows only when conditions are present. these values are used for stop loss
            df.loc[symbol].wick_open = df_bars.iloc[-1].open
        if df_bars.iloc[-1].open - df_bars.iloc[-1].low > atr*2:
            wick_string = "bear wick possible"
            df.loc[symbol].wick_low = df_bars.iloc[-1].low
            df.loc[symbol].wick_open = df_bars.iloc[-1].open
        if df_bars.iloc[-1].high - df_bars.iloc[-1].open > atr*2 and df_bars.iloc[-1].open - df_bars.iloc[-1].low > atr*2:
            wick_string = "bull/bear wick possible"
            df.loc[symbol].wick_high = df_bars.iloc[-1].high
            df.loc[symbol].wick_low = df_bars.iloc[-1].low
        df.loc[symbol].wick_signal = wick_string
        # print(wick_string, symbol)

    # turn off adx for now
    if 1 == 0 and df.loc[symbol].calculable == "yes":  # conserve resources and only calculate ADX for top symbols
        # calcuate ADX
        adx_df = ta.adx(high=calc_bars['high'].tail(550), low=calc_bars['low'].tail(550),
                        close=calc_bars['close'].tail(550), timeperiod=14,
                        tvmode=True)  # running dev version of talib. tvmode replicates the code on TradingView
        # print(symbol)
        # print(calc_bars)
        # print(adx_df)

        adx_df = adx_df.iloc[::-1]  # reverse the dataframe to iterate over the most recent rows.
        adx_df = adx_df.reset_index(drop=True)  # reset index to 0

        # save adx df so we can manipulate it for testing
        # outside_command_path = "json/" + "adx_test.json"
        # with open(outside_command_path, 'w') as file_object:  # open the file in write mode
        #     string = adx_df.to_json()
        #     json.dump(string, file_object)

        # print(adx_df.head(20))

        ### adx signal ### find recent bottom, look for trend strength after within a number of bars
        index_of_bottom = None  # find the most recent bottom if it exists
        adx_direction = adx_df.iloc[0].DMP_14 - adx_df.iloc[0].DMN_14
        for index, row in adx_df.iloc[:10].iterrows():  # look backwards to find bottom.
            if adx_df.iloc[index].ADX_14 < adx_df.iloc[index + 1].ADX_14:
                # print(index)
                # print(adx_df.iloc[index].ADX_14)
                index_of_bottom = index
                break
        signal_string = "none"
        adx_dict = df.loc[symbol].adx_dict
        if index_of_bottom:  # bottom is recent
            if df.loc[symbol].in_trade != "none" or df.loc[
                symbol].tradeable == "no":  # we're in a trade, record the most recent bottom or this symbol isn't tradeable and we want to prevent false signals if it becomes tradeable
                adx_dict["last_adx_bottom"] = adx_df.iloc[
                    index_of_bottom].ADX_14  # lots a decimals, an unwanted direct match is unlikely
            if adx_df.iloc[index_of_bottom].ADX_14 < 25:  # bottom is pretty low
                if adx_df.iloc[0].ADX_14 - adx_df.iloc[1].ADX_14 >= 1:  # last adx change was pretty strong
                    if adx_df.iloc[1].ADX_14 - adx_df.iloc[2].ADX_14 >= .5 and adx_df.iloc[2].ADX_14 - adx_df.iloc[
                        3].ADX_14 >= .5:  # the two before that were building strength
                        # print(adx_dict["last_adx_bottom"], adx_df.iloc[index_of_bottom].ADX_14)
                        if round(adx_dict["last_adx_bottom"], 4) != round(adx_df.iloc[index_of_bottom].ADX_14,
                                                                          4):  # continues to update bottoms while in a trade, must round for sure equality due to how digits are stored in df.
                            # print(adx_dict["last_adx_bottom"], adx_df.iloc[index_of_bottom].ADX_14)
                            signal_string = "signal_buy" if adx_direction > 0 else "signal_sell"
                            if df.loc[symbol].adx_signal == "none":
                                winsound.PlaySound('ding.wav', winsound.SND_FILENAME)
                        # else:
                        #     winsound.PlaySound('deep.wav', winsound.SND_FILENAME)
                        #     print(symbol, "rejecting because ADX bottoms match")
        df.loc[symbol].adx_signal = signal_string  # set buy sell none signal

        # adx_under_15_count = 0
        # adx_bump = None
        # adx_direction = 0
        # index_count = 0
        # for index, row in adx_df.iloc[:6].iterrows():  # iterate over 7 rows, but shift to focus on 6
        #     if ((xz.minute - (time_frame - 1)) % time_frame == 0 and xz.second > 50 and index < 6):  # check for signal late in the bar
        #         adx_bump = True if adx_df.iloc[0].ADX_14 - adx_df.iloc[1].ADX_14 >= 1 else False
        #         adx_direction = adx_df.iloc[0].DMP_14 - adx_df.iloc[0].DMN_14
        #         if row.ADX_14 <= 15:
        #             adx_under_15_count += 1
        #     if (xz.minute % time_frame == 0):  # check for signal if it was missed in the last bar
        #         adx_bump = True if adx_df.iloc[1].ADX_14 - adx_df.iloc[2].ADX_14 >= 1 else False  # shift because we are in a new bar
        #         adx_direction = adx_df.iloc[1].DMP_14 - adx_df.iloc[1].DMN_14
        #         if row.ADX_14 <= 15 and index != 0:  # shift because we are in a new bar
        #             adx_under_15_count += 1
        # adx_dict = df.loc[symbol].adx_dict
        #
        # duration_since_last_signal = (datetime.datetime.now() - adx_dict["last_signal_time"]).total_seconds()
        # if adx_under_15_count >= 5 and adx_bump == True and duration_since_last_signal >= 60 * (time_frame * 3):  # wait 3 time frames before issuing new signal
        #     df.loc[symbol].adx_signal = "signal_buy" if adx_direction > 0 else "signal_sell"
        #     # df.loc[symbol].adx_dict = {"last_signal_time": datetime.datetime.now()}
        #     # ######### for pattern verification
        #     # print(symbol)
        #     # print(xz.hour, xz.minute, xz.second)
        #     # print(adx_under_15_count)
        #     # print(adx_bump)
        #     # print(adx_direction)
        #     # adx = round(adx_df.iloc[0].ADX_14, 2)
        #     # print(adx_df.iloc[0].ADX_14 - adx_df.iloc[1].ADX_14)
        #     # print(adx_df.iloc[1].ADX_14 - adx_df.iloc[2].ADX_14)
        #     # print(adx)
        #     # print(adx_df.head(10))
        #     # print("playing sound")
        #     # winsound.PlaySound('ding.wav', winsound.SND_FILENAME)
        #     # ib.disconnect()
        #     # quit(0)
        # else:
        #     df.loc[symbol].adx_signal = "none"

        adx = round(adx_df.iloc[0].ADX_14, 2)
        # if adx <= 15:
        #     print(symbol)
        #     print(adx_under_15_count)
        #     print(adx_bump)
        #     print(adx_direction)
        #     print(adx)

        if 1 == 0:  # turn all of this off for now
            # calculate 9 EMA
            ema_df = pd.DataFrame(columns=['ema9'])  # erase old stuff
            # ema_df.ema9 = ta.ema(calc_bars['close'].tail(20), length=9)
            ema_df.ema9 = ta.ema(calc_bars.close, length=9)
            # print(ema_df.ema9.tail(20))
            ema9 = round(ema_df.iloc[-1].ema9, 4)
            # df.loc[symbol].EMA9 = ema

            # check for up signal
            signal_up = True
            for r in range(-2, -7, -1):  # check last five EMAs
                if ema_df.iloc[r].ema9 > ema_df.iloc[r - 1].ema9:
                    pass
                else:
                    signal_up = False
            if signal_up:
                if not ema_df.iloc[-2].ema9 - ema_df.iloc[
                    -11].ema9 > atr_1:  # use negative indexing to calculate from the most recent
                    signal_up = False
            if signal_up:
                bars_up_count = 0
                for r in range(-2, -12, -1):
                    if calc_bars.iloc[r].close >= calc_bars.iloc[r].open:
                        bars_up_count += 1
                if bars_up_count < 7:
                    signal_up = False
            if signal_up:
                df.loc[symbol].signal = "signal_up"
            else:
                df.loc[symbol].signal = "none"

            # check for down signal
            signal_down = True
            for r in range(-2, -7, -1):  # check last five EMAs
                if ema_df.iloc[r].ema9 < ema_df.iloc[r - 1].ema9:
                    pass
                else:
                    signal_down = False
            if signal_down:
                if not ema_df.iloc[-11].ema9 - ema_df.iloc[
                    -2].ema9 > atr_1:  # use negative indexing to calculate from the most recent
                    signal_down = False
            if signal_down:
                bars_down_count = 0
                for r in range(-2, -12, -1):
                    if calc_bars.iloc[r].close <= calc_bars.iloc[r].open:
                        bars_down_count += 1
                if bars_down_count < 7:
                    signal_down = False
            if signal_down:
                df.loc[symbol].signal = "signal_down"
            # print("down", signal_down)
            # if symbol == "TSLA":
            # print("bars up", bars_up_count, "bars down", bars_down_count)
            # print("ema-2, ema-11, atr", ema_df.iloc[-2].ema9, ema_df.iloc[-11].ema9, atr)
            # print("ema-2, ema-7", ema_df.iloc[-2].ema9, ema_df.iloc[-7].ema9)

            # update atr_count
            if previous_bar_time % time_frame == 0 and previous_bar_time != df.loc[symbol].set_time_atr:
                try:  # sometimes bar data doesn't load for some amount of time
                    p_atr_count = df.loc[symbol].atr_count
                    p_open = df_bars.iloc[-2].open
                    p_close = df_bars.iloc[-2].close
                    # print(p_atr_count, p_open, p_close, atr)
                    if p_close >= p_open + atr:
                        df.loc[symbol].set_time_atr = previous_bar_time
                        if p_atr_count > 0:
                            df.loc[symbol].atr_count = p_atr_count + 1
                        else:
                            df.loc[symbol].atr_count = 1
                    if p_close <= p_open - atr:
                        df.loc[symbol].set_time_atr = previous_bar_time
                        if p_atr_count < 0:
                            df.loc[symbol].atr_count = p_atr_count - 1
                        else:
                            df.loc[symbol].atr_count = -1
                except:
                    pass

    # print("barupdate : " + str(datetime.datetime.now() - xz))


def onPendingTickers(tickers):
    global df
    global dict_spreads
    xx = datetime.datetime.now()
    # for t in tickers:
    #     print(str(t.contract.symbol) + " " + str(t.vwap))
    for t in tickers:
        symbol = t.contract.symbol
        try:
            spread = (t.ask - t.bid) / df.loc[symbol].atr  # convert to precent of atr
            if not math.isnan(spread):
                dict_spreads[symbol].insert(0, spread)  # add new spread at the top
                if len(dict_spreads[symbol]) > 5000:  # keep the last 1,000 ticks to get an average later
                    del dict_spreads[symbol][-1]  # delete oldest spread
                # if symbol == "TSLA":
                # print(dict_spreads[symbol])
                # df.loc[symbol]["spread %"] = mean(dict_spreads[symbol])
        except:
            pass
        mid = (t.ask + t.bid) / 2
        df.loc[symbol].mid_price = mid
        df.loc[symbol].spread = t.ask - t.bid
        if 1 == 0 and df.loc[symbol].calculable == "yes":  # conserve resources and only calculate ADX for top symbols
            # get previous bars closing vwap and store vwap at time_frame in case we want to reference it later
            if xx.minute % time_frame == 0 and xx.minute != df.loc[symbol].set_time_vwap:
                df.loc[symbol].set_time_vwap = xx.minute
                df.loc[symbol].ticker_open = t.last
                if math.isnan(df.loc[symbol].vwap_1):  # if these are nan, make them all equal to let the script run
                    df.loc[symbol].vwap_1 = df.loc[symbol].vwap
                    df.loc[symbol].vwap_2 = df.loc[symbol].vwap
                    df.loc[symbol].vwap_3 = df.loc[symbol].vwap
                df.loc[symbol].vwap_3 = df.loc[symbol].vwap_2
                df.loc[symbol].vwap_2 = df.loc[symbol].vwap_1
                df.loc[symbol].vwap_1 = df.loc[symbol].vwap
                if df.loc[symbol].vwap_o == 0:  # set first vwap open, high and low
                    df.loc[symbol].vwap_o = df.loc[symbol].vwap_1
                    df.loc[symbol].vwap_h = df.loc[symbol].vwap_1
                    df.loc[symbol].vwap_l = df.loc[symbol].vwap_1
                if df.loc[symbol].vwap_1 > df.loc[symbol].vwap_h:
                    df.loc[symbol].vwap_h = df.loc[symbol].vwap_1
                if df.loc[symbol].vwap_1 < df.loc[symbol].vwap_l:
                    df.loc[symbol].vwap_l = df.loc[symbol].vwap_1
                # count vwap stairs
                if df.loc[symbol].vwap_1 > df.loc[symbol].vwap_2:
                    if df.loc[symbol].stairs >= 0:
                        df.loc[symbol].stairs = df.loc[symbol].stairs + 1
                    else:
                        df.loc[symbol].stairs = 1
                elif df.loc[symbol].vwap_1 < df.loc[symbol].vwap_2:
                    if df.loc[symbol].stairs <= 0:
                        df.loc[symbol].stairs = df.loc[symbol].stairs - 1
                    else:
                        df.loc[symbol].stairs = -1

                if df.loc[symbol].vwap_per_1 == 0:
                    df.loc[symbol].vwap_per_1 = 0
                    df.loc[symbol].vwap_per_2 = 0
                    df.loc[symbol].vwap_per_3 = 0
                df.loc[symbol].vwap_per_3 = df.loc[symbol].vwap_per_2
                df.loc[symbol].vwap_per_2 = df.loc[symbol].vwap_per_1
                if not math.isnan(df.loc[symbol].atr):
                    df.loc[symbol].vwap_per_1 = round(
                        (df.loc[symbol].vwap_1 - df.loc[symbol].vwap_2) / df.loc[symbol].atr, 2)

        df.loc[symbol].vwap = t.vwap
    # print("ticker : " + str(datetime.datetime.now() - xx))
    # # update atr_count
    # if xx.minute % time_frame == 0 and xx.minute != df.loc[symbol].set_time_atr:
    #     atr_count = df.loc[symbol].atr_count
    #     if t.last >= df.loc[symbol].ticker_open + df.loc[symbol].atr:
    #         df.loc[symbol].set_time_atr = xx.minute
    #         if atr_count > 0:
    #             df.loc[symbol].atr_count = atr_count + 1
    #         else:
    #             df.loc[symbol].atr_count = 1
    #     if t.last <= df.loc[symbol].ticker_open - df.loc[symbol].atr:
    #         df.loc[symbol].set_time_atr = xx.minute
    #         if atr_count < 0:
    #             df.loc[symbol].atr_count = atr_count - 1
    #         else:
    #             df.loc[symbol].atr_count = -1

    # df.loc[t.contract.symbol] = (t.ask - t.bid, t.vwap)

    # print(t.vwap)
    # ib.sleep(3)
    # if t.contract.symbol == "TSLA":
    #     tsla = t.vwap
    # d = {'symbol': [t.contract.symbol], 'spread': [t.ask - t.bid], 'vwap': [t.vwap]}
    # print(df)
    # print(df.loc[t.contract.symbol])
    # df.loc[t.contract.symbol] = (t.ask - t.bid, t.vwap)
    # df = pd.DataFrame(data=d)
    # df1 = pd.DataFrame(data=d)
    # df = pd.concat({'symbol': [t.contract.symbol], 'spread': [t.ask - t.bid], 'vwap': [t.vwap]}, ignore_index=True)
    # df = pd.concat([df,df1], ignore_index=True)
    # if len(df)>10:
    #     df = df.drop([0]).reset_index(drop=True)
    # print(df)
    # print(tickers)
    # print("--------------------------")


########### delete after testing is done ###################
# adx_test_path = "json/" + "adx_test.json"
# with open(adx_test_path, 'r') as openfile:
#     string = json.load(openfile)
#     adx_df = pd.read_json(string)
#     print(adx_df.head(15))
#     index_of_bottom = None  # find the most recent bottom if it exists
#     for index, row in adx_df.iloc[:10].iterrows():  # look backwards to find bottom.
#         if adx_df.iloc[index].ADX_14 < adx_df.iloc[index + 1].ADX_14:
#             print(index)
#             print(adx_df.iloc[index].ADX_14)
#             index_of_bottom = index
#             break
#     if index_of_bottom:  # bottom is recent
#         if adx_df.iloc[index_of_bottom].ADX_14 < 25:  # bottom is pretty low
#             if adx_df.iloc[0].ADX_14 - adx_df.iloc[1].ADX_14 >= 1:  # last adx change was pretty strong
#                 if adx_df.iloc[1].ADX_14 - adx_df.iloc[2].ADX_14 >= .5 and adx_df.iloc[2].ADX_14 - adx_df.iloc[3].ADX_14 >= .5:  # the two before that were building strength
#                     print("signal")
#
#     ib.disconnect()
#     quit(0)
########### delete after testing is done ###################

for contract in contracts:
    ib.sleep(.2)  # to prevent rate limiting
    ib.reqMktData(contract, '233', False, False)
    print(contract.symbol + " connected")
    # df1 = pd.DataFrame(data={'symbol': [contract.symbol], 'spread': [10], 'vwap': [1]})
    # df1 = pd.DataFrame( index = [contract.symbol],data={'spread': [10], 'vwap': [1]})
    # df = pd.concat([df, df1], ignore_index=True)
    # ticker = ib.reqTickers(contract)
tickers = ib.reqTickers(*contracts)

# ib.sleep(10)

# onPendingTickers(tickers)

ib.pendingTickersEvent += onPendingTickers
# print(ticker[0].contract.symbol)
# print(ticker)
# print(ticker[0].vwap)
# ib.disconnect()
# quit(0)
#################################################################################################################

# symbols_atr = []
# for contract in contracts:
#     #request bars to calculate atr and add to symbols list
#     bars = ib.reqHistoricalData(
#         contract,
#         endDateTime='',
#         durationStr='6 D',
#         barSizeSetting='15 mins',
#         whatToShow='TRADES',
#         useRTH=True,
#         keepUpToDate=True,
#     )
#     atr_bars = pd.DataFrame(bars)
#     atr_df = pd.DataFrame() # erase old stuff
#     atr_df['ATR'] = ta.atr(high=atr_bars['high'].tail(150), low=atr_bars['low'].tail(150),close=atr_bars['close'].tail(150), length=100, mamode='SMA')
#     atr = round(atr_df['ATR'].iloc[-1],2)
#     symbols_atr.append([bars.contract.localSymbol,atr])
#     print('atr calculated' + ' ' + str(contract.symbol) + ' ' + str(atr))
#     ib.cancelHistoricalData(bars)
#     ib.sleep(0)
#
# pnl_account = ib.reqPnL(account)
# pnl_SPY = ib.reqPnLSingle(account,modelCode = '',conId=756733)
#
# #print(symbols_atr)
# #symbols_atr[0][1]
# #ib.disconnect()
# #quit(0)
# #ib.sleep(5)
#
movement_dict = {}

print("tickers connected, requesting historical bars")

x = datetime.datetime.now()
# # Request Streaming bars
time_string = ""
if time_frame > 1:
    time_string = str(time_frame) + ' mins'
else:
    time_string = str(time_frame) + ' min'
for contract in contracts:
    ib.sleep(.2) # to prevent rate limiting
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='10 D',
        barSizeSetting=time_string,
        # barSizeSetting=str(time_frame) + ' min',
        # barSizeSetting='15 mins',
        whatToShow='TRADES',
        useRTH=True,  # use Regular Trading Hours True for Regular
        keepUpToDate=True,
    )
    print(contract.symbol, "connected")
    df.loc[contract.symbol].set_time_vwap = 0
    df.loc[contract.symbol].contract = contract
    df.loc[contract.symbol].symbol = contract.symbol
    df.loc[contract.symbol].pnl = 0
    df.loc[contract.symbol].direction = "none"
    movement_dict[contract.symbol] = []
    df.loc[contract.symbol].sum_percent = 0
    df.loc[contract.symbol].banned = ""
    df.loc[contract.symbol].vwap_o = 0
    df.loc[contract.symbol].stairs = 0
    df.loc[contract.symbol].vwap_per_1 = 0
    df.loc[contract.symbol].set_time_vwap_per = 0
    df.loc[contract.symbol].set_time_atr = 30 - time_frame  # stops atr_count from updating with premarket data
    df.loc[contract.symbol].atr_count = 0
    df.loc[contract.symbol].in_trade = "none"
    df.loc[contract.symbol].signal = "none"
    df.loc[contract.symbol].adx_signal = "none"
    df.loc[contract.symbol].adx_dict = {"last_adx_bottom": 0, "last_signal_time": datetime.datetime(2012, 3, 5, 23, 8, 15)}  # arbitrary date in the past
    df.loc[contract.symbol].calculable = "no"
    df.loc[contract.symbol].wick_signal = "none"

print("historical bars connected, waiting for open")
    # if contract.symbol == "MSFT":
    #     market_order = MarketOrder('SELL', 10)
    #     trade = ib.placeOrder(contract, market_order)

# reqRealTimeBars(contract, barSize, whatToShow, useRTH, realTimeBarsOptions=[])[source]
# for contract in contracts:
#     bars = ib.reqRealTimeBars(contract, 5, 'TRADES', True, [])
#     df.loc[contract.symbol].set_time_vwap = x.minute
#     df.loc[contract.symbol].contract = contract
#     df.loc[contract.symbol].symbol = contract.symbol
#     df.loc[contract.symbol].pnl = 0
#     df.loc[contract.symbol].direction = "none"
# ib.sleep(10)
# onBarUpdateNew(bars, True)
#
# market_order = MarketOrder('BUY', 10)
# # stop_order = StopOrder('BUY', 10, 261.75)
# trade = ib.placeOrder(contract, market_order)
# trade = ib.placeOrder(contract, stop_order)
# ib.sleep(10)
# open_trades = ib.openTrades()
# print(ib.positions())
# for trade in open_trades:
#     if trade.contract.symbol == "TSLA":
#         trade.order.auxPrice = 261.76
#         ib.placeOrder(contract, trade.order)
# place_stop_order("BUY", 10, 430)
# ib.disconnect()
# quit(0)
#
# # Check the spread and limit trading if it's too wide
# print("waiting to check spreads")
# symbol_count = []
# symbols_direction = []
# while True:
#     x = datetime.datetime.now()
#     if x.hour >= 8 and x.minute >= 44 and x.second >= 0: # use local time zone
#     #if 1 == 1:
#         for contract in contracts:
#             symbol = contract.symbol
#             ticker = ib.reqTickers(contract)
#             #ticker = ib.reqMktData(contract,  genericTickList=233) #not working
#             bid = ticker[0].bid
#             ask = ticker[0].ask
#             spread = round(ask - bid, 2)
#             spread_percent = round(spread / atr,2)
#             spread_percent_price = round(spread / ask, 10)
#             if spread_percent > .11:  # .25 is percentage of atr
#                 set_first_trade(symbol)  # don't trade this stock today
#                 first_trade = True
#                 #print(str(symbol) + " " + str(spread_percent) + " too high, don't trade")
#             else:
#                 symbol_count.append(symbol)
#                 symbols_direction.append(symbol)
#             print(str(symbol) + " " + str(round(spread_percent*100,0)) + "%" + " " + str(round(spread_percent_price * 100, 2)) + "%")
#         break
# symbol_count = len(symbol_count)
# risk = 1000/symbol_count # 1000 for $1,000 in max risk spread across tradeable securities
# #risk = 100
# print('connected')
#
# #print(bars)
#
# market_order = MarketOrder('SELL', 10)
# trade = ib.placeOrder(contract, market_order)
# # Data to be written
# #ib.disconnect()
# #quit(0)
#
#
# ib.sleep(5)
# onBarUpdateNew(bars, True)
# ib.sleep(1)
# onBarUpdateNew(bars, True)
# ib.sleep(.5)
# onBarUpdateNew(bars, True)
# ib.disconnect()
# quit(0)
#
# ib.barUpdateEvent += onBarUpdate

ib.reqPnL(account)

ib.barUpdateEvent += onBarUpdateNew

daily_trade_count = 0

# keep track of last trade_loop, we don't want to loop too much
global last_trade_loop_time
last_trade_loop_time = datetime.datetime.now()

global loop_count

# while True:
#     time = datetime.datetime.now()
#     if time.hour == 8:
#         if time.minute >= 31:
#             break
#     else:
#         break
#     ib.sleep(3)
#     print("waiting for 8:31")


# loop_count = 0
def trade_loop(bars: BarDataList, has_new_bar: bool):  # called from event listener
    x = datetime.datetime.now()  # x.hour returns hour
    global last_trade_loop_time
    last_loop_seconds = (x - last_trade_loop_time).total_seconds()
    if bars.contract.symbol == symbols[0] and last_loop_seconds >= 2:
        last_trade_loop_time = x
        try:
            #     global loop_count
            #     loop_count += 1
            #     print(loop_count)
            global df
            df = df.sort_values(by=['spread %'])
            i = 0
            # print(df.head(10))
            print(df[['signal', 'atr_count', 'stairs', 'wick_signal', 'adx_signal', 'spread %', 'spread', 'vwap',
                      'sum_percent', 'direction', 'pnl', 'mid_price', 'atr', 'in_trade', 'tradeable',
                      'calculable']].head(20))
            # if x.hour == 8:
            #     print("waiting until 9am")
            #     return
            positions = ib.positions()  # get positions
            df_positions = util.df(positions)  # create dataframe with positions
            # print(df_positions)
            open_trades = ib.openTrades()
            df_open_trades = util.df(open_trades)
            # print(df_open_trades)

            # check if a close all command has been issued
            outside_command_path = "json/" + "outside_command.json"
            with open(outside_command_path, 'r') as openfile:
                string = json.load(openfile)
            if string == "s":  # switching from string to boolean
                print("close all command received")
                close_position(1)
                print("all positions closed")
                quit()
            if string == "s75":  # switching from string to boolean
                print("reduce positions by 75% command received")
                close_position(.75)
                outside_command_path = "json/" + "outside_command.json"
                command = ""
                with open(outside_command_path, 'w') as file_object:  # open the file in write mode
                    json.dump(command, file_object)
                print("positions reduced by 75%")

            # check if a symbol has been banned
            path = "json/" + "close.json"
            with open(path, 'r') as openfile:
                string = json.load(openfile)
            if string != "":
                close_single_position(string)
                print(string + " has been closed")
                # df.loc[string].banned = "yes"
                string = ""
                with open(path, 'w') as file_object:
                    json.dump(string, file_object)

            # close all open orders and positions at the end of the day.
            if x.hour == 14 and x.minute >= 55:
                    # while True:
                    #     if len(ib.positions()) > 0 or len(ib.openTrades()) > 0:
                    #         print("open contracts found, call close_position()")
                    #         close_position(1)  # closes all positions
                    #         ib.sleep(10)  # wait and check again
                    #     else:
                    #         break
                    close_position(1)  # closes all positions
                    ib.sleep(10)  # wait and check again
                    close_position(1)
                    log("closed all positions at 2:55")
                    log("stopping algo")
                    ib.disconnect()
                    quit(0)

            pnl = ib.pnl()

            index_count = 0  # doesn't affect trading logic, just controls a print statement

            max_position_count = 10 + 1  # add one if we're holding a long term SPY position // Allows 10 positions to be open at one time but not more.
            # tradeable_count = 10  # only open trades for the top symbols in the sorted df corresponds to tradeable // only look at the top 8 symbols
            # calculable_count = 15
            max_daily_trades = 1000  # limits max trades per day to 10
            atr_count_entry = 3  # place a limit order when atr_count == 3
            for index, row in df.iterrows():
                symbol = index
                if symbol == "SPY":
                    print("symbol is spy")
                    continue
                vwap = df.loc[index].vwap
                # vwap = round(df.loc[index].vwap_1, 2)
                mid = df.loc[index].mid_price
                atr = df.loc[index].atr
                bar_open = df.loc[index].open
                bar_high = df.loc[index].high
                bar_low = df.loc[index].low
                last_check_minute = df.loc[index].set_time_vwap
                contract = df.loc[index].contract

                # close all open orders and positions at the end of the day.
                # if x.hour == 14 and x.minute >= 55:
                #     while True:
                #         final_positions = ib.positions()
                #         final_open_trades = ib.openTrades()
                #         if contract in [i.contract for i in final_positions] or contract in [j.contract for j in final_open_trades]:  # check for open positions and orders
                #             print("open contracts found, call close_position()")
                #             close_position(1)  # closes all positions
                #             ib.sleep(10)  # wait and check again
                #         else:
                #             break
                #     print("closed all positions at 2:55")
                #     print("stopping algo")
                #     ib.disconnect()
                #     quit(0)

                outside_command_path = "json/" + "risk.json"
                with open(outside_command_path, 'r') as openfile:
                    string = json.load(openfile)
                risk = float(string)

                # check if we should open a symbol
                open_position = False
                path = "json/" + "open.json"
                with open(path, 'r') as openfile:
                    string = json.load(openfile)
                if string == symbol:
                    open_position = True
                    with open(path, 'w') as file_object:  # open the file in write mode
                        string = ""
                        json.dump(string, file_object)

                # probably delete. keep track of big movements
                # if abs(df.loc[symbol].sum_percent) >= 4:
                #     path = "json/" + "sum_percent.json"
                #     with open(path, 'r') as openfile:
                #         list = json.load(openfile)
                #     list.append(str(x.hour) + ":" + str(x.minute) + ":" + str(x.second) + " " + str(symbol) + " " + str(df.loc[symbol].sum_percent) + "............................")
                #     with open(path, 'w') as file_object:  # open the file in write mode
                #         json.dump(list, file_object)

                vwap_per_1 = df.loc[symbol].vwap_per_1
                vwap_per_2 = df.loc[symbol].vwap_per_2
                vwap_per_3 = df.loc[symbol].vwap_per_3
                atr_count = df.loc[symbol].atr_count

                # # save vwap_per to file
                # if x.minute % time_frame == 0 and x.minute != df.loc[symbol].set_time_vwap_per:
                #     if abs(df.loc[symbol].vwap_per_1) >= .10 and index_count < 15:
                #         path = "json/" + "vwap_per.json"
                #         with open(path, 'r') as openfile:
                #             list = json.load(openfile)
                #         list.append(str(x.hour) + ":" + str(x.minute) + ":" + str(x.second) + " " + str(symbol) + " " + str(vwap_per_1) + " " + str(vwap_per_2) + " " + str(vwap_per_3) + "............................")
                #         with open(path, 'w') as file_object:  # open the file in write mode
                #             json.dump(list, file_object)
                # if abs(df.loc[symbol].vwap_per_1) >= .10 and index_count < 15:
                #     print(str(symbol) + " " + str(vwap_per_1) + " " + str(vwap_per_2) + " " + str(vwap_per_3))

                # # save atr_count to file
                # if abs(df.loc[symbol].atr_count) >= 4 and index_count < 15:
                #     path = "json/" + "atr_count.json"
                #     with open(path, 'r') as openfile:
                #         list = json.load(openfile)
                #     list.append(str(x.hour) + ":" + str(x.minute) + ":" + str(x.second) + " " + str(symbol) + " " + str(mid) + " " + str(atr_count) + "............................")
                #     with open(path, 'w') as file_object:  # open the file in write mode
                #         json.dump(list, file_object)
                # index_count += 1

                tradeable = False
                if df.loc[symbol]["spread %"] <= .20:
                    tradeable = True
                    df.loc[symbol].tradeable = "yes"
                else:
                    df.loc[symbol].tradeable = "no"
                if x.hour == 14 and x.minute > 50: # don't open new trades too near close
                    tradeable = False
                    df.loc[symbol].tradeable = "no"
                # tradeable_count -= 1

                if df.loc[symbol]["spread %"] < .25 or tradeable:  # help limit resource use by only calculating adx on tradeable contracts
                    df.loc[contract.symbol].calculable = "yes"
                else:
                    df.loc[contract.symbol].calculable = "no"

                try:
                    df.loc[symbol]["spread %"] = mean(dict_spreads[symbol])  # spreads are saved as a %, spread/atr
                except:
                    pass

                # wait_for_timeframe()  # make sure the first bar of the day has passed

                # if df.loc[index].hasnans:  # wait for all the data to load
                #     print(symbol + " has NaN")
                #     continue
                if x.hour == 8:
                    if x.minute < 31:
                        continue

                df.loc[symbol].sum_percent = int(sum(movement_dict[symbol]) / atr)  # sum of recent movement in %

                profit = 0
                df.loc[symbol].pnl = 0
                if len(positions) > 0:
                    for i in df_positions.index:
                        if df_positions.contract[i] == contract:
                            profit = round((mid - df_positions.avgCost[i]) * df_positions.position[i], 2)
                            df.loc[index].pnl = profit

                i += 1
                if not tradeable and contract not in [i.contract for i in positions] and contract not in [j.contract for j in open_trades]:  # iterate over the top 10 spread % and allow a position to be handled if > 10
                    continue

                vwap_1 = df.loc[symbol].vwap_1
                vwap_2 = df.loc[symbol].vwap_2
                vwap_3 = df.loc[symbol].vwap_3
                vwap_o = df.loc[symbol].vwap_o
                vwap_h = df.loc[symbol].vwap_h
                vwap_l = df.loc[symbol].vwap_l

                if vwap_1 > vwap_2:
                    df.loc[symbol].direction = "up"
                elif vwap_1 < vwap_2:
                    df.loc[symbol].direction = "dn"

                qty = int(round(risk / atr, 0))

                desired_orders = []
                order_type = "none"

                # open via command
                if open_position == True:
                    if df.loc[symbol].direction == "up":
                        market_order = MarketOrder("BUY", qty)  # original
                        ib.placeOrder(contract, market_order)
                        ib.sleep(0)

                    if df.loc[symbol].direction == "dn":
                        market_order = MarketOrder("SELL", qty)  # original
                        ib.placeOrder(contract, market_order)
                        ib.sleep(0)

                ##############################################################################################################
                # open and manage positions based on 'signal'
                # open a new order to manage
                if contract not in [i.contract for i in positions] and contract not in [j.contract for j in open_trades]:
                    df.loc[symbol].in_trade = "none"  # set to none since no positions/orders and waiting for a signal
                    # if ((x.minute - (time_frame - 1)) % time_frame == 0 and x.second > 50) or (x.minute % time_frame == 0 and x.second <= 3):  # check for signal late in the bar or v early in the current bar.
                    if (x.minute + 1) % time_frame == 0 and x.second >= 55:  # check if we are near the end of the bar
                        if tradeable and df.loc[symbol].wick_signal == "bull wick possible" and bar_high - mid >= atr*2: # check for signal and pull back
                            print(symbol, "Opening Buy Market Order - possible bull wick")
                            qty = int(round(risk / (bar_high - mid), 0))
                            market_order_to_open = MarketOrder("BUY", abs(qty))
                            ib.placeOrder(contract, market_order_to_open)
                            ib.sleep(0)
                            df.loc[symbol].trade_bar = (x.hour * (60/time_frame) * time_frame) + (x.minute - x.minute % time_frame ) # convert to a minute value.  note the bar the trade happened on for advanced stop loss protections

                        if tradeable and df.loc[symbol].wick_signal == "bear wick possible" and mid - bar_low >= atr*2:
                            print(symbol, "Opening Sell Market Order - possible bear wick")
                            qty = int(round(risk / (mid - bar_low), 0))
                            market_order_to_open = MarketOrder("SELL", abs(qty))
                            ib.placeOrder(contract, market_order_to_open)
                            ib.sleep(0)
                            df.loc[symbol].trade_bar = (x.hour * (60 / time_frame) * time_frame) + (x.minute - x.minute % time_frame)  # convert to a minute value, note the bar the trade happened on for advanced stop loss protections

                    # if tradeable and df.loc[
                    #     symbol].wick_signal == "bull wick possible":  # and (x.minute + 1) % time_frame == 0 and x.second >= 50:  # trend following
                    #     # df.loc[symbol].adx_dict["last_signal_time"] = datetime.datetime.now()  # keep track of last trade time so we don't over trade
                    #     print(symbol, "Opening Buy Stop Order - possible bull wick")
                    #     opening_price = round(bar_open, 2)
                    #     stop_order_to_open = StopOrder("BUY", abs(qty), opening_price)
                    #     ib.placeOrder(contract, stop_order_to_open)
                    #     ib.sleep(0)
                    #
                    # if tradeable and df.loc[
                    #     symbol].wick_signal == "bear wick possible":  # and (x.minute + 1) % time_frame == 0 and x.second >= 50:  # trend following
                    #     # df.loc[symbol].adx_dict["last_signal_time"] = datetime.datetime.now()  # keep track of last trade time so we don't over trade
                    #     print(symbol, "Opening Sell Stop Order - possible bear wick")
                    #     opening_price = round(bar_open, 2)
                    #     stop_order_to_open = StopOrder("SELL", abs(qty), opening_price)
                    #     ib.placeOrder(contract, stop_order_to_open)
                    #     ib.sleep(0)

                    # if tradeable and df.loc[symbol].adx_signal == "signal_buy":  # trend following
                    #     df.loc[symbol].adx_dict[
                    #         "last_signal_time"] = datetime.datetime.now()  # keep track of last trade time so we don't over trade
                    #     print(symbol, "Buying - Signal Up")
                    #     market_order = MarketOrder("BUY", abs(qty))
                    #     ib.placeOrder(contract, market_order)
                    #     ib.sleep(0)
                    #
                    # if tradeable and df.loc[symbol].adx_signal == "signal_sell":  # trend following
                    #     df.loc[symbol].adx_dict[
                    #         "last_signal_time"] = datetime.datetime.now()  # keep track of last trade time so we don't over trade
                    #     print(symbol, "Selling - Signal Down")
                    #     market_order = MarketOrder("SELL", abs(qty))
                    #     ib.placeOrder(contract, market_order)
                    #     ib.sleep(0)

                # open and manage positions based on atr_count
                # open a new order to manage
                # if 1 == 0 and contract not in [i.contract for i in positions] and contract not in [j.contract for j in open_trades]:
                #     # control over trading a trend
                #     if df.loc[symbol].in_trade == "up" and atr_count > 0:  # set atr_count to 0 if we just participated in a trend
                #         df.loc[symbol].in_trade = "none"
                #         df.loc[symbol].atr_count = 0
                #         continue
                #     elif df.loc[symbol].in_trade == "dn" and atr_count < 0:
                #         df.loc[symbol].in_trade = "none"
                #         df.loc[symbol].atr_count = 0
                #         continue
                #     else:
                #         df.loc[symbol].in_trade = "none"
                #
                #     if tradeable and len(df_positions.index) < max_position_count and abs(atr_count) >= atr_count_entry:  # limit positions to max_position_count
                #         if atr_count >= atr_count_entry:
                #             print("BUY", str(qty), str(round(bar_open + atr, 2)))
                #             place_stop_order("BUY", qty, round(bar_open + atr, 2))
                #             print(symbol + ": opening buy order")
                #         if atr_count <= -abs(atr_count_entry):
                #             print("SELL", str(qty), str(round(bar_open - atr, 2)))
                #             place_stop_order("SELL", qty, round(bar_open - atr, 2))
                #             print(symbol + ": opening sell order")

                # cancel an order that is no longer relevant
                if contract not in [i.contract for i in positions] and contract in [j.contract for j in open_trades] and df.loc[symbol].wick_signal == "none":
                    for trade in open_trades:
                        if trade.contract.symbol == symbol:
                            ib.cancelOrder(trade.order)
                            print(symbol + ": cancelling order")
                            # if trade.orderStatus.status != "PendingCancel":
                            #     ib.cancelOrder(trade.order)
                            #     # print(trade.order)
                            #     # print(trade.orderStatus.status == "PendingCancel")
                            #     print(symbol + ": cancelling order")
                            # else:
                            #     print(symbol + ": pending cancellation")

                # modify an opening orders price
                if 1==0 and contract not in [i.contract for i in positions] and contract in [j.contract for j in ib.openTrades()]:
                    for trade in open_trades:
                        # wait until late in the bar and move the opening price from open to bar high/low  +- atr
                        if trade.contract.symbol == symbol and trade.orderStatus.status != "Cancelled" and (x.minute + 1) % time_frame == 0 and x.second >= 54: # check if the order was just cancelled
                            if trade.order.action == "BUY":
                                desired_price = round(bar_high - atr*2, 2)
                                if trade.order.auxPrice != desired_price:
                                    trade.order.auxPrice = desired_price
                                    ib.placeOrder(contract, trade.order)
                                    print(str(symbol) + " auxPrice changed to " + str(desired_price))
                            if trade.order.action == "SELL":
                                desired_price = round(bar_low + atr*2, 2)
                                if trade.order.auxPrice != desired_price:
                                    trade.order.auxPrice = desired_price
                                    ib.placeOrder(contract, trade.order)
                                    print(str(symbol) + " auxPrice changed to " + str(desired_price))

                # handle open positions and send closing orders
                if contract in [i.contract for i in positions] and contract not in [j.contract for j in open_trades]:
                    for po in positions:
                        if po.contract.symbol == symbol:
                            qty_close = po.position
                            avg_cost = po.avgCost
                            if qty_close > 0:
                                df.loc[symbol].in_trade = "up"
                                action = "SELL"
                                price1 = round(df.loc[symbol].wick_high, 2)  # take profit
                                price2 = round(avg_cost - abs(df.loc[symbol].wick_high - avg_cost), 2)  # stop loss
                                if avg_cost < df.loc[symbol].wick_open:
                                    risk_reward = abs(df.loc[symbol].wick_open - df.loc[symbol].wick_high)
                                    price1 = round(avg_cost + risk_reward, 2)  # take profit
                                    price2 = round(avg_cost - risk_reward, 2)  # stop loss
                                # price1 = round(avg_cost + (atr * 2), 2)  # take profit
                                # price1 = round(avg_cost + abs(avg_cost - df.loc[symbol].wick_low), 2)  # take profit
                                # price2 = round(df.loc[symbol].wick_low, 2)  # stop loss
                            if qty_close < 0:
                                df.loc[symbol].in_trade = "dn"
                                action = "BUY"
                                price1 = round(df.loc[symbol].wick_low, 2)  # take profit
                                price2 = round(avg_cost + abs(avg_cost - df.loc[symbol].wick_low), 2)  # stop loss
                                if avg_cost > df.loc[symbol].wick_open:
                                    risk_reward = abs(df.loc[symbol].wick_open - df.loc[symbol].wick_low)
                                    price1 = round(avg_cost - risk_reward, 2)  # take profit
                                    price2 = round(avg_cost + risk_reward, 2)  # stop loss
                                # price1 = round(avg_cost - (atr * 2), 2)  # take profit
                                # price1 = round(avg_cost - abs(avg_cost - df.loc[symbol].wick_high), 2)  # take profit
                                # price2 = round(df.loc[symbol].wick_high, 2)  # stop loss
                            print(symbol, "Opening Take Profit and Stop Loss")
                            print(avg_cost, action, price1, price2, )
                            order1 = LimitOrder(action, abs(qty_close), price1)
                            order2 = StopOrder(action, abs(qty_close), price2)
                            place_oca_orders(contract, order1, order2)

                # modify stop loss price for closing order
                if contract in [i.contract for i in positions] and contract in [j.contract for j in open_trades]:
                    for trade in open_trades:
                        if trade.contract.symbol == symbol:
                            # try:
                            # print(datetime.datetime.now(timezone.utc))
                            # print(trade.log[0].time)
                            # print(datetime.datetime.now(timezone.utc) - trade.log[0].time)
                            # print((datetime.datetime.now(timezone.utc) - trade.log[0].time).total_seconds())
                            # print(trade.log)
                            # except Exception as error:
                            #     print(error)
                            # print(symbol, (datetime.datetime.utcnow() - trade.log[0].time).total_seconds())
                            # if (datetime.datetime.now(timezone.utc) - trade.log[0].time).total_seconds() > 10:  # don't modify an order too quickly, let the bars update after entry
                            if df.loc[symbol].trade_bar != "order_modified":
                                if (x.hour * (60 / time_frame) * time_frame) + x.minute >= df.loc[symbol].trade_bar + (time_frame*2): # wait for one full bar after order entry to update orders.
                                    log(str((x.hour * (60 / time_frame) * time_frame) + x.minute) + " " + str(df.loc[symbol].trade_bar + (time_frame*2)))
                                    for po in positions:
                                        if po.contract.symbol == symbol:
                                            avg_cost = po.avgCost # get the average cost for the open position
                                    if trade.order.action == "BUY":
                                        if mid < avg_cost and trade.order.orderType == "STP": # price is good, update the stop loss to reduce loss.
                                            if trade.order.auxPrice != round(avg_cost, 2):
                                                trade.order.auxPrice = round(avg_cost, 2)
                                                ib.placeOrder(contract, trade.order)
                                                df.loc[symbol].trade_bar = "order_modified"
                                                print(str(symbol) + " Stop Loss auxPrice changed to " + str(round(avg_cost, 2)))
                                        if mid > avg_cost and trade.order.orderType == "LMT":
                                            if trade.order.lmtPrice != round(avg_cost, 2):
                                                trade.order.lmtPrice = round(avg_cost, 2)
                                                ib.placeOrder(contract, trade.order)
                                                df.loc[symbol].trade_bar = "order_modified"
                                                print(str(symbol) + " Limit auxPrice changed to " + str(round(avg_cost, 2)))
                                    if trade.order.action == "SELL":
                                        if mid > avg_cost and trade.order.orderType == "STP": # price is good, update the stop loss to reduce loss.
                                            if trade.order.auxPrice != round(avg_cost, 2):
                                                trade.order.auxPrice = round(avg_cost, 2)
                                                ib.placeOrder(contract, trade.order)
                                                df.loc[symbol].trade_bar = "order_modified"
                                                print(str(symbol) + " Stop Loss auxPrice changed to " + str(round(avg_cost, 2)))
                                        if mid < avg_cost and trade.order.orderType == "LMT":
                                            if trade.order.lmtPrice != round(avg_cost, 2):
                                                trade.order.lmtPrice = round(avg_cost, 2)
                                                ib.placeOrder(contract, trade.order)
                                                df.loc[symbol].trade_bar = "order_modified"
                                                print(str(symbol) + " Limit auxPrice changed to " + str(round(avg_cost, 2)))

                                    # if trade.order.orderType == "LMT" and trade.order.action == "BUY":
                                    #     if trade.order.lmtPrice != round(bar_open - atr, 2):
                                    #         trade.order.lmtPrice = round(bar_open - atr, 2)
                                    #         ib.placeOrder(contract, trade.order)
                                    #         print(str(symbol) + " limit price changed to " + str(round(bar_open + atr, 2)))
                                    # if trade.order.orderType == "LMT" and trade.order.action == "SELL":
                                    #     if trade.order.lmtPrice != round(bar_open + atr, 2):
                                    #         trade.order.lmtPrice = round(bar_open + atr, 2)
                                    #         ib.placeOrder(contract, trade.order)
                                    #         print(str(symbol) + " limit price changed to " + str(round(bar_open - atr, 2)))
                                    # if trade.order.orderType == "STP" and trade.order.action == "BUY":
                                    #     if trade.order.auxPrice != round(bar_open + atr, 2):
                                    #         trade.order.auxPrice = round(bar_open + atr, 2)
                                    #         ib.placeOrder(contract, trade.order)
                                    #         print(str(symbol) + " Stop Loss auxPrice changed to " + str(round(bar_open + atr, 2)))
                                    # if trade.order.orderType == "STP" and trade.order.action == "SELL":
                                    #     if trade.order.auxPrice != round(bar_open - atr, 2):
                                    #         trade.order.auxPrice = round(bar_open - atr, 2)
                                    #         ib.placeOrder(contract, trade.order)
                                    #         print(str(symbol) + " Stop Loss auxPrice changed to " + str(round(bar_open - atr, 2)))

                ##############################################################################################################
                """
                # handle active positions
                if contract in [i.contract for i in positions] and contract not in [j.contract for j in open_trades]:
                    # we are in a position
                    idx = df_positions.loc[df_positions['contract'] == contract].index[0]  # locate index of the contract
                    current_qty = df_positions.position[idx]
                    avgCost = round(df_positions.avgCost[idx], 2)
                    # reverse trade and follow vwap or close
                    # if current_qty < 0:  # revert
                    if current_qty > 0:  # original
                        if vwap_1 < vwap_2 < vwap_3 or mid < vwap_1 - atr:  # and df.loc[symbol].direction != "sell":
                            # market_order = MarketOrder("SELL", abs(current_qty * 2))
                            market_order = MarketOrder("SELL", abs(current_qty))
                            ib.placeOrder(contract, market_order)
                            df.loc[symbol].banned = "yes"  # ban now to limit trading in the future
                            ib.sleep(0)
                            # df.loc[symbol].direction = "sell"
        
                    # elif current_qty > 0:  # revert
                    elif current_qty < 0:  # original
                        if vwap_1 > vwap_2 > vwap_3 or mid > vwap_1 + atr:  # and df.loc[symbol].direction != "buy":
                            # market_order = MarketOrder("BUY", abs(current_qty * 2))
                            market_order = MarketOrder("BUY", abs(current_qty))
                            df.loc[symbol].banned = "yes"  # ban now to limit trading in the future
                            ib.placeOrder(contract, market_order)
                            ib.sleep(0)
                            # df.loc[symbol].direction = "buy"
                    # if current_qty > 0:
                    #     desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(vwap, 2), 'totalQuantity': abs(current_qty) * 1, 'action': 'SELL'})
                    #     # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(avgCost - (atr), 2), 'totalQuantity': abs(current_qty) * 1, 'action': 'SELL'})
                    #     # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(low + (atr / 2), 2),'totalQuantity': abs(current_qty), 'action': 'SELL'})
                    #
                    # elif current_qty < 0:
                    #     desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(vwap, 2), 'totalQuantity': abs(current_qty) * 1, 'action': 'BUY'})
                    #     # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(avgCost + (atr), 2), 'totalQuantity': abs(current_qty) * 1, 'action': 'BUY'})
                    #     # desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'LMT', 'price': round(high - (atr / 2), 2),'totalQuantity': abs(current_qty), 'action': 'BUY'})
                    order_type = "close"
        
                # open trades if no position
                elif contract not in [i.contract for i in positions] and contract not in [j.contract for j in open_trades]:
                    # we aren't in a position
                    continue
                    if x.hour == 8:
                        if x.minute < 45:
                            continue
                    if tradeable and len(df_positions.index) < max_position_count and df.loc[symbol].banned != "yes" and daily_trade_count < max_daily_trades:  # limit positions to max_position_count
                        # if mid > vwap:
                        #     desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(vwap, 2), 'totalQuantity': qty, 'action': 'SELL'})
                        # elif mid < vwap:
                        #     desired_orders.append({'contract': contract, 'symbol': symbol, 'orderType': 'STP', 'price': round(vwap, 2), 'totalQuantity': qty, 'action': 'BUY'})
                        # order_type = "open"
                        # if vwap_1 < vwap_2 and vwap_2 < vwap_3:  # and df.loc[symbol].direction != "sell":
                        # if vwap < vwap_o - atr:
                        if vwap_per_1 <= -.10 and vwap_per_2 <= -.10 and vwap_per_3 <= -.10:
                            # market_order = MarketOrder("BUY", qty)  # revert
                            market_order = MarketOrder("SELL", qty)  # original
                            ib.placeOrder(contract, market_order)
                            ib.sleep(0)
                            daily_trade_count += 1
                            # df.loc[symbol].direction = "sell"
                        # elif vwap_1 > vwap_2 and vwap_2 > vwap_3:  # and df.loc[symbol].direction != "buy":
                        # elif vwap > vwap_o + atr:
                        elif vwap_per_1 >= .10 and vwap_per_2 >= .10 and vwap_per_3 >= .10:
                            # market_order = MarketOrder("SELL", qty)  # revert
                            market_order = MarketOrder("BUY", qty)  # original
                            ib.placeOrder(contract, market_order)
                            ib.sleep(0)
                            daily_trade_count += 1
                            # df.loc[symbol].direction = "buy"
                        # order_type = "open"
        
                # build dataframe of open orders
                open_orders = ib.openTrades()
                orders = [ord.order for ord in open_orders]
                orders = util.df(orders)
                contracts = [con.contract for con in open_orders]
                contracts = util.df(contracts)
                orders_status = [stat.orderStatus for stat in open_orders]
                orders_status = util.df(orders_status)
                trailingPercent = 0
        
                if len(open_orders) > 0:
                    open_orders = pd.concat([orders, contracts, orders_status], axis=1)  # combine dataframes into one
                    open_orders = open_orders.loc[:, ~open_orders.columns.duplicated()].copy()  # remove duplicate columns to prevent errors
                    for i in open_orders.index:
                        if open_orders.symbol[i] != symbol:
                            open_orders = open_orders.drop([i])  # drop orders not related to the current symbol
                    open_orders.reset_index(drop=True, inplace=True)  # reindex the dataframe after dropping rows
                    # open_orders = open_orders.reindex(range(len(open_orders))) # reindex the dataframe after dropping rows
                # print(open_orders)
        
                # modify open orders
                desired_orders_df = util.df(desired_orders)
                # if len(open_orders) > 0 and order_type == "close":
                if len(open_orders) > 0 and len(desired_orders) > 0:
                    for i in open_orders.index:
                        for e in desired_orders_df.index:
                            if open_orders.symbol[i] == desired_orders_df.symbol[e] and open_orders.orderType[i] == desired_orders_df.orderType[e] and open_orders.action[i] == desired_orders_df.action[e]:
                                if open_orders.orderType[i] == "LMT":
                                    # for trailing limit orders
                                    # if current_qty > 0:
                                    #     if open_orders.lmtPrice[i] > desired_orders_df.price[e]:  # for reversal
                                    #         change_order(open_orders.orderId[i], desired_orders_df.price[e], contract)
                                    # elif current_qty < 0:
                                    #     if open_orders.lmtPrice[i] < desired_orders_df.price[e]:  # for reversal
                                    #         change_order(open_orders.orderId[i], desired_orders_df.price[e], contract)
                                    # for fixed limit orders
                                    if open_orders.lmtPrice[i] != desired_orders_df.price[e]:
                                        # print(open_orders.orderId[i], open_orders.lmtPrice[i], desired_orders_df.price[e])
                                        # cprint("changing an order price")
                                        change_order(open_orders.orderId[i], desired_orders_df.price[e], contract)
                                        print(symbol + " modifying order")
        
                                else:
                                    if open_orders.auxPrice[i] != desired_orders_df.price[e]:
                                        # print(open_orders.orderId[i],open_orders.auxPrice[i],desired_orders_df.price[e])
                                        # cprint("changing an order price")
                                        change_order(open_orders.orderId[i], desired_orders_df.price[e], contract)
                                        print(symbol + " modifying order")
                # i += 1
                # if i == 10:  # iterate over the top 10 spread %
                #     break
                continue
                # send orders to open
                if tradeable and order_type == "open" and contract not in [i.contract for i in open_trades]:  # don't open more trades if a trade is waiting to be executed
                    desired_orders = util.df(desired_orders)
                    place_single_order(desired_orders, contract, order_type)
                    print(symbol + " placing order")
        
                # send orders to close
                if order_type == "close" and contract not in [i.contract for i in open_trades]:
                    desired_orders = util.df(desired_orders)
                    place_single_order(desired_orders, contract, order_type)
                
                #####------ check if profit and close
        
                #####------ cancel unwanted orders
        
                # if x.minute % time_frame == 0 and x.minute > last_check_minute:
                #     df.loc[index].last_check = x.minute
                #     df.loc[index].vwap_1 = vwap  # store vwap at time_frame in case we want to reference it later
        
                i += 1
                if i == 10:  # iterate over the top 10 spread %
                    break
                """

            # calculate win rate
            completed_trades = ib.trades()
            trade_list = []
            for trade in completed_trades:
                if trade.orderStatus.status == "Filled":  # make sure orders were filled and not cancelled
                    price = 0
                    qty = 0
                    for fill in trade.fills:  # calculate average_price
                        price += fill.execution.price * fill.execution.shares
                        qty += fill.execution.shares
                    avg_price = round(price / qty, 2)
                    trade_list.append(
                        {"symbol": trade.contract.symbol, "action": trade.order.action, "qty": qty, "price": avg_price,
                         "time": trade.log[0].time})  # add dict to list

            # trade_list = sorted(trade_list, key=lambda d: d['time'])  # sort the list based on time
            trade_list = sorted(trade_list, key=lambda d: (d['symbol'], d['time']))  # sort the list by symbol and time
            win = 0
            loss = 0
            close_date = datetime.datetime.now(timezone.utc)
            for idx, trade in enumerate(trade_list):
                try:
                    if trade["symbol"] == trade_list[idx + 1]["symbol"] and trade["time"] != close_date:
                        close_date = trade_list[idx + 1][
                            "time"]  # set time of closing trade, so we don't look at it again
                        if trade["action"] == "BUY":
                            if trade["price"] < trade_list[idx + 1]["price"]:
                                win += 1
                            else:
                                loss += 1
                        if trade["action"] == "SELL":
                            if trade["price"] > trade_list[idx + 1]["price"]:
                                win += 1
                            else:
                                loss += 1
                except:
                    pass  # out of bounds
            # print("win :", win, "loss :", loss)

            profit_sum = round(df['pnl'].sum() + pnl[0].realizedPnL, 2)
            # print("profit " + str(profit_sum))

            commission = 0
            for fill in ib.fills():
                commission += fill.commissionReport.commission
            # print("commission", round(commission, 2) * -1)
            print("profit:", profit_sum, "commission:", round(commission, 2) * -1, "win:", win, "loss:", loss, "time: " + str(x.hour) + ":" + str(x.minute) + ":" + str(x.second))

            # dump profit/loss to a .json file at fixed points of the day for review.
            if x.hour == 8 and x.minute == 45 and x.second <= 10 or x.hour == 9 and x.minute == 0 and x.second <= 10:
                dump_string = "profit: " + str(profit_sum) + " commission: " + str(round(commission, 2) * -1) + " win: " + str(win) + " loss: " + str(loss)
                path = "json/" + "dump_string.json"
                with open(path, 'r') as openfile:
                    original_string = json.load(openfile)

                with open(path, 'w') as file_object:
                    string = original_string + '     ' + dump_string
                    json.dump(string, file_object)

            # if profit_sum > 50:
            #     close_position(1)
            #     print("closing all for profit")
            #     daily_trade_count = 100
            #     # quit()
            # if profit_sum < -50:
            #     close_position(1)
            #     print("closing all for a loss")
            #     daily_trade_count = 100
            # quit()
            # if profit > 300:
            #     path = "json/" + "profit" + str(profit_sum) + ".json"
            #     with open(path, 'w') as file_object:
            #         string = ib.reqPnL(account)
            #         json.dump(string, file_object)
            # print("loop : " + str(datetime.datetime.now() - x))
            # ib.sleep(3)
        # except:
        except Exception as error:
            print(error)
            print("error caught", traceback.format_exc())
            print("wait for more data, returning")
            return


# Run infinitely
ib.barUpdateEvent += trade_loop
ib.run()

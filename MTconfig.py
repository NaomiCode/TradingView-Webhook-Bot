import MetaTrader5 as mt5
import config


def init_mt5():
    if not mt5.initialize():
        print("initializing failed!",mt5.last_error())
        mt5.shutdown()
    if config.account and config.password:
        authorized=mt5.login(config.account, password=config.password)
        if not authorized:
            print("failed to connect at account #{}, error code: {}".format(config.account, mt5.last_error()))
    print(mt5.account_info())


def get_orders(symbol):
    orders=mt5.orders_get(symbol=symbol)
    if orders is None:
        return None
    else:
        return orders

def close_trade(symbol):
    orders = get_orders(symbol=symbol)
    if orders != None:
        for order in orders:
            order = order._asdict()
            if order['magic'] == config.magic:
                price=mt5.symbol_info_tick(symbol).bid
                if order['type'] == mt5.ORDER_TYPE_BUY:
                    type_of_trade = mt5.ORDER_TYPE_SELL
                else:
                    type_of_trade = mt5.ORDER_TYPE_BUY
                request={
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": order['volume'],
                    "type": type_of_trade,
                    "position": order['ticket'],
                    "price": price,
                    "deviation": 200,
                    "magic": config.magic,
                    "comment": "python script close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_RETURN,
                }

                result=mt5.order_send(request)
                if result.retcode != mt5.TRADE_RETCODE_DONE:
                    print("order_send failed, retcode={}".format(result.retcode))
                    return False
                    
                else:
                    print("position #{} closed, {}".format(order['ticket'],result))
                    return True
    return True
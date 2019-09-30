from xylem.functions.metrics import alpha
from pendulum import from_format


def compute(context, stats, order):
    '''
    1. Find the current amount of buying power
    2. Find the current price of the security
    3. Find how many shares we can buy/sell
    4. Order that amount
    '''

    # If short term momentum exceeds long term momentum
    if ((stats["EMA12"] * (1.00 - context["bias"])) > stats["EMA26"] and
            not context["long_position"]):
        # Enter a long position, selling our short position if we have one
        if context["short_position"]:
            # Exit the short position with a market buy order
            order(1)
            context["short_position"] = False

        order(1)
        context["long_position"] = True

    # If short term momentum falls below long term momentum
    elif ((stats["EMA12"] * (1.00 + context["bias"])) < stats["EMA26"] and
          not context["short_position"]):
        # Enter a short position, selling our long position if we have one
        if context["long_position"]:
            order(-1)
            context["long_position"] = False

        order(-1)
        context['short_position'] = True


def before_exit(context, stats, order):
    # if context["long_position"]:
        # print("Long position before_exit()")

    # if context["short_position"]:
        # print("Short position before_exit()")

    order(liquidate=True)


def analyze(result_set, barsets):
    for results, barset in zip(result_set, barsets):
        RI = results["ending_balance"] - results["starting_balance"]
        start = from_format(results["start_time"], 'YYYY-MM-DD').date()
        stop = from_format(results["stop_time"], 'YYYY-MM-DD').date()
        # print("Alpha: ", alpha(RI, results.symbol, start, stop))

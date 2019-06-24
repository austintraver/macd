def compute(context, stats, order):
    # If short term momentum exceeds long term momentum
    if (stats["EMA12"] * (1.00 - context["bias"])) > stats["EMA26"] and not context["long_position"]:
        # Enter a long position, selling our short position if we have one
        if context["short_position"]:
            # Returning the stock that we borrowed requires subtracting from our balance
            order(1)
            context["short_position"] = False

        order(1)
        context["long_position"] = True
        
    # If short term momentum falls below long term momentum
    elif (stats["EMA12"] * (1.00 + context["bias"])) < stats["EMA26"] and not context["short_position"]:
        # Enter a short position, selling our long position if we have one
        if context["long_position"]:
            order(-1)
            context["long_position"] = False

        order(-1)
        context['short_position'] = True

def before_exit(context, stats, order):
    if context["long_position"]:
        order(-1)

    if context["short_position"]:
        order(1)

def analyze(result_set):
    pass
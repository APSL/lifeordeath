from datetime import timedelta


def rag_column(stamp, frequency, warning, elapsed):
    data = dict(item=([dict(value=None, text=None)] * 3))
    if elapsed >= timedelta(seconds=frequency):
        colour = 0
    elif elapsed >= timedelta(seconds=warning):
        colour = 1
    else:
        colour = 2
    data['item'][colour] = {'value': elapsed.total_seconds() / 60, 'text': 'mins ago'}
    return data

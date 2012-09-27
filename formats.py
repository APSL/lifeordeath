from datetime import datetime, timedelta


def geckoboard_rag_column(stamp):
    data = dict(item=([dict(value=None, text=None)] * 3))
    now = datetime.now()
    elapsed = now - stamp.timestamp
    if elapsed >= timedelta(seconds=stamp.frequency):
        colour = 0
    elif elapsed >= timedelta(seconds=stamp.warning):
        colour = 1
    else:
        colour = 2
    data['item'][colour] = {'value': elapsed.seconds, 'text': stamp.key}
    return data

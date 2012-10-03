from datetime import datetime, timedelta


def rag_column(stamp, event):
    data = dict(item=([dict(value=None, text=None)] * 3))
    now = datetime.now()
    elapsed = now - stamp.timestamp
    if elapsed >= timedelta(seconds=event['frequency']):
        colour = 0
    elif elapsed >= timedelta(seconds=event['warning']):
        colour = 1
    else:
        colour = 2
    data['item'][colour] = {'value': elapsed.seconds / 60, 'text': 'mins ago'}
    return data

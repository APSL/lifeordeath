from datetime import timedelta


def rag_column(stamp, frequency, warning, elapsed):
    data = dict(item=([dict(value=None, text=None)] * 3))
    if elapsed >= timedelta(seconds=frequency):
        colour = 0
    elif elapsed >= timedelta(seconds=warning):
        colour = 1
    else:
        colour = 2
    time = elapsed.days * 24 * 60 + elapsed.seconds / 60
    ago = 'mins ago'
    if time > 300:
        time = time / 60
        ago = 'hours ago'
    data['item'][colour] = {'value': time, 'text': ago}
    return data

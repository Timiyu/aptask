def time_since(from_time):
    import arrow
    from_time = arrow.get(arrow.get(from_time).datetime, 'Asia/Shanghai')
    return from_time.humanize(arrow.now('Asia/Shanghai'), locale='zh')
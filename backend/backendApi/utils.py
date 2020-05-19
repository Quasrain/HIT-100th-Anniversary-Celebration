# 方法库


# 将UID转换成序数词
def getUID(x):
    y = x % 100
    if 11 <= y <= 13:
        return '%sth' % x
    y = y % 10
    if y == 1:
        return '%sst' % x
    if y == 2:
        return '%snd' % x
    if y == 3:
        return '%srd' % x
    return '%sth' % x
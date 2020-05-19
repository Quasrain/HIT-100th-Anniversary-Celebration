from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models

import random

# 添加评论
# todo: 自动审核
def addComment(request):
    comment = models.Comment()
    tmp = request.path.split('/')
    comment.Name = tmp[2]
    comment.Tag = tmp[3]
    comment.Comment = tmp[4]
    comment.Year = tmp[5]
    comment.save()
    ret = comment.UID
    return HttpResponse('%s' % ret)

# 选择100条评论进行展示，逻辑是top5 + 80条前200高赞，15条随机
def selectComment(request):
    decades = [0 for i in range(10)]
    data = models.Comment.objects.all().order_by('-Year')

    if len(data) <= 100:
        ret = []
        for x in data:
            tmp = [x.UID, x.Name, x.Tag, x.Comment, x.Year]
            ret.append(tmp)
        return HttpResponse(ret)

    data_top = models.Comment.objects.all().order_by('-Count')
    select_uid = set()
    for i in range(5):
        year = data_top[i].Year
        year = (year - 1920) / 10
        decades[year] += 1
        select_uid.add(data_top[i].UID)
    ret = []
    cnt = 0
    while len(select_uid) < 85:
        cnt += 1
        y = 0
        if len(data_top) > 200:
            y = 199
        else:
            y = len(data_top) - 1 
        x = random.randint(0, y)
        year = data_top[x].Year
        year = (year - 1920) / 10
        if year == 10:
            year = 9
        if decades[year] >= 10 or data_top[x].UID in select_uid:
            if cnt < 500:
                continue
        decades[year] += 1
        select_uid.add(data_top[x].UID)
    while len(select_uid) < 100:
        x = random.randint(1, len(data_top) - 1)
        year = data_top[x].Year
        year = (year - 1920) / 10
        if year == 10:
            year = 9
        if decades[year] >= 10 or data_top[x].UID in select_uid:
            if cnt < 500:
                continue
        decades[year] += 1
        select_uid.add(data_top[x].UID)
    for x in select_uid:
        tmp = models.Comment.objects.get(UID = x)
        ret.append([tmp.UID, tmp.Name, tmp.Tag, tmp.Comment, tmp.Year])
    res = sorted(ret, key = lambda x: x[4], reverse = True)
    return HttpResponse(res)

# 点赞功能，需要前端传输UID
def like(request):
    tmp = request.path.split('/')
    uid = tmp[2]
    count = models.Comment.objects.get(UID = uid)
    models.Comment.objects.filter(UID = uid).update(Count = count.Count + 1)
    return HttpResponse(count.Count + 1)


# 抽取最后的幸运参与者，不急
def lottery(request):
    data_top = models.Comment.objects.all().order_by('-Count')
    tot = len(data_top)
    res = []
    Set = set()
    cnt = 1
    while len(res) < 5:
        l = 0
        r = cnt * (tot-1) // 5
        x = random.randint(l, r)
        if x not in Set:
            Set.add(x)
            res.append([data_top[x].UID, data_top[x].Name, data_top[x].Tag, data_top[x].Comment, data_top[x].Count])
            cnt += 1
    return HttpResponse(res)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models
import json

import random
from aip import AipImageCensor


APP_ID = '20127419'
API_KEY = 'HnCMlNQBzVsQr4z3S57vClIK'
SECRET_KEY = 'hqpehal5EiZtqs3bjCgoroLpRF9PZwLW'
client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)

def check(str):
    result = client.textCensorUserDefined(str)
    if result.get('conclusion') == '不合规':
        return True
    return False

# 添加评论
# todo: 自动审核
def addComment(request):
    comment = models.Comment()
    tmp = request.path.split('/')
    comment.Department = tmp[2]
    comment.Grade = tmp[3]
    comment.Identity = tmp[4]
    comment.Name = tmp[5]
    comment.Comment = tmp[6]
    if check(tmp[2]) or check(tmp[3]) or check(tmp[4]) or check(tmp[5]) or check(tmp[6]):
        data = {
            'Succ' : False,
            'UID' : -1,
        }
        return JsonResponse(data)
    comment.save()
    ret = comment.UID
    data = {
        'Succ' : True,
        'UID' : ret,
    }
    return JsonResponse(data)

# 选择第x页，每页100条
def selectComment(request):
    data = models.Comment.objects.all()
    tmp = request.path.split('/')
    x = int(tmp[2])
    if (x <= 0):
        left = 0
        right = len(data)
    else:
        left = (x - 1) * 100
        right = min(x * 100, len(data))
    data = data[left : right]
    ret = []
    for x in data:
        tmp = {
            'UID' : x.UID,     
            'Department' : x.Department,
            'Grade' : x.Grade,
            'Identity' : x.Identity,
            'Name' : x.Name,
            'Comment': x.Comment,
            'Count': x.Count,
        }
        ret.append(tmp)
    res = {
        'size' : len(data),
        'data' : ret,
    }
    return JsonResponse(res, safe = False, json_dumps_params={'ensure_ascii':False})

# 点赞功能，需要前端传输UID
def like(request):
    tmp = request.path.split('/')
    uid = tmp[2]
    count = models.Comment.objects.get(UID = uid)
    models.Comment.objects.filter(UID = uid).update(Count = count.Count + 1)
    data = {
        'Count' : count.Count + 1,
    }
    return JsonResponse(data)


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
    res = sorted(res, key = lambda x: x[4], reverse = True)
    ret = []
    for x in res:
        data = {
            'UID' : x[0],
            'Name' : x[1],
            'Tag' : x[2],
            'Comment': x[3],
        }
        ret.append(data)
    data = {
        'data' : ret,
    }
    return JsonResponse(data, safe = False, json_dumps_params={'ensure_ascii':False})


# 选取
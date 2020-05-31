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
    str = request.path.split('/')[-1]
    tmp = str.split('-')
    comment.Department = tmp[0]
    comment.Grade = tmp[1]
    comment.Identity = tmp[2]
    comment.Name = tmp[3]
    comment.Comment = tmp[4]
    comment.phone = tmp[5]
    # 查询是否存在一样的数据
    QAQ = models.Comment.objects.filter(Department = comment.Department, Grade = comment.Grade, Identity = comment.Identity, Name = comment.Name, Comment = comment.Comment, phone = comment.phone)
    if len(QAQ) > 0:
        data = {
            'status' : 210,
            'UID' : -1,
        }
        return JsonResponse(data)
    # 自动审核内容
    if check(tmp[0]) or check(tmp[1]) or check(tmp[2]) or check(tmp[3]) or check(tmp[4]):
        data = {
            'status' : 211,
            'UID' : -1,
        }
        return JsonResponse(data)
    comment.save()
    ret = comment.UID
    data = {
        'Succ' : 200,
        'UID' : ret,
    }
    return JsonResponse(data)

# 选择第x页，每页100条
def selectComment(request):
    data = models.Comment.objects.all()
    tmp = request.path.split('-')
    x = int(tmp[-1])
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
        'status' : 200,
        'size' : len(data),
        'data' : ret,
    }
    return JsonResponse(res, safe = False, json_dumps_params={'ensure_ascii':False})

# 点赞功能，需要前端传输UID
def like(request):
    tmp = request.path.split('-')
    uid = tmp[-1]
    count = models.Comment.objects.get(UID = uid)
    models.Comment.objects.filter(UID = uid).update(Count = count.Count + 1)
    data = {
        'status' : 200,
        'Count' : count.Count + 1,
    }
    return JsonResponse(data)


# 抽取最后的幸运参与者
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
            res.append([data_top[x].UID, data_top[x].Department, data_top[x].Grade, data_top[x].Identity, data_top[x].Name, data_top[x].Comment, data_top[x].Count, data_top[x].phone])
            cnt += 1
    res = sorted(res, key = lambda x: x[6], reverse = True)
    ret = []
    for x in res:
        data = {
            'UID' : x[0],
            'Department' : x[1],
            'Grade' : x[2],
            'Identity' : x[3],
            'Name' : x[4],
            'Comment': x[5],
            'Count' : x[6],
            'phone' : x[7],
        }
        ret.append(data)
    data = {
        'status' : 200,
        'data' : ret,
    }
    return JsonResponse(data, safe = False, json_dumps_params={'ensure_ascii':False})


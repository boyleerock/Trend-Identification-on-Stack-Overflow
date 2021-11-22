from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from mysite.settings import BASE_DIR
import os
from datetime import datetime, timedelta
import re
import pandas as pd
from account import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import pandas as pd


# Create your views here.
# main page
def main(request):
    # to do something

    return redirect(to='index/')


def index(request):
    return render(request, 'index.html')


import json


@login_required
@csrf_exempt
def outPut(request):
    if request.method == 'POST':
        # start = request.POST.get('start')
        # end = request.POST.get('end')
        # num_window = request.POST.get('num_window')
        # limit = request.POST.get('limit')
        # types = request.POST.get('types')
        # sort = request.POST.get('sort')
        # word = request.POST.get('word')
        # username = request.session['username']
        # fileDir = models.File.objects.filter(status=1, user__username=username).first().dir
        #
        # # 8 elements
        # input_string = f'start:{start} end:{end} num_window:{num_window} limit:{limit} types:{types} sort:{sort} word:{word} fileDir:{fileDir}'
        # print(input_string)
        # dir = 'static/txt/input.txt'
        # with open(dir, 'w+') as f:
        #     f.write(input_string)
        #
        # # exec(open('batch_analysis.py').read())  # perform NLP ------------------------
        # return render(request,'output_new.html')
        data = json.loads(request.POST.get('data'))
        print(data)
        start = data.get('start')

        end = data.get('end')
        num_window = data.get('num_window')
        limit = data.get('limit')
        types = data.get('types')
        sort = data.get('sort')
        word = data.get('word')
        print(start, end, num_window, limit, types, sort, word)
        spelling = data.get('spelling', 0)
        spelling = 1 if spelling == True else 0
        singularize = data.get('singularize', 0)
        singularize = 1 if singularize == True else 0
        n_lines = data.get('n_lines')
        username = request.session['username']
        fileDir = models.File.objects.filter(status=1, user__username=username).first().dir
        print(spelling, singularize)

        input_string = f'start:{start} end:{end} num_window:{num_window} limit:{limit} ' \
                       f'types:{types} sort:{sort} word:{word} ' \
                       f'fileDir:{fileDir} ' \
                       f'spelling:{spelling} singularize:{singularize} n_lines:{n_lines}'
        print(input_string)
        dir = 'static/txt/input.txt'
        with open(dir, 'w+') as f:
            f.write(input_string)

        spell = "disabled"
        singular = "enabled"
        if (spelling == 1):
            spell = "enabled"
        if (singularize == 0):
            singular = "disabled"

        # fixme
        # import time
        # time.sleep(2)
        exec(open('batch_analysis.py').read())  # perform NLP ------------------------

        # todo: write info
        df_res = pd.read_csv("output/merge.csv")
        n_rows = df_res.shape[0]
        if (types == "unrelated_qa"):
            types = "unrelated questions and answers (1:1)"
        elif (types == "qa"):
            types = "questions with related answers"
        elif (types == "qc"):
            types = "questions with related comments"
        elif (types == "ac"):
            types = "answers with related comments"

        if (sort == "creation_date_desc"):
            sort = "most recent created"
        elif (sort == "creation_date_asc"):
            sort = "least recent created"
        elif (sort == "score"):
            sort = "highest score"

        d = {'start date': [start], 'end date': [end], 'number of time windows': [num_window],
             'limit per time window': [limit],
             'post type': [types], 'sort by': [sort], 'phrase contains': [word], 'spelling correction': [spell],
             'singularize': [singular], 'number of phrases to display': [n_lines],
             'total number of eligible phrases': [n_rows]}
        df = pd.DataFrame(data=d)
        df.to_csv("static/csv/info.csv", index=False)
        # return render(request,'output_new.html')
        data = {'code': 1}
        return JsonResponse(data)


@login_required
def outPutPage(request):
    return render(request, 'output_new.html')


@login_required
def outPutData(request):
    if request.method == "GET":
        f = open('static/txt/input.txt', 'r')  # read inputs
        lines = f.readlines()
        n_lines = int(lines[0].split(" ")[10].split(":")[1])
        print(lines[0])

        # n_lines = 20

        # read resulting csv
        df = pd.read_csv('output/merge.csv')
        df = df[df.frequency > 0]  # todo: drop fake rows
        df.to_csv('static/csv/merge.csv', index=False)
        print("output csv")

        if (df.shape[0] >= n_lines):
            df = df.head(n_lines)
        else:
            n_lines = df.shape[0]

        print("df total number of rows:", df.shape[0])
        df = df.head(n_lines)
        freqs_matrix = []
        date_list = []

        # freq values: number of rows = number of lines, number of columns = number of time windows
        # n_lines = 5
        num_window = re.search('num_window:(.+? )', lines[0])
        num_window = num_window.group().split(':')[1].strip(' ')
        print(num_window)
        num_window = int(num_window)
        for i in range(0, n_lines):
            row = []
            for j in range(0, num_window):
                row.append(int(df.iat[i, j + 4]))
            freqs_matrix.append(row)
        print(freqs_matrix)

        time_windows = list(df.columns.values.tolist())
        for i in range(num_window):
            date_list.append(time_windows[i + 4])
            date_split = date_list[i].split(" ")
            date_list[i] = date_split[0] + " ~ " + date_split[3]

        # legends: phrase names
        cate_names = []
        index = 0
        for line in df.values:
            cate_names.append(f'{line[1]} {line[2]}')
        print(cate_names)

        data = {'code': 1, 'cate_names': cate_names, 'freqs_matrix': freqs_matrix, 'date_list': date_list}
        return JsonResponse(data)


from django.core.exceptions import PermissionDenied


def per_denied(request):
    raise PermissionDenied

#! /usr/bin/env python
# -*- coding:utf-8 -*-
import shutil
import xml
import time
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.db.models import Sum, Max, F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

import xlrd
import requests, re


def page404(request):
    return render(request, 'RBAC/standard/404.html')


def notFount(request,  exception=404):
    return render(request, 'RBAC/standard/404.html')

def serverError(request):
    return render(request, 'RBAC/other/404.html')


def forbidden(request, exception=403):
    return render(request, 'RBAC/other/404.html')
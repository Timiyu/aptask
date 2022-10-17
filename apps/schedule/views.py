# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.views.generic.base import View


class Schedule(View):

    def get(self, request):
        return JsonResponse({'1': '1'})

    def post(self, request):
        return JsonResponse({'1': '1'})

    def delete(self, request):
        return JsonResponse({'1': '1'})

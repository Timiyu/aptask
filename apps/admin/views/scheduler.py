from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse
import json

from regex import F


class Scheduler(View):
    def get(self,request):
        return render(request,'admin/scheduler.html')
    
    def post(self,request):
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
    
    @staticmethod
    def schedulers(request):
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse
import json
from apscheduler import job,jobstores


class Scheduler(View):
    def get(self,request):
        return render(request,'admin/scheduler.html')
    
    def post(self,request):
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
    
    def delete(self, request):
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
    
    @staticmethod
    def scheduler_single(request):
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
    
    @staticmethod
    def schedulers_list(request):
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
    
    @staticmethod
    def schedulers_delete(request):
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
from atexit import register
from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse
from django_apscheduler.models import DjangoJob,DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobExecution,DjangoJobStore,DjangoJob,DjangoResultStoreMixin,DjangoMemoryJobStore,register_events,register_job
from aptask.settings import TIME_ZONE
import json

scheduler = BackgroundScheduler(timezone=TIME_ZONE)
register_events(scheduler)


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
        req_data = request.GET
        current_page = req_data.get('current_page',1)
        page_size = req_data.get('page_size',10)
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
    
    @staticmethod
    def schedulers_delete(request):
        return JsonResponse(json.dumps({}, ensure_ascii=False),safe=False)
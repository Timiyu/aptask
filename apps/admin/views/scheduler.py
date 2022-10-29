from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse
import json

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
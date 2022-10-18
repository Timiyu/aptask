from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from admin.tools.admin_mixin_utils import superuser_only
from website.models import Opt_log
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from admin.tools.covert_tools import chinese_time
import json


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def list_client_history(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/website-history-list.html')

    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        sort_type = data.get('sort_type', 'descending')
        if sort_type is None:
            sort_type = 'descending'
        column_name = data.get('column_name', '')
        filter = data.get('filter', {'username': '', 'ipaddress': '', 'os': '', 'platform': '', 'zone': '', 'browser': ''})
        if filter['username'] != '':
            if column_name == '':
                all_history = Opt_log.objects.filter(
                    Q(userinfo__username__icontains=filter['username']) & Q(
                        ipaddress__icontains=filter['ipaddress']) & Q(
                        os__icontains=filter['os']) & Q(platform__icontains=filter['platform']) & Q(
                        zone__icontains=filter['zone']) & Q(browser__icontains=filter['browser'])).order_by('-id')
            else:
                if sort_type == 'descending':
                    sort_type = '-'
                elif sort_type == 'ascending':
                    sort_type = ''
                all_history = Opt_log.objects.filter(
                    Q(userinfo__username__icontains=filter['username']) & Q(
                        ipaddress__icontains=filter['ipaddress']) & Q(
                        os__icontains=filter['os']) & Q(platform__icontains=filter['platform']) & Q(
                        zone__icontains=filter['zone'])& Q(browser__icontains=filter['browser'])).order_by(
                    '{0}{1}'.format(sort_type, column_name))
        else:
            if column_name == '':
                all_history = Opt_log.objects.filter(
                    Q(ipaddress__icontains=filter['ipaddress']) & Q(
                        os__icontains=filter['os']) & Q(platform__icontains=filter['platform']) & Q(
                        zone__icontains=filter['zone'])& Q(browser__icontains=filter['browser'])).order_by('-id')
            else:
                if sort_type == 'descending':
                    sort_type = '-'
                elif sort_type == 'ascending':
                    sort_type = ''
                all_history = Opt_log.objects.filter(
                    Q(ipaddress__icontains=filter['ipaddress']) & Q(
                        os__icontains=filter['os']) & Q(platform__icontains=filter['platform']) & Q(
                        zone__icontains=filter['zone'])& Q(browser__icontains=filter['browser'])).order_by(
                    '{0}{1}'.format(sort_type, column_name))
        try:
            page = data.get('current_page', 1)
        except PageNotAnInteger:
            page = 1
        try:
            pagesize = data.get('page_size', 1)
        except PageNotAnInteger:
            pagesize = 1
        p = Paginator(all_history, pagesize)
        total = len(all_history)
        try:
            resp_history = p.page(page)
        except EmptyPage:
            resp_history = list()
        resp_data = list()
        for item in resp_history:
            resp_item = dict()
            resp_item['id'] = item.id
            resp_item['ipaddress'] = item.ipaddress
            resp_item['platform'] = item.platform
            resp_item['os'] = item.os
            resp_item['browser'] = item.browser
            if item.userinfo is None:
                resp_item['userinfo'] = '匿名'
            else:
                resp_item['userinfo'] = item.userinfo.username
            resp_item['path'] = item.path
            resp_item['zone'] = item.zone
            resp_item['device'] = item.device
            resp_item['addtime'] = chinese_time(item.addtime)
            resp_data.append(resp_item)
        page_result = dict()
        page_result["pageData"] = resp_data
        page_result['total'] = total
        page_result['success'] = 'success'
        page_result['msg'] = '分页查询成功'
        return JsonResponse(page_result, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def delete_opt_logs(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        print(data)
        logs = data.get('deleteitems')
        try:
            for item in logs:
                Opt_log.objects.filter(id=item['id']).delete()
            resp = {'success': 'success', 'msg': '删除选中记录成功！'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed', 'msg': '删除选中记录失败！'}
        return JsonResponse(resp, safe=False)

from django.shortcuts import render
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator
from admin.tools.admin_mixin_utils import AdminLoginRequiredMixin
from admin.tools.admin_mixin_utils import superuser_only



def chinese_time(x):
    y = datetime.strftime(x, "%Y{0}%m{1}%d{2} %H{3}%M{4}%S{5}".format("年", "月", '日', '时', '分', '秒'))
    return y


# Create your views here.
# 首页

class Index(AdminLoginRequiredMixin, View):
    @method_decorator(superuser_only)
    def get(self, request):
        return render(request, 'admin/index.html')
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.users.models import AdminUser
from aptask import settings
import json
from django.contrib.auth.hashers import make_password

resp_data = dict()
login_success_code = 'success'
login_success_message = '登录成功'
login_failed_code = 'failed'
login_failed_message = '登录失败'
register_success_code = 'success'
register_success_message = '注册成功'
register_failed_code = 'failed'
register_failed_message = '注册失败'
login_session_default_expiry = settings.LOGIN_SESSION_EXPIRY_DEFAULT
login_session_remember_expiry = settings.LOGIN_SESSION_EXPIRY_REMEMBER


class CustomBackend(ModelBackend):
    def authenticate(self, request, username:str='', password:str='', **kwargs):
        try:
            user = AdminUser.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            else:
                return None
        except Exception as e:
            return None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        is_staff = getattr(user, 'is_staff', None)
        can_auth = is_active and is_staff
        return can_auth or (is_active is None or is_staff is None)


class Register(View):
    @staticmethod
    def get(request):
        with open(settings.LOGIN_PUBLIC_KEY) as f:
            key = f.read().splitlines()
        public_key = ""
        for item in key:
            public_key += item
        return render(request, 'users/register.html', {'public_key': public_key})

    @staticmethod
    def post(request):
        data = request.body
        data = json.loads(data)
        resp_data['data'] = ''
        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password', '')
        name_user = User.objects.filter(username=username)
        email_user = User.objects.filter(email=email)
        if name_user:
            resp_data['code'] = register_failed_code
            resp_data['message'] = '账号 {} 已存在'.format(username)
        elif email_user:
            resp_data['code'] = register_failed_code
            resp_data['message'] = '邮箱 {} 已绑定账号 {}'.format(
                email, email_user[0].username)
        else:
            from extra_apps.utils.createkey import decrypt_password
            password = make_password(decrypt_password(password))
            user = User(username=username, email=email,
                        password=password, is_staff=True)
            try:
                user.save()
                resp_data['code'] = register_success_code
                resp_data['message'] = register_success_message
            except Exception as e:
                print(e)
                resp_data['code'] = register_failed_code
                resp_data['message'] = register_failed_message
        return JsonResponse(resp_data, safe=False)


class Login(View):
    @staticmethod
    def get(request):
        with open(settings.LOGIN_PUBLIC_KEY) as f:
            key = f.read().splitlines()
        public_key = ""
        for item in key:
            public_key += item
        return render(request, 'users/login.html', {'public_key': public_key})

    @staticmethod
    def post(request):
        data = request.body
        data = json.loads(data)
        username = data.get('username', '')
        password = data.get('password', '')
        remember = data.get('remember', False)
        from extra_apps.utils.createkey import decrypt_password
        password = decrypt_password(password)
        user = auth.authenticate(username=username, password=password)
        resp_data = dict()
        if user:
            auth.login(request, user)
            if remember is True:
                request.session.set_expiry(
                    login_session_remember_expiry*24*60*60)
            else:
                request.session.set_expiry(
                    login_session_default_expiry*24*60*60)
            resp_data['data'] = {}
            resp_data['code'] = login_success_code
            resp_data['message'] = login_success_message
        else:
            resp_data['data'] = {}
            resp_data['code'] = login_failed_code
            resp_data['message'] = login_failed_message
        return JsonResponse(resp_data, safe=False)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', settings.LOGIN_URL))

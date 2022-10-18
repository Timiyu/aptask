from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from blog.models import ArticleCategory as Category, Article
from users.models import UserProfile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
import json
from admin.tools.covert_tools import chinese_time, str_list, list_str
from admin.tools.admin_mixin_utils import superuser_only


# Create your views here.


# 文章分类
@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def List_Category(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/article-category-list.html')

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Get_All_Category(request):
    if request.method == 'GET':
        first_level_cate = Category.objects.filter(CateLevel='1').order_by('-UpDate_Time')
        resp_cate = list()
        for item_1 in first_level_cate:
            resp_first_level = {'value': {'id': item_1.id, 'CategoryName': item_1.CategoryName},
                                'label': item_1.CategoryName, 'children': list()}
            second_level_cate = Category.objects.filter(ParentCategory__id=item_1.id).order_by('-UpDate_Time')
            if len(second_level_cate) > 0:
                for item_2 in second_level_cate:
                    resp_second_level = {'value': {'id': item_2.id, 'CategoryName': item_2.CategoryName},
                                         'label': item_2.CategoryName, 'children': list()}
                    three_level_cate = Category.objects.filter(ParentCategory__id=item_2.id).order_by('-UpDate_Time')
                    if len(three_level_cate) > 0:
                        for item_3 in three_level_cate:
                            resp_three_level = {'value': {'id': item_3.id, 'CategoryName': item_3.CategoryName},
                                                'label': item_3.CategoryName}
                            resp_second_level['children'].append(resp_three_level)
                    else:
                        resp_second_level.pop('children')
                    resp_first_level['children'].append(resp_second_level)
            else:
                resp_first_level.pop('children')
            resp_cate.append(resp_first_level)

        print(resp_cate)
        return JsonResponse({'success': 'success', 'allcategory': resp_cate, 'msg': '查询所有分类成功！'}, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Get_Category(request):
    if request.method == 'GET':
        column_name = request.GET.get('column_name')

        sort_type = request.GET.get('sort_type')

        filter = request.GET.get('filter', {'CategoryName': '', 'ParentCategory': ''})

        filter = json.loads(filter)

        if filter['ParentCategory'] == '':

            if column_name == '':
                all_category = Category.objects.filter(CategoryName__icontains=filter['CategoryName']).order_by('-id')
            else:
                if sort_type is None:
                    all_category = Category.objects.filter(CategoryName__icontains=filter['CategoryName']).order_by(
                        '-id')
                else:
                    if sort_type == 'descending':
                        sort_type = '-'
                    elif sort_type == 'ascending':
                        sort_type = ''
                    all_category = Category.objects.filter(CategoryName__icontains=filter['CategoryName']).order_by(
                        '{}'.format(sort_type + column_name))
        else:

            if column_name == '':
                all_category = Category.objects.filter(Q(CategoryName__icontains=filter['CategoryName']) & Q(
                    ParentCategory__CategoryName__icontains=filter['ParentCategory'])).order_by('-id')
            else:
                if sort_type is None:
                    all_category = Category.objects.filter(Q(CategoryName__icontains=filter['CategoryName']) & Q(
                        ParentCategory__CategoryName__icontains=filter['ParentCategory'])).order_by('-id')
                else:
                    if sort_type == 'descending':
                        sort_type = '-'
                    elif sort_type == 'ascending':
                        sort_type = ''
                    all_category = Category.objects.filter(Q(CategoryName__icontains=filter['CategoryName']) & Q(
                        ParentCategory__CategoryName__icontains=filter['ParentCategory'])).order_by(
                        '{}'.format(sort_type + column_name))
        try:
            page = request.GET.get('current_page', 1)
        except PageNotAnInteger:
            page = 1
        try:
            pagesize = request.GET.get('page_size', 1)
        except PageNotAnInteger:
            pagesize = 1
        p = Paginator(all_category, pagesize)
        total = len(all_category)
        try:
            pageData = p.page(page)
        except EmptyPage:
            pageData = list()

        data = list()
        page_result = dict()
        for item in pageData:
            if item.ParentCategory is None:
                data.append({
                    'id': item.id,
                    'CategoryName': item.CategoryName,
                    'ParentCategory': {'id': None, 'CategoryName': '没有父分类'},
                    'CateLevel': item.CateLevel,
                    'Slug': item.Slug,
                    'AddDate_Time': chinese_time(item.AddDate_Time),
                    'UpDate_Time': chinese_time(item.UpDate_Time)
                })
            else:
                data.append({
                    'id': item.id,
                    'CategoryName': item.CategoryName,
                    'ParentCategory': {'id': item.ParentCategory.id, 'CategoryName': item.ParentCategory.CategoryName},
                    'CateLevel': item.CateLevel,
                    'Slug': item.Slug,
                    'AddDate_Time': chinese_time(item.AddDate_Time),
                    'UpDate_Time': chinese_time(item.UpDate_Time)
                })
        page_result["pageData"] = data
        page_result['total'] = total
        page_result['success'] = 'success'
        page_result['msg'] = '分页查询成功'
        return JsonResponse(page_result, safe=False)

    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        category_id = int(data.get('id', ''))
        try:
            item = Category.objects.get(id=category_id)
            if item.ParentCategory is None:
                category = {
                    'id': item.id,
                    'CategoryName': item.CategoryName,
                    'ParentCategory': {'id': None, 'CategoryName': '没有父分类'},
                    'Slug': item.Slug,
                    'AddDate_Time': chinese_time(item.AddDate_Time),
                    'UpDate_Time': chinese_time(item.UpDate_Time)
                }
            else:
                category = {
                    'id': item.id,
                    'CategoryName': item.CategoryName,
                    'ParentCategory': {'id': item.ParentCategory.id, 'CategoryName': item.ParentCategory.CategoryName},
                    'Slug': item.Slug,
                    'AddDate_Time': chinese_time(item.AddDate_Time),
                    'UpDate_Time': chinese_time(item.UpDate_Time)
                }
            resp = {'success': 'success', 'msg': '查询成功', 'category': category}
        except SystemError:
            resp = {'success': 'failed', 'msg': '没有找到分类，或已被删除！'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Add_Category(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        category_name = data.get('CategoryName')
        parent_category = data.get('ParentCategory')
        if parent_category == '' or parent_category == []:
            parent_category = None
            cate_level = '1'
        else:
            parent_category = Category.objects.get(id=(parent_category[-1]).get('id'))
            cate_level = str(int(parent_category.CateLevel) + 1)
        resp = {}
        category = dict()
        try:
            if int(cate_level) > 3:
                resp = {'success': 'failed', 'msg': '分类最多为3级，父分类不能是3级分类！'}
            else:
                category['CategoryName'] = category_name
                category['ParentCategory'] = parent_category
                category['CateLevel'] = cate_level
                Category.objects.create(**category)
                resp = {'success': 'success', 'msg': '分类添加成功！'}
        except Exception as e:
            print(e)
            resp = {'success': 'success', 'msg': '分类添加失败！'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Edit_Category(request):
    if request.method == 'GET':
        cate_id = request.GET.get('id')
        resp_category = dict()
        try:
            category = Category.objects.get(id=cate_id)
            if category.CateLevel == '1':
                resp_category = {
                    'id': category.id,
                    'CategoryName': category.CategoryName,
                    'ParentCategory': '',
                    'ParentCateLabel': "请选择父分类",
                    'Slug': category.Slug,
                    'AddDate_Time': chinese_time(category.AddDate_Time),
                    'UpDate_Time': chinese_time(category.UpDate_Time)
                }
            if category.CateLevel == '2':
                resp_category = {
                    'id': category.id,
                    'CategoryName': category.CategoryName,
                    'ParentCategory': [
                        {'id': category.ParentCategory.id, 'CategoryName': category.ParentCategory.CategoryName}],
                    'ParentCateLabel': category.ParentCategory.CategoryName,
                    'Slug': category.Slug,
                    'AddDate_Time': chinese_time(category.AddDate_Time),
                    'UpDate_Time': chinese_time(category.UpDate_Time)
                }

            if category.CateLevel == '3':
                parent_category = category.ParentCategory
                grand_parent_category = parent_category.ParentCategory
                resp_category = {
                    'id': category.id,
                    'CategoryName': category.CategoryName,
                    'ParentCategory': [{'id': parent_category.id, 'CategoryName': parent_category.CategoryName}],
                    'ParentCateLabel': grand_parent_category.CategoryName + ' / ' + parent_category.CategoryName,
                    'Slug': category.Slug,
                    'AddDate_Time': chinese_time(category.AddDate_Time),
                    'UpDate_Time': chinese_time(category.UpDate_Time)
                }
            resp = {'success': 'success', 'resp_category': resp_category}
        except Exception as e:
            print(e)
            resp = {'success': 'failed', 'mag': '查询失败！'}

        return JsonResponse(resp, safe=False)

    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        cate_id = data.get('id')
        category_name = data.get('CategoryName')
        parent_category = data.get('ParentCategory')
        if parent_category == '' or parent_category == []:
            parent_category = None
            cate_level = '1'
        else:
            parent_category = Category.objects.get(id=(parent_category[-1]).get('id'))
            cate_level = str(int(parent_category.CateLevel) + 1)
        resp = {}
        category = Category.objects.get(id=cate_id)
        try:
            if int(cate_level) > 3:
                resp = {'success': 'failed', 'msg': '分类最多为3级，父分类不能是3级分类！'}
            else:
                category.CategoryName = category_name
                category.ParentCategory = parent_category
                category.CateLevel = cate_level
                category.save()
                resp = {'success': 'success', 'msg': '分类编辑已保存！'}
        except Exception as e:
            print(e)
            resp = {'success': 'success', 'msg': '分类编辑保存失败！'}

        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Category(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        category_id = int(data.get('id', 0))
        resp = {}
        try:
            Category.objects.filter(id=category_id).delete()
            if len(Category.objects.filter(id=category_id)) == 0:
                resp = {'success': 'success', 'msg': '分类已删除！'}
            else:
                resp = {'success': 'failed', 'msg': '删除分类失败！'}
        except SystemError:
            resp = {'success': 'failed', 'msg': '删除分类失败！'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Selected_Category(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        resp = {}
        try:
            for item in data:
                Category.objects.get(id=item['id']).delete()
            resp = {'success': 'success', 'msg': '删除成功！'}
        except SystemError:
            resp = {'success': 'failed', 'msg': '删除异常！'}
        return JsonResponse(resp, safe=False)


# 课程
@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def List_Articles(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/articles-list.html')

    if request.method == 'POST':
        request_data = request.body

        request_data = json.loads(request_data)

        column_name = request_data.get('column_name')

        sort_type = request_data.get('sort_type')

        filter_data = request_data.get('filter', {
            'ArticleTitle': '',
            'CategoryName': '',
            'ArticleTags': '',
        })
        print(request_data)

        if column_name == '':
            all_article = Article.objects.filter(
                Q(ArticleTitle__icontains=filter_data['ArticleTitle']) & Q(
                    ArticleTags__icontains=filter_data['ArticleTags']) & Q(
                    ArticleCategory__CategoryName__icontains=filter_data['CategoryName'])).order_by('-id')
        else:
            if sort_type is None:
                all_article = Article.objects.filter(
                    Q(ArticleTitle__icontains=filter_data['ArticleTitle']) & Q(
                        ArticleTags__icontains=filter_data['ArticleTags']) & Q(
                        ArticleCategory__CategoryName__icontains=filter_data['CategoryName'])).order_by('-id')
            else:
                if sort_type == 'descending':
                    sort_type = '-'
                elif sort_type == 'ascending':
                    sort_type = ''
                all_article = Article.objects.filter(
                    Q(ArticleTitle__icontains=filter_data['ArticleTitle']) & Q(
                        ArticleTags__icontains=filter_data['ArticleTags']) & Q(
                        ArticleCategory__CategoryName__icontains=filter_data['CategoryName'])).order_by(
                    '{}'.format(sort_type + column_name))
        try:
            page = request_data.get('current_page', 1)
        except PageNotAnInteger:
            page = 1
        try:
            pagesize = request_data.get('page_size', 1)
        except PageNotAnInteger:
            pagesize = 1
        p = Paginator(all_article, pagesize)
        total = len(all_article)
        try:
            pageData = p.page(page)
        except EmptyPage:
            pageData = list()

        data = list()
        page_result = dict()
        for item in pageData:
            if item.ArticleCategory is None:
                data.append({
                    'id': item.id,
                    'ArticleTitle': item.ArticleTitle,
                    'ArticleAuthor': item.ArticleAuthor.username,
                    'ArticleDescribe': item.ArticleDescribe,
                    'ArticleReadNum': item.ArticleReadNum,
                    'CategoryName': "没有分类",
                    'ArticleSlug': item.ArticleSlug,
                    'ArticleCover': item.ArticleCover,
                    'ArticleTags': str_list(item.ArticleTags),
                    'AddDate_Time': chinese_time(item.AddDate_Time),
                    'UpDate_Time': chinese_time(item.UpDate_Time)
                })
            else:
                data.append({
                    'id': item.id,
                    'ArticleTitle': item.ArticleTitle,
                    'ArticleAuthor': item.ArticleAuthor.username,
                    'ArticleDescribe': item.ArticleDescribe,
                    'ArticleReadNum': item.ArticleReadNum,
                    'CategoryName': item.ArticleCategory.CategoryName,
                    'ArticleSlug': item.ArticleSlug,
                    'ArticleCover': item.ArticleCover,
                    'ArticleTags': str_list(item.ArticleTags),
                    'AddDate_Time': chinese_time(item.AddDate_Time),
                    'UpDate_Time': chinese_time(item.UpDate_Time)
                })
        print(data)
        page_result["pageData"] = data
        page_result['total'] = total
        page_result['success'] = 'success'
        page_result['msg'] = '分页查询成功'
        return JsonResponse(page_result, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Add_Article(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        resp = dict()
        article = dict()
        title = data['ArticleTitle']
        category = data['Category']
        tag = data['ArticleTags']
        content = data['ArticleContent']
        article['ArticleTags'] = list_str(tag)
        user_id = request.user.id
        user = UserProfile.objects.get(id=user_id)
        article['ArticleDescribe'] = data['ArticleDescribe']
        article['ArticleTitle'] = title
        article['ArticleCover'] = data['ArticleCover']
        article['ArticleAuthor'] = user
        article['ArticleContent'] = content
        if category == [] or category == '':
            article['ArticleCategory'] = None
        else:
            try:
                article['ArticleCategory'] = Category.objects.get(id=(category[-1]).get('id'))
                Article.objects.create(**article)
                resp = {'success': 'success', 'message': '发表文章成功！'}
            except Exception as e:
                print(e)
                resp = {'success': 'failed', 'message': '文章发表失败，请稍后重试！'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Get_Article(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        article_id = int(data.get('id'))
        article = Article.objects.get(id=article_id)

        category = article.ArticleCategory

        Cate_Label = ''

        if category.CateLevel == '1':
            Cate_Label = category.CategoryName

        if category.CateLevel == '2':
            Cate_Label = category.ParentCategory.CategoryName + ' / ' + category.CategoryName

        if category.CateLevel == '3':
            parent_category = category.ParentCategory
            grand_parent_category = parent_category.ParentCategory
            Cate_Label = grand_parent_category.CategoryName + ' / ' + parent_category.CategoryName + ' / ' + category.CategoryName

        resp_article = {
            'id': article.id,
            'ArticleTitle': article.ArticleTitle,
            'ArticleAuthor': article.ArticleAuthor.username,
            'Category': [{'id': article.ArticleCategory.id, 'CategoryName': article.ArticleCategory.CategoryName}],
            'CategoryLabel': Cate_Label,
            'ArticleSlug': article.ArticleSlug,
            'ArticleCover': article.ArticleCover,
            'ArticleDescribe': article.ArticleDescribe,
            'ArticleTags': str_list(article.ArticleTags),
            'ArticleContent': article.ArticleContent,
            'AddDate_Time': chinese_time(article.AddDate_Time),
            'UpDate_Time': chinese_time(article.UpDate_Time)
        }

        return JsonResponse({'Article': resp_article}, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Edit_Article(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        resp = dict()
        article = Article.objects.get(id=data['id'])
        req_category = data['Category']
        if req_category == '' or req_category == []:
            category = None
        else:
            category = Category.objects.get(id=(req_category[-1]).get('id'))
        try:
            article.ArticleTitle = data['ArticleTitle']
            article.ArticleContent = data['ArticleContent']
            article.ArticleCover = data['ArticleCover']
            article.ArticleDescribe = data['ArticleDescribe']
            article.ArticleCategory = category
            article.ArticleTags = list_str(data['ArticleTags'])
            article.save()
            resp = {'success': 'success', 'message': '文章编辑已保存！'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed', 'message': '文章编辑保存失败！'}

        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Article(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        article_id = int(data.get('id'))
        resp = {}
        try:
            Article.objects.filter(id=article_id).delete()
            resp = {'success': 'success', 'msg': '已删除文章！'}

        except SystemError:
            resp = {'success': 'failed', 'msg': '删除文章失败！'}

        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
def Delete_Selected_Article(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        resp = {}
        try:
            for item in data:
                article_id = int(item['id'])
                Article.objects.filter(id=article_id).delete()

            resp = {'success': 'success', 'msg': '已删除选中文章！'}
        except SystemError:

            resp = {'success': 'failed', 'msg': '批量删除文章失败！'}

        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Upload_Image(request):
    if request.method == 'POST':
        file = request.FILES.get("file")
        file_name = file.name
        file_ext = file_name.split('.')[-1]
        file_content = file.read()
        import os
        import time
        tmp_path = "/opt/tmp/{0}".format(int(time.time()))
        file_path = tmp_path + '/' + file_name
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        f = open(file_path, "wb")
        f.write(file_content)
        f.close()
        image_url = ''
        if file_ext.lower() in ['jpg', 'png', 'jpeg']:
            try:
                from utils.compress import compress_image, resize_image
                compress_image_path = compress_image(file_path, tmp_path + '/compress.' + file_ext, quality=10)
                resize_image_path = resize_image(compress_image_path, tmp_path + '/resized.' + file_ext, x_s=1024)
                from utils.VodUploadSDK.samples.uploadImage import testUploadLocalImage
                try:
                    image_url = testUploadLocalImage(resize_image_path, file_name)
                    if compress_image_path == file_path:
                        pass
                    else:
                        os.remove(compress_image_path)
                    os.remove(resize_image_path)
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
                from utils.VodUploadSDK.samples.uploadImage import testUploadLocalImage
                try:
                    image_url = testUploadLocalImage(file_path, file_name)
                except Exception as e:
                    print(e)
        else:
            from utils.VodUploadSDK.samples.uploadImage import testUploadLocalImage
            try:
                image_url = testUploadLocalImage(file_path, file_name)
            except Exception as e:
                print(e)
        os.remove(file_path)
        os.rmdir(tmp_path)
        return JsonResponse({'location': image_url}, safe=False)

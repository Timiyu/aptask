from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Category, Courses, CourseLessons, CourseCapitals
from resources.models import Videos
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
import json
from admin.tools.covert_tools import chinese_time, str_list, list_str, timeConvert
from admin.tools.admin_mixin_utils import superuser_only


# Create your views here.


# 课程分类
@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def List_Category(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/category-list.html')


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
        resp = dict()
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
def List_Courses(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/courses-list.html')

    if request.method == 'POST':
        data = request.body

        data = json.loads(data)

        column_name = data.get('column_name')

        sort_type = data.get('sort_type')

        filter = data.get('filter', {
            'CourseName': '',
            'CategoryName': '',
            'CourseTags': '',
        })

        if column_name == '':
            all_course = Courses.objects.filter(
                Q(CourseName__icontains=filter['CourseName']) & Q(CourseTags__icontains=filter['CourseTags']) & Q(
                    Category__CategoryName__icontains=filter['CategoryName'])).order_by('-id')
        else:
            if sort_type is None:
                all_course = Courses.objects.filter(
                    Q(CourseName__icontains=filter['CourseName']) & Q(CourseTags__icontains=filter['CourseTags']) & Q(
                        Category__CategoryName__icontains=filter['CategoryName'])).order_by('-id')
            else:
                if sort_type == 'descending':
                    sort_type = '-'
                elif sort_type == 'ascending':
                    sort_type = ''
                all_course = Courses.objects.filter(
                    Q(CourseName__icontains=filter['CourseName']) & Q(CourseTags__icontains=filter['CourseTags']) & Q(
                        Category__CategoryName__icontains=filter['CategoryName'])).order_by(
                    '{}'.format(sort_type + column_name))
        try:
            page = data.get('current_page', 1)
        except PageNotAnInteger:
            page = 1
        try:
            pagesize = data.get('page_size', 1)
        except PageNotAnInteger:
            pagesize = 1
        p = Paginator(all_course, pagesize)
        total = len(all_course)
        try:
            pageData = p.page(page)
        except EmptyPage:
            pageData = list()

        data = list()
        page_result = dict()
        for item in pageData:
            if item.Category is None:
                data.append({
                    'id': item.id,
                    'CourseName': item.CourseName,
                    'CategoryName': "没有分类",
                    'CourseDescribe': item.CourseDescribe,
                    'CourseFeeType': item.get_CourseFeeType_display(),
                    'CourseStudent': item.CourseStudent,
                    'CourseFavNum': item.CourseFavNum,
                    'CourseClickNum': item.CourseClickNum,
                    'CourseTarget': item.CourseTarget,
                    'CourseNeedKnow': item.CourseNeedKnow,
                    'CoursePrice': item.CoursePrice,
                    'CourseDegree': item.get_CourseDegree_display(),
                    'Slug': item.Slug,
                    'IsBannerCourse': item.get_IsBannerCourse_display(),
                    'CourseTags': str_list(item.CourseTags),
                    'AddDate_Time': chinese_time(item.AddDate_Time),
                    'UpDate_Time': chinese_time(item.UpDate_Time)
                })
            else:
                data.append({
                    'id': item.id,
                    'CourseName': item.CourseName,
                    'CategoryName': item.Category.CategoryName,
                    'CourseDescribe': item.CourseDescribe,
                    'CourseFeeType': item.get_CourseFeeType_display(),
                    'CourseStudent': item.CourseStudent,
                    'CourseFavNum': item.CourseFavNum,
                    'CourseTarget': item.CourseTarget,
                    'CourseNeedKnow': item.CourseNeedKnow,
                    'CourseClickNum': item.CourseClickNum,
                    'CoursePrice': item.CoursePrice,
                    'CourseDegree': item.get_CourseDegree_display(),
                    'Slug': item.Slug,
                    'IsBannerCourse': item.get_IsBannerCourse_display(),
                    'CourseTags': str_list(item.CourseTags),
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
def Add_Course(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        resp = dict()
        course = data
        category = course['Category']
        tag = course['CourseTags']
        course['CourseTags'] = list_str(tag)
        if category == [] or category == '':
            category = None
        else:
            try:
                course['Category'] = Category.objects.get(id=(category[-1]).get('id'))
                Courses.objects.create(**course)
                resp = {'success': 'success', 'message': '添加课程成功！'}
            except Exception as e:
                print(e)
                resp = {'success': 'failed', 'message': '添加课程失败，请稍后重试！'}
        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Get_Course(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        course_id = int(data.get('id'))
        course = Courses.objects.get(id=course_id)
        resp_capitals_lessons = list()
        capitals = course.get_capitals()
        for item in capitals:
            resp_capital = {'id': item.id, 'CapitalName': item.CapitalName}
            lessons = item.get_lessons()
            resp_lessons = list()
            for lesson in lessons:
                resp_lesson = {'id': lesson.id, 'LessonName': lesson.LessonName,
                               'LessonFreePreview': lesson.LessonFreePreview,
                               'LessonVideo': {'id': lesson.LessonVideo.id, 'VideoId': lesson.LessonVideo.VideoId,
                                               'VideoTitle': lesson.LessonVideo.VideoTitle,
                                               'VideoCoverURL': lesson.LessonVideo.VideoCoverURL,
                                               'VideoDuration': timeConvert(lesson.LessonVideo.VideoDuration)}}
                resp_lessons.append(resp_lesson)
            resp_capitals_lessons.append({'capital': resp_capital, 'lessons': resp_lessons})

        category = course.Category

        Cate_Label = ''

        if category.CateLevel == '1':
            Cate_Label = category.CategoryName

        if category.CateLevel == '2':
            Cate_Label = category.ParentCategory.CategoryName + ' / ' + category.CategoryName

        if category.CateLevel == '3':
            parent_category = category.ParentCategory
            grand_parent_category = parent_category.ParentCategory
            Cate_Label = grand_parent_category.CategoryName + ' / ' + parent_category.CategoryName + ' / ' + category.CategoryName

        resp_course = {
            'id': course.id,
            'CourseName': course.CourseName,
            'Category': [{'id': course.Category.id, 'CategoryName': course.Category.CategoryName}],
            'CategoryLabel': Cate_Label,
            'CourseDescribe': course.CourseDescribe,
            'CourseDetail': course.CourseDetail,
            'CourseFeeType': course.CourseFeeType,
            'CourseStudent': course.CourseStudent,
            'CourseFavNum': course.CourseFavNum,
            'CourseClickNum': course.CourseClickNum,
            'CourseTarget': course.CourseTarget,
            'CourseNeedKnow': course.CourseNeedKnow,
            'CoursePrice': course.CoursePrice,
            'CourseDegree': course.CourseDegree,
            'HorizontalImage': course.HorizontalImage,
            'VerticalImage': course.VerticalImage,
            'WideBannerImage': course.WideBannerImage,
            'Slug': course.Slug,
            'IsBannerCourse': course.IsBannerCourse,
            'CourseTags': str_list(course.CourseTags),
            'AddDate_Time': chinese_time(course.AddDate_Time),
            'UpDate_Time': chinese_time(course.UpDate_Time)
        }

        return JsonResponse({'Course': resp_course, 'Capitals_Lessons': resp_capitals_lessons}, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Creat_Capitals(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        course_id = data.get('course_id')
        resp = dict()
        capital = dict()
        try:
            course = Courses.objects.get(id=course_id)
            capital['CapitalName'] = data.get('CapitalName')
            capital['CapitalCourse'] = course
            CourseCapitals.objects.create(**capital)
            resp = {'success': 'success', 'message': '已添加章节！'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed', 'message': '添加章节失败'}
        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Creat_Lessons(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        capital_id = data.get('capital_id')
        course_id = data.get('course_id')
        req_video = data.get('video')
        video_id = req_video.get('id')
        resp = dict()
        lesson = dict()
        print(data)
        try:
            capital = CourseCapitals.objects.get(id=capital_id)
            course = Courses.objects.get(id=course_id)
            video = Videos.objects.get(id=video_id)
            lesson['LessonName'] = data.get('LessonName')
            lesson['LessonCourse'] = course
            lesson['LessonCapital'] = capital
            lesson['LessonVideo'] = video
            lesson['LessonFreePreview'] = data.get('LessonFreePreview')
            CourseLessons.objects.create(**lesson)
            resp = {'success': 'success', 'message': '已添加小节！'}
        except Exception as e:
            print(e)
            resp = {'success': 'success', 'message': '添加小节失败！'}
        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Edit_Capital(request):
    if request.method == 'GET':
        capital_id = request.GET.get('capital_id')
        capital = CourseCapitals.objects.get(id=capital_id)
        resp_capital = {'capital_id': capital.id, 'CapitalName': capital.CapitalName}
        return JsonResponse({'Capital': resp_capital}, safe=False)

    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        capital_id = data.get('capital_id')
        resp = dict()
        capital = CourseCapitals.objects.get(id=capital_id)
        try:
            capital.CapitalName = data.get('CapitalName')
            capital.save()
            resp = {'success': 'success', 'message': '章节编辑已保存！'}
        except Exception as e:
            print(e)
            resp = {'success': 'success', 'message': '章节编辑保存失败！'}
        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Edit_Lesson(request):
    if request.method == 'GET':
        lesson_id = request.GET.get('lesson_id')
        lesson = CourseLessons.objects.get(id=lesson_id)
        resp_lesson = {'lesson_id': lesson.id, 'LessonName': lesson.LessonName,
                       'LessonFreePreview': lesson.LessonFreePreview,
                       'video': {'id': lesson.LessonVideo.id, 'VideoId': lesson.LessonVideo.VideoId,
                                 'VideoTitle': lesson.LessonVideo.VideoTitle,
                                 'VideoCoverURL': lesson.LessonVideo.VideoCoverURL,
                                 'VideoDuration': timeConvert(lesson.LessonVideo.VideoDuration)}}
        print(resp_lesson)

        return JsonResponse({'Lesson': resp_lesson}, safe=False)

    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        lesson_id = data.get('lesson_id')
        req_video = data.get('video')
        resp = dict()
        print(data)
        try:
            lesson = CourseLessons.objects.get(id=lesson_id)
            video = Videos.objects.get(id=req_video.get('id'))
            lesson.LessonName = data.get('LessonName')
            lesson.LessonVideo = video
            lesson.LessonFreePreview = data.get('LessonFreePreview')
            lesson.save()
            resp = {'success': 'success', 'message': '小节编辑已保存！'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed', 'message': '小节编辑保存失败！'}

        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Capital(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        capital_id = data.get('capital_id')
        resp = dict()

        try:
            CourseCapitals.objects.filter(id=capital_id).delete()
            resp = {'success': 'success', 'message': '章节已删除！'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed', 'message': '章节删除失败！'}

        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Lesson(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        lesson_id = data.get('lesson_id')
        resp = dict()
        try:
            CourseLessons.objects.filter(id=lesson_id).delete()
            resp = {'success': 'success', 'message': '小节已删除！'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed', 'message': '小节删除失败！'}

        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Edit_Course(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        resp = dict()
        course = Courses.objects.get(id=data['id'])
        req_category = data['Category']
        if req_category == '' or req_category == []:
            category = None
        else:
            category = Category.objects.get(id=(req_category[-1]).get('id'))
        print(data)
        try:
            course.CourseName = data['CourseName']
            course.Category = category
            course.CourseDescribe = data['CourseDescribe']
            course.CourseDetail = data['CourseDetail']
            course.HorizontalImage = data['HorizontalImage']
            course.VerticalImage = data['VerticalImage']
            course.WideBannerImage = data['WideBannerImage']
            course.CourseDegree = data['CourseDegree']
            course.CourseFeeType = data['CourseFeeType']
            course.CourseTarget = data['CourseTarget']
            course.CourseNeedKnow = data['CourseNeedKnow']
            course.CoursePrice = data['CoursePrice']
            course.IsBannerCourse = data['IsBannerCourse']
            course.CourseTags = list_str(data['CourseTags'])
            course.save()
            resp = {'success': 'success', 'message': '课程编辑已保存！'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed', 'message': '课程编辑保存失败！'}

        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Course(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        course_id = int(data.get('id'))
        resp = {}
        try:
            Courses.objects.filter(id=course_id).delete()
            resp = {'success': 'success', 'msg': '已删除课程！'}

        except SystemError:
            resp = {'success': 'failed', 'msg': '删除课程失败！'}

        return JsonResponse(resp, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Selected_Courses(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        resp = {}
        try:
            for item in data:
                course_id = int(item['id'])
                Courses.objects.filter(id=course_id).delete()

            resp = {'success': 'success', 'msg': '已删除选中课程！'}
        except SystemError:

            resp = {'success': 'failed', 'msg': '批量删除课程失败！'}

        return JsonResponse(resp, safe=False)

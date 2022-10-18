from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from admin.tools.admin_mixin_utils import superuser_only
from django.shortcuts import render
from django.db.models import Q
from utils.log import logger
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from resources.models import Pictures, Videos
from utils.aliyun_image_util import delete_image
from utils.aliyun_video_util import delete_video, get_video_playauth
from admin.tools.covert_tools import chinese_time, approximate_size, timeConvert, str_list
import json

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Get_Picture_Cate(request):
    if request.method == 'GET':
        from utils.aliyun_image_util import get_picture_category
        resp = get_picture_category()
        resp_picture_cate = list()
        if resp.get('SubTotal') > 0:
            for item in resp.get('SubCategories')['Category']:
                first_level = {'value': item, 'label': item['CateName'], 'children': list()}
                sub_resp = get_picture_category(cateId=item['CateId'])
                if sub_resp.get('SubTotal') > 0:
                    for item_1 in sub_resp.get('SubCategories')['Category']:
                        second_level = {'value': item_1, 'label': item_1['CateName']}
                        first_level['children'].append(second_level)
                else:
                    first_level.pop('children')
                resp_picture_cate.append(first_level)
        return JsonResponse({'resp_picture_cate': resp_picture_cate}, safe=False)


# get_pictures_this_type
@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Get_Picture_This_Type(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        logger(data)
        picturecate = data.get('cate')
        if picturecate == '':
            pictures = Pictures.objects.filter().order_by('-UpDate_Time')
        else:
            pictures = Pictures.objects.filter(ImageCateId=(picturecate[-1]).get('CateId')).order_by('-UpDate_Time')
        resp_pictures = list()

        for item in pictures:
            picture = dict()
            picture['id'] = item.id
            picture['ImageURL'] = item.ImageURL
            picture['ImageURLTumb'] = item.ImageURL + '?x-oss-process=image/resize,l_20,s_20'
            picture['ImageTitle'] = item.ImageTitle
            resp_pictures.append(picture)
        return JsonResponse({'Pictures': resp_pictures}, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def List_Pictures(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/pictures-list.html')

    if request.method == 'POST':
        data = request.body

        data = json.loads(data)

        logger(data)

        column_name = data.get('column_name')

        sort_type = data.get('sort_type')

        filter = data.get('filter', {'ImageTitle': '', 'ImageCateName': '', 'ImageTags': ''})

        if column_name == '':
            all_course = Pictures.objects.filter(Q(ImageTitle__icontains=filter['ImageTitle']) & Q(
                ImageCateName__icontains=filter['ImageCateName']) & Q(
                ImageTags__icontains=filter['ImageTags'])).order_by('-id')
        else:
            if sort_type is None:
                all_course = Pictures.objects.filter(Q(ImageTitle__icontains=filter['ImageTitle']) & Q(
                    ImageCateName__icontains=filter['ImageCateName']) & Q(
                    ImageTags__icontains=filter['ImageTags'])).order_by('-id')
            else:
                if sort_type == 'descending':
                    sort_type = '-'
                elif sort_type == 'ascending':
                    sort_type = ''
                all_course = Pictures.objects.filter(Q(ImageTitle__icontains=filter['ImageTitle']) & Q(
                    ImageCateName__icontains=filter['ImageCateName']) & Q(
                    ImageTags__icontains=filter['ImageTags'])).order_by(
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
            data.append({
                'id': item.id,
                'ImageId': item.ImageId,
                'ImageTumb': "{0}?x-oss-process=image/resize,l_70,h_70/quality,q_100".format(item.ImageURL),  # 略缩图
                'ImageBigTumb': "{0}?x-oss-process=image/resize,l_600/quality,q_80".format(item.ImageURL),  # 缩放大图
                'ImageTitle': item.ImageTitle,
                'ImageDescription': item.ImageDescription,
                'ImageCate': {'ImageCateId': item.ImageCateId, 'ImageCateName': item.ImageCateName},
                'ImageSize': approximate_size(item.ImageSize),
                'ImageURL': item.ImageURL,
                'ImageTags': str_list(item.ImageTags),
                'ImageOriginalFileName': item.ImageOriginalFileName,
                'AddDate_Time': chinese_time(item.AddDate_Time),
                'UpDate_Time': chinese_time(item.UpDate_Time)
            })
        page_result["pageData"] = data
        page_result['total'] = total
        page_result['success'] = 'success'
        page_result['msg'] = '分页查询成功'
        return JsonResponse(page_result, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Edit_Pictures(request):
    if request.method == 'GET':
        id = int(request.GET.get('id'))
        picture = Pictures.objects.get(id=id)
        resp_picture = dict()
        resp_picture['id'] = picture.id
        resp_picture['ImageId'] = picture.ImageId
        resp_picture['ImageTitle'] = picture.ImageTitle
        from utils.aliyun_image_util import get_picture_category
        resp = get_picture_category(cateId=picture.ImageCateId)
        if resp.get('Category')['Level'] == 2:
            father_picture_cate = get_picture_category(cateId=resp.get('Category')['ParentId'])
            resp_picture['ImageCate'] = [father_picture_cate.get('Category'), resp.get('Category')]
            resp_picture['ImageCateLabel'] = father_picture_cate.get('Category')['CateName'] + ' / ' + \
                                             resp.get('Category')[
                                                 'CateName']
        else:
            resp_picture['ImageCate'] = [resp.get('Category')]
            resp_picture['ImageCateLabel'] = resp.get('Category')['CateName']
        resp_picture['ImageDescription'] = picture.ImageDescription
        resp_picture['ImageURL'] = picture.ImageURL
        resp_picture['ImageTumb'] = '{0}?x-oss-process=image/resize,l_600,s_600/quality,q_100'.format(picture.ImageURL)
        resp_picture['ImageSize'] = approximate_size(picture.ImageSize)
        resp_picture['ImageHeight'] = picture.ImageHeight
        resp_picture['ImageWidth'] = picture.ImageWidth
        resp_picture['ImageTags'] = str_list(picture.ImageTags)
        resp_picture['AddDate_Time'] = chinese_time(picture.AddDate_Time)
        resp_picture['UpDate_Time'] = chinese_time(picture.UpDate_Time)
        return JsonResponse({'success': 'success', 'data': resp_picture}, safe=False)

    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        logger(data)
        resp_picture = dict()
        picture = Pictures.objects.get(id=data.get('id'))
        picture.ImageTitle = data.get('ImageTitle')
        picture.ImageDescription = data.get('ImageDescription')
        Cate = data.get('ImageCate', [{'CateId': 1000061918, 'CateName': '未分类'}])[-1]
        picture.ImageCateId = Cate.get('CateId')
        picture.ImageCateName = Cate.get('CateName')
        if len(data.get('ImageTags')) != 0:
            picture.ImageTags = data.get('ImageTags')
        else:
            picture.ImageTags = ''
        try:
            from utils.aliyun_image_util import change_image
            change_result = change_image(data)
            if change_result is True:
                picture.save()
                picture = Pictures.objects.get(id=data.get('id'))
                resp_picture['id'] = picture.id
                resp_picture['ImageId'] = picture.ImageId
                from utils.aliyun_image_util import get_picture_category
                resp = get_picture_category(cateId=picture.ImageCateId)
                if resp.get('Category')['Level'] == 2:
                    father_picture_cate = get_picture_category(cateId=resp.get('Category')['ParentId'])
                    resp_picture['ImageCate'] = [father_picture_cate.get('Category'), resp.get('Category')]
                    resp_picture['ImageCateLabel'] = father_picture_cate.get('Category')['CateName'] + ' / ' + \
                                                     resp.get('Category')[
                                                         'CateName']
                else:
                    resp_picture['ImageCate'] = [resp.get('Category')]
                    resp_picture['ImageCateLabel'] = resp.get('Category')['CateName']
                resp_picture['ImageSize'] = approximate_size(picture.ImageSize)
                resp_picture['ImageHeight'] = picture.ImageHeight
                resp_picture['ImageWidth'] = picture.ImageWidth
                resp_picture['ImageType'] = picture.ImageType
                resp_picture['ImageURL'] = picture.ImageURL
                resp_picture['ImageTumb'] = "{0}?x-oss-process=image/resize,l_600,s_600/quality,q_100".format(
                    picture.ImageURL)
                resp_picture['AddDate_Time'] = chinese_time(picture.AddDate_Time)
                resp_picture['UpDate_Time'] = chinese_time(picture.UpDate_Time)
                resp_picture['ImageTitle'] = picture.ImageTitle
                resp_picture['ImageDescription'] = picture.ImageDescription
                resp_picture['ImageTags'] = str_list(picture.ImageTags)
                resp = {'success': 'success', 'data': resp_picture, 'msg': '图片编辑已保存！'}
            else:
                resp = {'success': 'failed', 'msg': '图片编辑保存失败！'}
        except SystemError:
            resp = {'success': 'failed', 'msg': '图片编辑保存失败！'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Pictures(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        logger(data)
        deleteitems = data.get('deleteitems')
        imageids = list()
        resp = dict()
        for item in deleteitems:
            imageids.append(item['ImageId'])
        try:
            delete_result = delete_image(imageids)
            if delete_result is True:
                for item in deleteitems:
                    Pictures.objects.filter(id=item['id']).delete()
                resp = {'success': 'success', 'msg': '图片删除完成！'}
            else:
                resp = {'success': 'failed', 'msg': '图片删除失败！'}
        except SystemError:
            resp = {'success': 'failed', 'msg': '图片删除失败！'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Get_Video_Cate(request):
    if request.method == 'GET':
        from utils.aliyun_video_util import get_video_category
        resp = get_video_category()
        resp_video_cate = list()
        if resp.get('SubTotal') > 0:
            for item in resp.get('SubCategories')['Category']:
                first_level = {'value': item, 'label': item['CateName'], 'children': list()}
                sub_resp = get_video_category(cateId=item['CateId'])
                if sub_resp.get('SubTotal') > 0:
                    for item_1 in sub_resp.get('SubCategories')['Category']:
                        second_level = {'value': item_1, 'label': item_1['CateName']}
                        first_level['children'].append(second_level)
                else:
                    first_level.pop('children')
                resp_video_cate.append(first_level)
        return JsonResponse({'resp_video_cate': resp_video_cate}, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Get_Videos(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        videocate = data.get('cate')
        print(data)
        if videocate == '':
            videos = Videos.objects.filter().order_by('-UpDate_Time')
        else:
            videos = Videos.objects.filter(VideoCateId=(videocate[-1])['CateId']).order_by('UpDate_Time')
        resp_videos = list()
        for item in videos:
            resp_videos.append({
                'id': item.id,
                'VideoCoverURLTumb': '{0}?x-oss-process=image/resize,l_20,s_20'.format(
                    item.VideoCoverURL),
                'VideoTitle': item.VideoTitle,
            })

        return JsonResponse({'Videos': resp_videos}, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def List_Videos(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/videos-list.html')

    if request.method == 'POST':
        if request.method == 'POST':
            data = request.body

            data = json.loads(data)

            logger(data)

            column_name = data.get('column_name')

            sort_type = data.get('sort_type')

            filter = data.get('filter', {'VideoTitle': '', 'VideoCateName': '', 'VideoTags': ''})

            if column_name == '':
                all_course = Videos.objects.filter(Q(VideoTitle__contains=filter['VideoTitle']) & Q(
                    VideoCateName__icontains=filter['VideoCateName']) & Q(
                    VideoTags__icontains=filter['VideoTags'])).order_by('-id')
            else:
                if sort_type is None:
                    all_course = Videos.objects.filter(Q(VideoTitle__icontains=filter['VideoTitle']) & Q(
                        VideoCateName__icontains=filter['VideoCateName']) & Q(
                        VideoTags__icontains=filter['VideoTags'])).order_by('-id')
                else:
                    if sort_type == 'descending':
                        sort_type = '-'
                    elif sort_type == 'ascending':
                        sort_type = ''
                    all_course = Videos.objects.filter(Q(VideoTitle__icontains=filter['VideoTitle']) & Q(
                        VideoCateName__icontains=filter['VideoCateName']) & Q(
                        VideoTags__icontains=filter['VideoTags'])).order_by(
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
                data.append({
                    'id': item.id,
                    'VideoId': item.VideoId,
                    'VideoCoverURLBigTumb': '{0}?x-oss-process=image/resize,l_600/quality,q_80'.format(
                        item.VideoCoverURL),
                    'VideoCoverURLTumb': '{0}?x-oss-process=image/resize,m_lfit,h_70/quality,q_100'.format(
                        item.VideoCoverURL),
                    'VideoTitle': item.VideoTitle,
                    'VideoDuration': timeConvert(item.VideoDuration),
                    'VideoDescription': item.VideoDescription,
                    'VideoCate': {'VideoCateId': item.VideoCateId, 'VideoCateName': item.VideoCateName},
                    'VideoSize': approximate_size(item.VideoSize),
                    'VideoTags': str_list(item.VideoTags),
                    'AddDate_Time': chinese_time(item.AddDate_Time),
                    'UpDate_Time': chinese_time(item.UpDate_Time)
                })
            page_result["pageData"] = data
            page_result['total'] = total
            page_result['success'] = 'success'
            page_result['msg'] = '分页查询成功'
            return JsonResponse(page_result, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Edit_Video(request):
    if request.method == 'GET':
        id = int(request.GET.get('id'))
        video = Videos.objects.get(id=id)
        resp_video = dict()
        resp_video['id'] = video.id
        resp_video['VideoId'] = video.VideoId
        resp_video['VideoTitle'] = video.VideoTitle
        from utils.aliyun_video_util import get_video_category
        resp = get_video_category(cateId=video.VideoCateId)
        if resp.get('Category')['Level'] == 2:
            father_video_cate = get_video_category(cateId=resp.get('Category')['ParentId'])
            resp_video['VideoCate'] = [father_video_cate.get('Category'), resp.get('Category')]
            resp_video['VideoCateLabel'] = father_video_cate.get('Category')['CateName'] + ' / ' + resp.get('Category')[
                'CateName']
        else:
            resp_video['VideoCate'] = [resp.get('Category')]
            resp_video['VideoCateLabel'] = resp.get('Category')['CateName']
        resp_video['VideoDescription'] = video.VideoDescription
        resp_video['VideoCoverURLTumb'] = '{0}?x-oss-process=image/resize,l_600,s_600/quality,q_100'.format(
            video.VideoCoverURL)
        resp_video['VideoSize'] = approximate_size(video.VideoSize)
        resp_video['VideoDuration'] = timeConvert(video.VideoDuration)
        resp_video['VideoTags'] = str_list(video.VideoTags)
        resp_video['AddDate_Time'] = chinese_time(video.AddDate_Time)
        resp_video['UpDate_Time'] = chinese_time(video.UpDate_Time)
        return JsonResponse({'success': 'success', 'data': resp_video}, safe=False)

    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        logger(data)
        resp_video = dict()
        video = Videos.objects.get(id=data.get('id'))
        video.VideoTitle = data.get('VideoTitle')
        video.VideoDescription = data.get('VideoDescription')
        Cate = data.get('VideoCate', [{'CateId': 1000061920, 'CateName': '未分类'}])
        Cate = Cate[-1]
        video.VideoCateId = Cate.get('CateId')
        video.VideoCateName = Cate.get('CateName')
        if len(data.get('VideoTags')) != 0:
            video.VideoTags = data.get('VideoTags')
        else:
            video.VideoTags = ''
        try:
            from utils.aliyun_video_util import change_video
            change_result = change_video(data)
            if change_result is True:
                video.save()
                video = Videos.objects.get(id=data.get('id'))
                resp_video['id'] = video.id
                resp_video['VideoId'] = video.VideoId
                from utils.aliyun_video_util import get_video_category
                resp = get_video_category(cateId=video.VideoCateId)
                if resp.get('Category')['Level'] == 2:
                    father_video_cate = get_video_category(cateId=resp.get('Category')['ParentId'])
                    resp_video['VideoCate'] = [father_video_cate.get('Category'), resp.get('Category')]
                    resp_video['VideoCateLabel'] = father_video_cate.get('Category')['CateName'] + ' / ' + \
                                                   resp.get('Category')['CateName']
                else:
                    resp_video['VideoCate'] = [resp.get('Category')]
                    resp_video['VideoCateLabel'] = resp.get('Category')['CateName']
                resp_video['VideoSize'] = approximate_size(video.VideoSize)
                resp_video['VideoDuration'] = timeConvert(video.VideoDuration)
                resp_video['VideoCoverURLTumb'] = "{0}?x-oss-process=image/resize,l_600,s_600/quality,q_100".format(
                    video.VideoCoverURL)
                resp_video['AddDate_Time'] = chinese_time(video.AddDate_Time)
                resp_video['UpDate_Time'] = chinese_time(video.UpDate_Time)
                resp_video['VideoTitle'] = video.VideoTitle
                resp_video['VideoDescription'] = video.VideoDescription
                resp_video['VideoTags'] = str_list(video.VideoTags)
                resp = {'success': 'success', 'data': resp_video, 'msg': '视频编辑已保存！'}
            else:
                resp = {'success': 'failed', 'msg': '视频编辑保存失败！'}
        except SystemError:
            resp = {'success': 'failed', 'msg': '视频编辑保存失败！'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Delete_Video(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        logger(data)
        deleteitems = data.get('deleteitems')
        videoids = list()
        resp = dict()
        for item in deleteitems:
            videoids.append(item['VideoId'])
        try:
            delete_result = delete_video(videoids)
            if delete_result is True:
                for item in deleteitems:
                    Videos.objects.filter(id=item['id']).delete()
                resp = {'success': 'success', 'msg': '视频删除完成！'}
            else:
                resp = {'success': 'failed', 'msg': '视频删除失败！'}
        except SystemError:
            resp = {'success': 'failed', 'msg': '视频删除失败！'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Pre_View_Video(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        logger(data)
        videoid = data.get('videoid')
        playAuth = get_video_playauth(videoid)
        playauth = playAuth["PlayAuth"]
        return JsonResponse({'success': 'success', 'data': {'playauth': playauth}}, safe=False)


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Pictures_Upload(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/upload-pictures.html')


@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Videos_Upload(request):
    if request.method == 'GET':
        return render(request, 'PC/admin/upload-videos.html')

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Create_Upload_image(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        title = data.get('title')
        from utils.aliyun_image_util import create_upload_image
        resp = create_upload_image(title)
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Create_Upload_Video(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        title = data.get('title')
        name = data.get('name')
        from utils.aliyun_video_util import create_upload_video
        resp = create_upload_video(title, name)
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Refresh_Upload_Video(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        videoid = data.get('videoid')
        from utils.aliyun_video_util import refresh_upload_video
        resp = refresh_upload_video(videoid)
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Set_Pictures_Cate(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        pictures = data.get('images')
        cate = data.get('cate', [{'CateId': 1000061918, 'CateName': '未分类'}])
        if cate == [] or cate == "":
            cate = [{'CateId': 1000061918, 'CateName': '未分类'}]
        cate = cate[-1]
        # print(pictures, cate)
        try:
            from utils.aliyun_image_util import change_images_cate
            for item in pictures:
                picture = Pictures.objects.get(id=item['id'])
                picture.ImageCateId = cate.get('CateId')
                picture.ImageCateName = cate.get('CateName')
                picture.save()
            change_images_cate(pictures, cate)
            resp = {'success': 'success'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed'}
        return JsonResponse(resp, safe=False)

@login_required(login_url='/singdl_admin/user_login/')
@superuser_only
def Set_Videos_Cate(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        videos = data.get('images')
        cate = data.get('cate', [{'CateId': 1000061920, 'CateName': '未分类'}])
        if cate == [] or cate == "":
            cate = [{'CateId': 1000061920, 'CateName': '未分类'}]
        cate = cate[-1]
        print(videos, cate)
        try:
            from utils.aliyun_video_util import change_videos_cate
            for item in videos:
                video = Videos.objects.get(id=item['id'])
                video.VideoCateId = cate.get('CateId')
                video.VideoCateName = cate.get('CateName')
                video.save()
            change_videos_cate(videos, cate)
            resp = {'success': 'success'}
        except Exception as e:
            print(e)
            resp = {'success': 'failed'}
        return JsonResponse(resp, safe=False)

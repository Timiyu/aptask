"""SingdlService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from admin.views import courses as Courses
from admin.views import blog as Blogs
from admin.views import resources as Resources
from admin.views import index as Index
from users.views import *
from admin.views import website as Website

app_name = 'admin'
urlpatterns = [
    path('', Index.Index.as_view(), name='index'),
    path('user_login/', Login.as_view(), name='user_login'),
    path('user_logout/', logout, name='user_logout'),
    path('list_courses_category', Courses.List_Category, name='list_courses_category'),
    path('get_all_category', Courses.Get_All_Category, name='get_all_category'),
    path('get_category', Courses.Get_Category, name='get_category'),
    path('add_category', Courses.Add_Category, name='add_category'),
    path('delete_category', Courses.Delete_Category, name='delete_category'),
    path('delete_selected_category', Courses.Delete_Selected_Category, name='delete_selected_category'),
    path('edit_category', Courses.Edit_Category, name='edit_category'),
    path('get_course', Courses.Get_Course, name='get_course'),
    path('list_courses', Courses.List_Courses, name='list_courses'),
    path('add_courses', Courses.Add_Course, name='add_courses'),
    path('add_capital', Courses.Creat_Capitals, name='add_capital'),
    path('edit_capital', Courses.Edit_Capital, name='edit_capital'),
    path('delete_capital', Courses.Delete_Capital, name='delete_capital'),
    path('add_lesson', Courses.Creat_Lessons, name='add_lesson'),
    path('delete_lesson', Courses.Delete_Lesson, name='delete_lesson'),
    path('edit_lesson', Courses.Edit_Lesson, name='edit_lesson'),
    path('edit_course', Courses.Edit_Course, name='edit_course'),
    path('delete_courses', Courses.Delete_Course, name='delete_courses'),
    path('delete_selected_courses', Courses.Delete_Selected_Courses, name='delete_selected_courses'),
    path('list_blogs_category', Blogs.List_Category, name='list_blogs_category'),
    path('blogs_list', Blogs.List_Articles, name='blogs_list'),
    path('get_all_blog_category', Blogs.Get_All_Category, name='get_all_blog_category'),
    path('get_blog_category', Blogs.Get_Category, name='get_blog_category'),
    path('add_blog_category', Blogs.Add_Category, name='add_blog_category'),
    path('edit_blog_category', Blogs.Edit_Category, name='edit_blog_category'),
    path('delete_blog_category', Blogs.Delete_Category, name='delete_blog_category'),
    path('delete_selected_blog_category', Blogs.Delete_Selected_Category, name='delete_selected_blog_category'),
    path('get_blog', Blogs.Get_Article, name='get_blog'),
    path('add_blog', Blogs.Add_Article, name='add_blog'),
    path('edit_blog', Blogs.Edit_Article, name='edit_blog'),
    path('delete_blog', Blogs.Delete_Article, name='delete_blog'),
    path('delete_selected_blog', Blogs.Delete_Selected_Article, name='delete_selected_blog'),
    path('upload_blog_image', Blogs.Upload_Image, name='upload_blog_imgae'),
    path('get_picture_cate', Resources.Get_Picture_Cate, name='get_picture_cate'),
    path('list_pictures', Resources.List_Pictures, name='list_pictures'),
    path('set_pictures_cate', Resources.Set_Pictures_Cate, name='set_pictures_cate'),
    path('get_pictures_this_type', Resources.Get_Picture_This_Type, name='get_pictures_this_type'),
    path('edit_pictures', Resources.Edit_Pictures, name='edit_pictures'),
    path('upload_pictures', Resources.Pictures_Upload, name='upload_pictures'),
    path('create_upload_image', Resources.Create_Upload_image, name='create_upload_image'),
    path('create_upload_video', Resources.Create_Upload_Video, name='create_upload_video'),
    path('refresh_upload_video', Resources.Refresh_Upload_Video, name='refresh_upload_video'),
    path('upload_videos', Resources.Videos_Upload, name='upload_videos'),
    path('delete_picture', Resources.Delete_Pictures, name='delete_pictures'),
    path('get_video_cate', Resources.Get_Video_Cate, name='get_video_cate'),
    path('get_videos', Resources.Get_Videos, name='get_videos'),
    path('set_videos_cate', Resources.Set_Videos_Cate, name='set_videos_cate'),
    path('list_videos', Resources.List_Videos, name='list_videos'),
    path('play_video', Resources.Pre_View_Video, name='pre_view_video'),
    path('edit_video', Resources.Edit_Video, name='edit_video'),
    path('delete_videos', Resources.Delete_Video, name='delete_videos'),
    path('list_users', Users.ListUser.as_view(), name='list_users'),
    path('list_client_history', Website.list_client_history, name='list_client_history'),
    path('delete_logs', Website.delete_opt_logs, name='delete_historys'),
]

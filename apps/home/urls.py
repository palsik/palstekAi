# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('profile_sbt', views. profileView, name='submit-profile'),
    path('blog-topic', views.blogTopic, name='frm-gen-blogt'),
    path('blog-section', views.blogSections, name='blogSections'),

    # Saving blog Topic for future use
    path('save-blog-topic/<str:uniqueId>', views.deleteBlogTopic, name='delete-blog-topic'),

    path('gen-frm-blog-topic/<str:uniqueId>', views.genBlogFrmsvtopic, name='gen-blog-frm-topic'),

    path('save-blog-topic/<str:blogTopic>', views.saveBlogTopic, name='save-blog-topic'),

    path('use-blog-topic/<str:blogTopic>', views.useBlogTopic, name='use-blog-topic'),

    # using request to submit profile
    path('view-generated-blog/<slug:slug>', views.viewGeneratedBlog, name='view-generated-blog'),




    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

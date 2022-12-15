# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import profile

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from numpy.ma import count

from apps.home.models import *
from apps.home.forms import *

from apps.home.functions import *


@login_required(login_url="/login/")
def index(request):
    emptyBlogs = []
    completedBlogs = []

    blogs = Blog.objects.filter(profile=request.user.Profile)
    for blog in blogs:
        sections = BlogSection.objects.filter(blog=blog)
        if sections.exists():
            blog.words = len(blog.title.split(' '))
            completedBlogs.append(blog)
        else:
            emptyBlogs.append(blog)
    context = {'segment': 'index'}

    context['numBlogs'] = 4
    context['monthCount'] = 1242
    context['emptyBlogs'] = emptyBlogs
    context['completedBlogs'] = completedBlogs

    html_template = loader.get_template('home/index2.html')
    # html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def profileView(request):
    context = {}
    # user = profile.user

    if request.method == 'GET':
        form = profileForm(instance=request.user.Profile)
        context['form'] = form
        return render(request, 'home/profile.html', context)

    if request.method == 'POST':
        form = profileForm(request.POST, instance=request.user.Profile)

        if form.is_valid():
            # form.username = form.cleaned_data['username'],
            # form. = form.cleaned_data['email'],
            form.firstname = form.cleaned_data['firstname'],
            form.lastname = form.cleaned_data['lastname'],
            form.address = form.cleaned_data['address'],
            form.aboutinfo = form.cleaned_data['aboutinfo']

            print()

            form.save()
            return redirect('submit-profile')

    return render(request, 'home/profile.html')


@login_required(login_url="/login/")
def blogTopic(request):
    context = {}

    if request.method == 'POST':
        # Retrieve the bogIdea String from the submitted FORM from request.POST
        blogIdea = request.POST['blogIdea']
        # saving the blodIdea string in the session for later route access
        request.session['blogIdea'] = blogIdea
        keywords = request.POST['keywords']
        request.session['keywords'] = keywords
        audience = request.POST['audience']
        request.session['audience'] = audience

        blogTopics = generatedBlogTopicIdeas(blogIdea, audience, keywords)
        if len(blogTopics) > 0:
            request.session['blogTopics'] = blogTopics
            return redirect('blogSections')
        else:
            messages.error("Ops we could not generate blog Ideas, Please try again")
            return redirect('frm-gen-blogt')

    return render(request, 'home/gen-blog.html')


@login_required(login_url="/login/")
def blogSections(request):
    if 'blogTopics' in request.session:
        pass
    else:
        messages.error(request, "Start by Creating blog topic Ideas")
        return redirect('blog-topic')

    context = {}
    blogTopics = request.session['blogTopics']
    context['blogTopics'] = blogTopics

    print(blogTopics)

    print("The size of blogTopic after receiving through session \n")
    print(len(blogTopics))

    # a_list = blogTopics.split('/n')

    if len(blogTopics) > 0:
        for blog in blogTopics:
            print(blog)

    return render(request, 'home/blog-Sections.html', context)


@login_required(login_url="/login/")
def saveBlogTopic(request, blogTopic):
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session and \
            'blogTopics' in request.session:
        blog = Blog.objects.create(
            title=blogTopic,
            blogIdea=request.session['blogIdea'],
            keywords=request.session['keywords'],
            audience=request.session['audience'],
            profile=request.user.Profile, )
        blog.save()

        blogTopics = request.session['blogTopics']
        blogTopics.remove(blogTopic)

        request.session['blogTopics'] = blogTopics

        return redirect('blogSections')
    else:
        return redirect('frm-gen-blogt')

        # context = {}
        # blogTopics = request.session['blogTopics']
        # context['blogTopics'] = blogTopics


@login_required(login_url="/login/")
def deleteBlogTopic(request, uniqueId):
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
        if blog.profile == request.user.Profile:
            blog.delete()
            return redirect('home')
        else:
            messages.error(request, "Access Denied")
            return redirect('home')
    except:
        messages.error(request, "Blog not found")
        return redirect('home')


# def profile(request):
#     contex = {}
#
#     if request.method == 'GET':
#         form = profileForm(request)
#         contex['form'] = form
#         return render(request, 'home/profile.html', contex)
#
#     if request.method == 'POST':
#         form = profileForm(request.POST)
#         if form.is_valid():
#             pass
#         if form.is_valid():
#             pass
#             # form.save()
#
#     return render(request, 'home/profile.html', contex)
#
#     context = {}
#
#     return render(request, 'home/profile.html')


@login_required(login_url="/login/")
def useBlogTopic(request, blogTopic):
    context = {}
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session:
        # Start by saving the Blog
        blog = Blog.objects.create(
            title=blogTopic,
            blogIdea=request.session['blogIdea'],
            keywords=request.session['keywords'],
            audience=request.session['audience'],
            profile=request.user.Profile, )
        blog.save()

        blogSections = generatedBlogSectionTitles(blogTopic, request.session['audience'], request.session['keywords'])
    else:
        return redirect('frm-gen-blogt')

    if len(blogSections) > 0:
        # Adding the sections to the sessions
        request.session['blogSections'] = blogSections

        # Adding the sections to the context
        context['blogSections'] = blogSections
    else:
        messages.error(request, 'Oops something went wrong try again')
        return redirect('frm-gen-blogt')

    if request.method == 'POST':
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:
                print(val)
                # Generating blogSection details
                sectionTopics = val
                section = generatedBlogSectionDetails(blogTopic, sectionTopics, request.session['audience'],
                                                      request.session['keywords'])
                # Create Database Record
                bloSec = BlogSection.objects.create(
                    title=val,
                    body=section,
                    blog=blog)
                bloSec.save()
                # # print(section)

        return redirect('view-generated-blog', slug=blog.slug)

    return render(request, 'home/select_blog_sections.html', context)

    # blog = Blog.objects.create(
    #     title=blogTopic,
    #     blogIdea=request.session['blogIdea'],
    #     keywords=request.session['keywords'],
    #     audience=request.session['audience'],
    #     profile=request.user.Profile, )
    # blog.save()


@login_required(login_url="/login/")
def genBlogFrmsvtopic(request, uniqueId):
    context = {}

    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(request, "Blog not found")
        return redirect('home')

    blogSections = generatedBlogSectionTitles(blog.title, blog.audience, blog.keywords)

    if len(blogSections) > 0:
        # Adding the sections to the sessions
        request.session['blogSections'] = blogSections

        # Adding the sections to the context
        context['blogSections'] = blogSections
    else:
        messages.error(request, 'Oops something went wrong try again')
        return redirect('frm-gen-blogt')

    if request.method == 'POST':
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:
                print(val)
                # Generating blogSection details
                sectionTopics = val
                section = generatedBlogSectionDetails(blog.title, sectionTopics, blog.audience, blog.keywords)
                # Create Database Record
                bloSec = BlogSection.objects.create(
                    title=val,
                    body=section,
                    blog=blog)
                bloSec.save()
                # # print(section)

        return redirect('view-generated-blog', slug=blog.slug)

    return render(request, 'home/select_blog_sections.html', context)

    # blog = Blog.objects.create(
    #     title=blogTopic,
    #     blogIdea=request.session['blogIdea'],
    #     keywords=request.session['keywords'],
    #     audience=request.session['audience'],
    #     profile=request.user.Profile, )
    # blog.save()


@login_required(login_url="/login/")
def viewGeneratedBlog(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        messages.error(request, 'Oops something went wrong try again')
        return redirect('frm-gen-blogt')
    # Fetch the Created Sections for the Blog
    blogSections = BlogSection.objects.filter(blog=blog)

    context = {}
    context['blog'] = blog
    context['blogSections'] = blogSections

    return render(request, 'home/view-generated-blog.html', context)

from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from taggit.models import Tag

from .forms import SignUpForm, SignInForm, FeedBackForm
from .models import Post



class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request, 'myblog/home.html', context={
                'page_obj': page_obj
            })


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-created_at')[:3]

        return render(
            request, 'myblog/post_detail.html', context={
                'post': post,
                'common_tags': common_tags,
                'last_posts': last_posts,
            })


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(
            request, 'myblog/signup.html', context={
                'form': form,
            })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')

        return render(
            request, 'myblog/signup.html', context={
                'form': form,
            })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            return render(request, 'myblog/signin.html', context={
                'form': form,
            })


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'myblog/contact.html', context={
            'form': form,
            'title': '???????????????? ??????',
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'???? {name} | {subject}', message, email, ['al_berhmiller@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid Header')
            return HttpResponseRedirect('success')
        return render(request, 'myblog/contact.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myblog/success.html', context={
            'title': '??????????????'
        })


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        results = ''
        if query:
            results = Post.objects.filter(Q(h1__contains=query) | Q(content__contains=query))

        paginator = Paginator(results, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myblog/search.html', context={
            'title': '??????????',
            'results': page_obj,
            'count': paginator.count
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'myblog/tag.html', context={
            'title': f'#?????? {tag}',
            'posts': posts,
            'common_tags': common_tags,
        })

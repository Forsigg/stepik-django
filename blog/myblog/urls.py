from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from .views import MainView, PostDetailView, SignUpView, SignInView, FeedBackView, SuccessView, SearchResultsView, \
    TagView

urlpatterns = [
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('contact/success/', SuccessView.as_view(), name='success'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('tag/<slug:slug>', TagView.as_view(), name='tag'),
    path('', MainView.as_view(), name='index'),
]
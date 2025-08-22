from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),                      # Home page
    path('blog/', views.post_list, name='blog'),            # Blog page
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),  # Blog detail page
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
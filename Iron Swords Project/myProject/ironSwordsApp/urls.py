from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import HeroListView


urlpatterns = [
    path('', views.home, name='home'),
    path('add-hero/', views.add_hero, name='add_hero'),
    path('login/', views.login_view, name='login'),
    path('transition/', views.transition, name='transition'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('forgot-password-submit/', views.forgot_password_submit, name='forgot_password_submit'),
    path('create-account/', views.create_account_view, name='create_account'),
    path('register/', views.register, name='register'),
    path('hall-of-fame/', views.hall_of_fame, name='hall_of_fame'),
    path('join_form_for_hero/', views.join_form_for_hero, name='join_form_for_hero'),
    path('edit_hero/<int:hero_id>/', views.edit_hero, name='edit_hero'),
    path('delete_hero/<int:hero_id>/', views.delete_hero, name='delete_hero'),
    path('join_form/', views.join_form, name='join_form'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('heroes/', HeroListView.as_view(), name='hero_list'),
    

    # Class-based views
    path('hero/new/', views.HeroCreateView.as_view(), name='hero-create'),
    path('hero/<int:pk>/edit/', views.HeroUpdateView.as_view(), name='hero-update'),
    path('hero/<int:pk>/delete/', views.HeroDeleteView.as_view(), name='hero-delete'),
    path('hero/<int:hero_id>/', views.hero_detail, name='hero_detail'),
]


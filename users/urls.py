from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # path() для страницы регистрации нового пользователя
    # полный адрес - "auth/signup".
    # префикс "auth/" обрабатывается в головном urls.py
    path('signup/', views.SignUP.as_view(), name='signup'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/',
         auth_views.LogoutView.
         as_view(template_name='registration/logout.html'),
         name='logout'),

    path('password_change/',
         auth_views.PasswordChangeView.
         as_view(template_name='registration/_password_change_form.html'),
         name='password_change'),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.
         as_view(template_name='registration/_password_change_done.html'),
         name='password_change_done'),

    path('password_reset/',
         auth_views.PasswordResetView.
         as_view(template_name='registration/_password_reset_form.html'),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.
         as_view(template_name='registration/_password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<str:uidb64>/<str:token>/',
         auth_views.PasswordResetConfirmView.
         as_view(template_name='registration/_password_change_form.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.
         as_view(template_name='registration/_password_change_done.html'),
         name='password_reset_complete'),
]

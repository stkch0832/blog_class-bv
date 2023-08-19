from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/<int:user_id>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:user_id>/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

    # auth
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),

]

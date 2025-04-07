from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'account'

urlpatterns = [
    path('token', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('sign-up/job-owner/', views.JobOwnerSignUpView.as_view(), name='sign-up-job-owner'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('user/profile/update/', views.UpdateProfileView.as_view(), name='update-user-profile'),
    path('user/detail/', views.UserDetailView.as_view(), name='update-detail'),
    path('user/logout/', views.LogoutView.as_view(), name='logout'),

]

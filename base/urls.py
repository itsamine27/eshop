from django.urls import path,include
from .views import Sign_Up_User,Log_In_User, Log_Out_User, NewProfile,HomeView


urlpatterns=[
    
    path("signup/", Sign_Up_User.as_view(), name='signup'),
    path("login/", Log_In_User.as_view(), name="login"),
    path("logout/", Log_Out_User.as_view(), name="logout"),
    path("profile_creation/", NewProfile.as_view(), name="create_company_profile"),
    
] 
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('delete-account/', views.delete_account, name='delete_account'),

    path('logout/',views.logout_view,name='logout'),
    path('login/',views.login_view,name='login'),
]
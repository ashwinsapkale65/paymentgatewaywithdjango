from tracemalloc import start
from unicodedata import name
from django import views
from django.contrib import admin
from django.urls import path , include
from start import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('billing',views.billing,name='billing'),
    path('sucess',views.sucess,name='sucess'),
    path('alreadydone',views.alreadydone,name='alreadydone'),
    path('login_view',views.login_view,name='login_view'),
    path('admindashboard',views.admindashboard,name='admindashboard'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('billtemplate',views.billtemplate,name='billtemplate'),
    path('studentspaymentpending',views.studentspaymentpending,name='studentspaymentpending')
    
  
    
]
"""lekshmiprj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from lekshmiapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.index, name="index"),
    path("simplecontrolview", views.formwithcontrolsview, name="simplecontrolview"),
    path("simpleformclassview", views.formwithformclass, name="simplefrmview"),
    path(
        "simpleformwithmodel/",
        views.formwithmodelandclassichtml,
        name="simplefrmmodelview",
    ),
    path(
        "search/",
        views.search,
        name="mysearch",
    ),
    path(
        "search1/",
        views.search1,
        name="mysearch1",
    ),
    path(
        "search2/",
        views.search2,
        name="mysearch2",
    ),
path('createstudent',views.CreateStudent,name="createstudent"),
path('traversal',views.manytomanytraversal,name="traversal"),
    path(
        "simpleformwithmodel/<str:fname>",
        views.formwithmodelandclassichtml,
        name="nishababu",
    ),
    path(
        "babu",
        views.babu,
        name="babu",
    ),
    path("examplemodelform", views.formwithmodelform, name="examplemodelform"),
    path("emplist", views.formemplist, name="emplist"),
    path('nishalist',views.nishafunc,name="nishalist"),
    path('CreateCity',views.CreateCity,name='createcity'),
    # path("", views.index, name="simpleview"),
    #path("", views.rdbuttonCheck, name="rdbuttonCheck"),
    path("", views.testcustomvalidators, name="testcustomvalidators"),
    path("commonfunc",views.commonfunc,name="commonfunc"),
    path("iamfromfetch",views.iamfromfetch,name="iamfromfetch"),
    
    
]

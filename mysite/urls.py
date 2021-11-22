"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf.urls import url
from mysite import settings
from index import views as in_views
from django.views import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',in_views.main),


    path('index/', include('index.urls'),name='index'),
    path('account/', include('account.urls'), name='account'),
    path('outPut/',in_views.outPut),
    path('outPutPage/',in_views.outPutPage),
    path('outPutData/',in_views.outPutData),


    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT},name='static'),
    url(r'^media/(?P<path>.*)$', static.serve, {"document_root": settings.MEDIA_ROOT}),

]
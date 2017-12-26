"""SurepayPET URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from project import views as project_views
from project.views import ProjectList, AjaxHardwareModels

# Uncomment the next two lines to enable the admin:
# import xadmin
# xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
# from xadmin.plugins import xversion
# xversion.register_models()

urlpatterns = [
    # url(r'^$', project_views.index, name='home'),
    # url(r'projects', ProjectList.as_view()),
    # url(r'^add/((?:-|\d)+)/((?:-|\d)+)/$', project_views.add, name='add'),
    #url(r'xadmin/', xadmin.site.urls, name='xadmin'),
    # url(r'^index/$',project_views.index, name='select_index') ,
    # url(r'^getdata/$', project_views.getdata, name='getdata'),
    url(r'^getrecordsize/$', project_views.getRecordSize, name='getrecordsize'),
    url(r'^getotherappinformation/$', project_views.getOtherApplicationInformation, name='getotherappinformation'),
    # url(r'^province_to_city/$', project_views.province_to_city, name='province_to_city'),

    url(r'^ajax/chained-hardware-models/$', AjaxHardwareModels.as_view(), name='ajax_hardware_models'),

    # url(r'^map/$',project_views.Map, name='Map'),
    # url(r'^GetCityData/$',project_views.Return_City_Data, name='GetCityData'),
    # url(r'^GetCountryData/$',project_views.Return_Country_Data, name='GetCountryData'),

    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
]

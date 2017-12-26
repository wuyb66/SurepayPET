from django.shortcuts import render
from django.views.generic import ListView
from .models import Project

# from xadmin.plugins.actions import BaseActionView
# from xadmin.views.base import filter_hook, ModelAdminView
from django.template.response import TemplateResponse
from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers, urlresolvers

from service.models import CurrentRelease

from . import forms
from .models import Project, TrafficInformation, WorkingProject, FeatureConfiguration, \
    ProjectInformation, ApplicationConfiguration
from hardware.models import HardwareModel, HardwareType
from service.models import DBInformation, FeatureDBImpact, FeatureName, ApplicationName
from .forms import ProjectForm1

import json

from clever_selects.views import ChainedSelectChoicesView


# Create your views here.

# def province_to_city(request):
#     province = request.GET.get('province')
#     ret = []
#     if province:
#         for city in City.objects.filter(parent__id=province):
#             ret.append(dict(id=city.id, value=str(city)))
#     if len(ret) != 1:
#         ret.insert(0, dict(id='', value='---'))
#     return HttpResponse(json.dumps(ret), content_type='application/json')
#
# def Map(request):
#     return render_to_response("Project/project_list2.html")
#     #return HttpResponse("Hello!")
#
# Place_dict = {
#     "GuangDong":{
#         "GuangZhou":["PanYu","HuangPu","TianHe"],
#         "QingYuan":["QingCheng","YingDe","LianShan"],
#         "FoShan":["NanHai","ShunDe","SanShui"]
#     },
#     "ShanDong":{
#         "JiNan":["LiXia","ShiZhong","TianQiao"],
#         "QingDao":["ShiNan","HuangDao","JiaoZhou"]
#     },
#     "HuNan":{
#         "ChangSha":["KaiFu","YuHua","WangCheng"],
#         "ChenZhou":["BeiHu","SuXian","YongXian"]
#     }
# }
#
# def Return_City_Data(request):
#     province = request.GET['Province']
#     print(province)
#     City_list = []
#     for city in Place_dict[province]:
#         City_list.append(city)
#     return HttpResponse(json.dumps(City_list))
#
# def Return_Country_Data(request):
#     province,city = request.GET['Province'],request.GET['City']
#     print(province,city)
#     Country_list = Place_dict[province][city]
#     return HttpResponse(json.dumps(Country_list))

# def index(request):
#     if request.method == 'POST':
#         form = SelectForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(urlresolvers.reverse('select_index'))
#         else:
#             return HttpResponse('error')
#     else:
#         pro = Province.objects.all()
#         se = SelectP.objects.all()
#         return render(request, 'Project/project_list.html', {'province':pro,'select':se})


# def getdata(request):
#     pk = request.GET['pk']
#     province = get_object_or_404(Province, pk=pk)
#     citys = province.city_set.all()
#     data = serializers.serialize('json', citys)
#     return HttpResponse(data, content_type='application/json')

# Create your views here.
# def index(request):
#     currentRelease_list = CurrentRelease.objects.all()
#     releaseName = currentRelease_list[0].name
#     context = {'releaseName':releaseName}
#     title = 'Surepay Engineering Tool '
#
#     site_title = title + releaseName
#     #return render(request, 'home.html', context)
#
#     #return render(request, 'xadmin/views/model_list.html', context)
#     context.update(
#         {
#             'title' : title,
#             'site_title' : site_title,
#             # 'login': forms.LoginForm(),
#             # 'registration': forms.RegistrationForm(),
#             # 'checkout': forms.CheckoutForm(),
#             # 'order': forms.OrderForm(),
#             # 'comment': forms.CommentForm(),
#             # 'bank': forms.BankForm(),
#         }
#     )
#     return render(request, 'Project\project_list.html', context)

# def index(request):
#     return render(request, 'Project\project_list.html')


def add(request, a, b):
    if request.is_ajax():
        ajax_string = 'ajax request: '
    else:
        ajax_string = 'not ajax request: '
    c = int(a) + int(b)
    r = HttpResponse(ajax_string + str(c))
    return r
def getRecordSize(request):
    pk = request.GET['pk']
    memberGroupOption = request.GET['memberGroupOption']
    dbInformation = get_object_or_404(DBInformation, pk=pk)
    recordSize = dbInformation.recordSize
    refDBFactor = getRefDBFactor(dbInformation.db, memberGroupOption)
    subscriberNumber = getSubscriberNumber(memberGroupOption)
    data = {'RecordSize':recordSize, 'RefDBFactor':refDBFactor, 'SubscriberNumber':subscriberNumber}
    return HttpResponse(json.dumps(data), content_type='application/json')
def getRefDBFactor(DB, memberGroupOption):
    featureDBImpactList = FeatureDBImpact.objects.all().filter(
        dbName=DB,
    )
    refDBFactor = 0
    if memberGroupOption == 'Member':
        for featureDBImpact in featureDBImpactList:
            refDBFactor += featureDBImpact.memberImpactFactor
    else:
        for featureDBImpact in featureDBImpactList:
            refDBFactor += featureDBImpact.groupImpactFactor
    return refDBFactor
def getSubscriberNumber(memberGroupOption):
    if WorkingProject.objects.all().count() > 0:
        trafficInformationList = TrafficInformation.objects.all().filter(
            project=WorkingProject.objects.all()[0].project
        )
        if trafficInformationList.count() > 0:
            activeSubscriber = trafficInformationList[0].activeSubscriber
        else:
            activeSubscriber = 0
        if memberGroupOption == 'Member':
            return activeSubscriber
        else:
            featureNameList = FeatureName.objects.all().filter(
                name='Online Hierarchy',
            )
            if featureNameList.count() > 0:
                penetrationOLH = FeatureConfiguration.objects.all().filter(
                    project=WorkingProject.objects.all()[0].project,
                    feature=featureNameList[0],
                )
            else:
                penetrationOLH = 0
            return activeSubscriber * penetrationOLH
    else:
        return 0


def getOtherApplicationInformation(request):
    activeSubscriber = 0
    inactiveSubscriber = 0
    trafficTPS = 0
    application_id = request.GET['pk']
    applicationName = get_object_or_404(ApplicationName, pk=application_id)

    if (applicationName.name == 'DRouter'):
        if WorkingProject.objects.all().count() > 0:
            projectInformation = ProjectInformation.objects.all().filter(
                project=WorkingProject.objects.all()[0].project,
            )
            if projectInformation.count() > 0:
                activeSubscriber = projectInformation[0].activeSubscriber
                inactiveSubscriber = projectInformation[0].inactiveSubscriber

            trafficInformationList = TrafficInformation.objects.all().filter(
                project=WorkingProject.objects.all()[0].project,
            )
            for trafficInformation in trafficInformationList:
                if 'Diameter' in trafficInformation.callType.name:
                    trafficTPS += trafficInformation.trafficTPS

    data = {'ActiveSubscriber': activeSubscriber,
            'InactiveSubscriber': inactiveSubscriber,
            'TrafficTPS': trafficTPS}
    return HttpResponse(json.dumps(data), content_type='application/json')






# class SetWorkingProjectAction(BaseActionView):
#     action_name = "set_working_Project_action"
#     description = 'Set working project'
#     model_perm = 'change'
#
#     @filter_hook
#     def do_action(self, queryset):
#
#         n = queryset.count()
#
#         if n == 1:
#             setWorkingProjectMessage = "Project %s has been set as working project!" % queryset[0].name
#             setWorkingProjectSuccess = True
#
#         else:
#             setWorkingProjectMessage = "Please select only one project!"
#             setWorkingProjectSuccess = False
#
#         context = self.get_context()
#         context['setWorkingProjectMessage'] = setWorkingProjectMessage
#         context['setWorkingProjectSuccess'] = setWorkingProjectSuccess
#
#         return TemplateResponse(self.request, self.get_template_list('views/set_working_project_information.html'),
#                                 context)

# def addProject(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             send_mail(
#                 cd['subject'],
#                 cd['message'],
#                 cd.get('email', 'noreply@example.com'),
#                 ['siteowner@example.com'],
#             )
#             return Redirect('/contact/thanks/')
#         else:
#             form = ProjectForm()
#     return render('contact_form.html', {'form': form})

class ProjectList(ListView):
    template_name = 'Project/templates/project_list.html'
    #c:\Django\SurepayPET\Project\templates\project_list.html
    model = Project

class AjaxHardwareModels(ChainedSelectChoicesView):
    def get_child_set(self):
        return HardwareModel.objects.filter(hardwareType__pk=self.parent_value)
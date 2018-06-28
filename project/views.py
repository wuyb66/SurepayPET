
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Project, TrafficInformation, WorkingProject, FeatureConfiguration, \
    ProjectInformation, ApplicationConfiguration
from hardware.models import HardwareModel, HardwareType
from service.models import DBInformation, FeatureDBImpact, FeatureName, ApplicationName

import json
import math

from clever_selects.views import ChainedSelectChoicesView

from common import logger
from common.logger import logged
import sys
import os.path


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

@logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
def get_record_size(request):
    pk = request.GET['pk']
    member_group_option = request.GET['memberGroupOption']
    application = request.GET['application']
    try:
        application_id = int(application)
    except:
        application_id = 1

    db_information = get_object_or_404(DBInformation, pk=pk)
    record_size = db_information.recordSize
    ref_db_factor = get_ref_db_factor(db_information.db, member_group_option)
    subscriber_number = get_subscriber_number(member_group_option, application_id, db_information.db)
    data = {'RecordSize': record_size, 'RefDBFactor': ref_db_factor, 'SubscriberNumber': subscriber_number}
    return HttpResponse(json.dumps(data), content_type='application/json')

@logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
def get_ref_db_factor(db, member_group_option):
    feature_db_impact_list = FeatureDBImpact.objects.all().filter(
        dbName=db,
    )
    ref_db_factor = 0
    if member_group_option == 'Member':
        if db.name == 'SIM':
            ref_db_factor = 1
        for feature_db_impact in feature_db_impact_list:
            ref_db_factor += feature_db_impact.memberImpactFactor
    else:
        if db.name == 'AI':
            ref_db_factor = 1
        for feature_db_impact in feature_db_impact_list:
            ref_db_factor += feature_db_impact.groupImpactFactor
    return ref_db_factor

@logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
def get_subscriber_number(member_group_option, application_id, db):
    if WorkingProject.objects.all().count() > 0:
        traffic_information_list = TrafficInformation.objects.all().filter(
            project=WorkingProject.objects.all()[0].project
        )
        feature_db_impact_list = FeatureDBImpact.objects.all().filter(
            dbName=db,
        )
        inactive_subscriber = 0

        application = ApplicationName.objects.get(id=application_id)
        if traffic_information_list.count() > 0:
            if db.isIncludeInactiveSubscriber:
                active_subscriber = traffic_information_list[0].activeSubscriber + \
                                    traffic_information_list[0].inactiveSubscriber
            else:
                active_subscriber = traffic_information_list[0].activeSubscriber
        else:
            active_subscriber = 0
        if member_group_option == 'Member' and application.name == 'EPAY':
                return active_subscriber
        else:
            feature_name_list = FeatureName.objects.all().filter(
                name='Online Hierarchy',
            )
            if feature_name_list.count() > 0:
                penetration_olh_list = FeatureConfiguration.objects.all().filter(
                    project=WorkingProject.objects.all()[0].project,
                    feature=feature_name_list[0],
                )
                if penetration_olh_list.count() > 0:
                    penetration_olh = penetration_olh_list[0].featurePenetration / 100
                else:
                    penetration_olh = 0
            else:
                penetration_olh = 0

            group_subscriber = math.ceil(active_subscriber * penetration_olh)

            if application.name == 'DRouter': #'DROUTER'
                return group_subscriber + active_subscriber

            if member_group_option == 'Member':
                return active_subscriber
            else:
                return group_subscriber

    else:
        return 0

@logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
def get_other_application_information(request):
    active_subscriber = 0
    inactive_subscriber = 0
    traffic_tps = 0
    application_id = request.GET['pk']
    application_name = get_object_or_404(ApplicationName, pk=application_id)

    app_config = ApplicationConfiguration.current_objects.create_application_config(
        project=WorkingProject.objects.all()[0].project,
        application_name=application_name,
        deployOption=application_name.name + ' Node',
    )
    if ProjectInformation.current_objects.count() > 0:
        project_information = ProjectInformation.current_objects.all()[0]
        if application_name.name == 'Group':
            active_subscriber = project_information.groupAccountNumber
            inactive_subscriber = 0
        else:
            active_subscriber = project_information.activeSubscriber
            inactive_subscriber = project_information.inactiveSubscriber

    # if application_name.name == 'DRouter':
    #     if WorkingProject.objects.all().count() > 0:
    #         project_information = ProjectInformation.objects.all().filter(
    #             project=WorkingProject.objects.all()[0].project,
    #         )
    #         if project_information.count() > 0:
    #             active_subscriber = project_information[0].activeSubscriber
    #             inactive_subscriber = project_information[0].inactiveSubscriber
    #
    #         traffic_information_list = TrafficInformation.objects.all().filter(
    #             project=WorkingProject.objects.all()[0].project,
    #         )
    #         for traffic_information in traffic_information_list:
    #             if 'Diameter' in traffic_information.callType.name:
    #                 traffic_tps += traffic_information.trafficTPS
    if app_config.applicationName.name == 'EPAY':
        traffic_tps = app_config.get_tps_for_epay()
    elif app_config.applicationName.name == 'DRouter':
        traffic_tps = app_config.get_tps_for_drouter()
    elif app_config.applicationName.name == 'EPPSM':
        traffic_tps = app_config.get_tps_for_eppsm()
    elif app_config.applicationName.name == 'Group':
        traffic_tps = app_config.get_tps_for_group()
    elif app_config.applicationName.name == 'eCTRL':
        traffic_tps = app_config.get_tps_for_ectrl()

    app_config.delete()

    data = {'ActiveSubscriber': active_subscriber,
            'InactiveSubscriber': inactive_subscriber,
            'TrafficTPS': traffic_tps}
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
    # c:\Django\SurepayPET\Project\templates\project_list.html
    model = Project


class AjaxHardwareModels(ChainedSelectChoicesView):
    def get_child_set(self):
        return HardwareModel.objects.filter(hardwareType__pk=self.parent_value)
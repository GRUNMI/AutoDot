# Create your views here.

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from common.DataEncode import data_encode
from common.DataReplace import data_replace
from common.SaveDynamicData import save_dynamic_data
from common.ConfigFile import Config
from common.HttpRequest import HttpRequest
from common.CaseData import case_data
from django.http import JsonResponse
from common.CreateProject import create_project
from common.GetProjectName import get_project_name
from common.GetProjectCase import GetCase
from common.RunCase import run_case
from common.ProjectReport import get_html_project_report
from django.template import Template, Context
import os

# AutoDot项目

PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))


# 导航栏
def navigation(request):
    projectName = get_project_name()
    return render(request, "navigation.html", {"projectName": projectName})


# 首页
def index(request):
    projectName = get_project_name()
    return render(request, template_name="index.html", context={'projectName': projectName})


# 单接口测试页面
def single_api_test_page(request):
    return render(request, template_name="singleapitest.html")


# 单接口测试
def api_test(request):
    if request.is_ajax():
        try:
            protocol = request.GET['protocol']
            host = request.GET['host'].strip()
            method = request.GET['method'].strip()
            headers = {
                "Content-Type": request.GET['headers']
            }
            path = request.GET['path'].strip()
            data = data_encode(request.GET['data']).strip()
            url = protocol+host+path
            response = HttpRequest().send_request(url, method, headers, data)
            return HttpResponse(response.text)
        except Exception as e:
            return HttpResponse(e)


# 项目列表
def project_list_page(request):
    projectName = get_project_name()
    return render(request, template_name="projectlist.html", context={'projectName': projectName})


# 新增项目
def new_add_project(request):
    if request.is_ajax():
        project = request.GET["projectName"]
        if len(project) <= 0:
            return HttpResponse("empty")
        else:
            # 返回创建的状态
            result = create_project(project)[0]
            return HttpResponse(result)


# 运行项目用例
def run_project_case(request):
    if request.is_ajax():
        project = request.GET["projectname"]
        result = run_case(project)
        return HttpResponse(result)


# 获取项目运行结果
def get_project_result(request):
    if request.is_ajax():
        projectName = request.GET["projectname"]
        reportFolder = PATH("../report") + "\\" + projectName + "\\" + "htmlReport\\"
        for root, dirs, files in os.walk(reportFolder):
            if files:
                # 倒序查找
                for name in files[::-1]:
                    # 项目报告
                    if name.find("settingReport") < 0:
                        Config('ReportName').add_option_value('reportName', 'name', name)
                        return HttpResponse('success')
            else:
                return HttpResponse('caseEmpty')
    return render(request, Config('ReportName').get_option_value('reportName', 'name'))

    # 使用session保存
    # if request.is_ajax():
    #     context = {}
    #     projectName = request.GET["projectname"]
    #     PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))
    #     reportFolder = PATH("../report") + "\\" + projectName + "\\" + "htmlReport\\"
    #     for root, dirs, files in os.walk(reportFolder):
    #         if files:
    #             # 倒序查找
    #             for name in files[::-1]:
    #                 # 项目报告
    #                 if name.find("settingReport") < 0:
    #                     # reportName.append(name)
    #                     # return HttpResponse('success')
    #                     reportPath = os.path.join(reportFolder, name)
    #                     context["reportPath"] = reportPath
    #                     return HttpResponse('success')
    #         else:
    #             return HttpResponse('caseEmpty')
    #     request.session['msg'] = context
    # context = request.session.get('msg')
    # with open(context["reportPath"], encoding='utf-8') as fp:
    #     template = Template(fp.read())
    #     # Context 针对渲的染模板传值
    #     html = template.render(Context({"1": "1"}))
    #     return HttpResponse(html)
    # print(reportName[0])
    # return render(request, template_name=reportName[0])


# 用例管理页面
def case_management_page(request):
    return render(request, template_name="casemanagement.html")


# 预加载获取项目用例
def get_project_case(request):
    if request.is_ajax():
        project = request.GET["projectName"]
        projectCase = GetCase(project).get_project_case()
        data = {
            "name": project, "case": projectCase[0], "num": projectCase[1],
            "noRunNum": projectCase[4], "runNum": projectCase[5]
        }
        return JsonResponse(data)


# 新增用例页面
def add_case_page(request):
    if request.is_ajax():
        context = {}
        projectname = request.GET["projectname"]
        context["name"] = projectname
        request.session['msg'] = context
        return HttpResponse(projectname)
    context = request.session.get('msg')
    # print(context, "-------------------------------------------")

    # 获取配置文件中存储的动态数据
    changeData = Config(context['name']).get_section_all_option('changeData')
    if changeData != None:
        context.update(changeData)

    return render(request, "addCase.html", {"project": context})


# 新增用例页面接口测试
def add_page_interface_test(request):
    if request.is_ajax():
        try:
            projectName = request.GET["projectName"].strip()
            sql = request.GET["sql"].strip()
            protocol = request.GET["protocol"].strip()
            host = request.GET["host"].strip()
            method = request.GET["method"].strip()
            path = request.GET["path"].strip()
            headers = {
                "Content-Type": request.GET['headers']
            }
            data = request.GET['data'].strip()
            replaceID = request.GET["replaceID"].strip()
            if replaceID:
                changge_data = Config(projectName).get_section_all_option("changeData")["changeData"]
                data = data_replace(data, replaceID, changge_data=changge_data)
            data = data_encode(data)
            url = protocol + host + path
            response = HttpRequest().send_request(url, method, headers, data)
            return HttpResponse(response.text)
        except Exception as e:
            return HttpResponse(e)


# 保存新增的用例 action=1
def save_case(request):
    if request.is_ajax():
        projectName = request.GET["projectName"].strip()
        moduleName = request.GET["ModuleName"].strip()
        caseName = request.GET["CaseName"].strip()
        caseDescription = request.GET["CaseDescription"].strip()
        sql = request.GET["sql"].strip()
        protocol = request.GET["protocol"].strip()
        host = request.GET["host"].strip()
        method = request.GET["method"].strip()
        path = request.GET["path"].strip()
        headers = request.GET["headers"].strip()
        data = request.GET["data"].strip()
        replaceID = request.GET["replaceID"].strip()
        expect = request.GET["expect"].replace('"',"'").strip()
        transmitID = request.GET["TransmitID"].strip()
        transmitTargetID = request.GET["TransmitTargetID"].strip()
        checkPoint = request.GET["CheckPoint"].strip()
        if not (moduleName and caseName and protocol and host and method and expect):
            return HttpResponse('dataError')
        # 更新配置文件的动态数据
        if transmitID and transmitTargetID:
            current_all_data = Config(projectName).get_all()
            current_changeData = Config(projectName).get_section_all_option("changeData")
            dynamicData = save_dynamic_data(expect, transmitID, transmitTargetID)
            if dynamicData:
                change_dynmaic_data = {"changeData": dynamicData}
                current_changeData.update(change_dynmaic_data)
                current_all_data.update(current_changeData)
                Config(projectName).add_dict(current_all_data)
            else:
                return HttpResponse("保存动态参数字段数量必须一致，请检查！")

        # checkPoint = request.GET["CheckPoint"].strip()

        case_data(projectName=projectName, action=1, sql=sql, moduleName=moduleName, caseName=caseName,
                  caseDescription=caseDescription, protocol=protocol, host=host, method=method, path=path,
                  headers=headers, data=data, file=None, replaceID=replaceID, expect=expect, transmitID=transmitID,
                  transmitTargetID=transmitTargetID, checkPoint=checkPoint, author='GRUNMI', editor='GRUNMI')
        return HttpResponse('success')


# 修改是否执行用例 action=4
def editor_run(request):
    if request.is_ajax():
        projectname = request.GET["projectname"]
        id = request.GET["id"]
        # action = request.GET["action"]
        is_run = request.GET["is_run"]
        case_data(projectName=projectname, action=4, id=id, run=is_run)
        return HttpResponse("editor success")


# 跳转到修改用例页面，返回当前用例数据
def editor_case_page(request):
    if request.is_ajax():
        context = {}
        projectname = request.GET["projectname"]
        id = request.GET["id"]
        context["projectname"] = projectname
        context["id"] = id
        request.session['msg'] = context
        return HttpResponse('success')
    context = request.session.get('msg')
    # action=5 查询数据，返回到修改界面
    result = case_data(projectName=context['projectname'], action=5, id=context["id"])
    # 获取配置文件中存储的动态数据
    changeData = Config(context['projectname']).get_section_all_option('changeData')
    if changeData != None:
        result.update(changeData)
    return render(request, "editorCase.html", {"editor": result})


# 修改页面单接口测试
def editor_page_api_test(request):
    if request.is_ajax():
        try:
            projectName = request.GET["projectName"].strip()
            sql = request.GET["sql"].strip()
            protocol = request.GET["protocol"].strip()
            host = request.GET["host"].strip()
            method = request.GET["method"].strip()
            path = request.GET["path"].strip()
            headers = {
                "Content-Type": request.GET['headers']
            }
            data = request.GET['data'].strip()
            replaceID = request.GET["replaceID"].strip()
            if replaceID:
                changge_data = Config(projectName).get_section_all_option("changeData")["changeData"]
                data = data_replace(data, replaceID, changge_data=changge_data)
            data = data_encode(data)
            url = protocol + host + path
            response = HttpRequest().send_request(url, method, headers, data)
            return HttpResponse(response.text)
        except Exception as e:
            return HttpResponse(e)


# 保存修改用例 action=3
def save_editor_case(request):
    if request.is_ajax():
        projectName = request.GET["projectName"].strip()
        id = request.GET["id"]
        moduleName = request.GET["moduleName"].strip()
        caseName = request.GET["caseName"].strip()
        caseDescription = request.GET["caseDescription"].strip()
        sql = request.GET["sql"].strip()
        protocol = request.GET["protocol"].strip()
        host = request.GET["host"].strip()
        method = request.GET["method"].strip()
        path = request.GET["path"].strip()
        headers = request.GET["headers"].strip()
        data = request.GET["data"].strip()
        replaceID = request.GET["replaceID"].strip()
        expect = request.GET["expect"].strip()
        transmitID = request.GET["transmitID"].strip()
        transmitTargetID = request.GET["transmitTargetID"].strip()
        checkPoint = request.GET["checkPoint"].strip()

        if not (moduleName and caseName and protocol and host and method and expect):
            return HttpResponse('dataError')

        # 更新配置文件的动态数据
        if transmitID and transmitTargetID:
            current_all_data = Config(projectName).get_all()
            current_changeData = Config(projectName).get_section_all_option("changeData")
            dynamicData = save_dynamic_data(expect, transmitID, transmitTargetID)
            if dynamicData:
                change_dynmaic_data = {"changeData": dynamicData}
                current_changeData.update(change_dynmaic_data)
                current_all_data.update(current_changeData)
                Config(projectName).add_dict(current_all_data)
            else:
                return HttpResponse("保存动态参数字段数量一致，或响应结果不存在该参数，请检查！")
        elif transmitID and transmitTargetID == '':
            return HttpResponse("保存动态参数字段数量一致，请检查！")

        elif transmitID == '' and transmitTargetID:
            return HttpResponse("保存动态参数字段数量一致，请检查！")

        # checkPoint = request.GET["checkPoint"].strip()

        case_data(projectName=projectName, action=3,id=id,moduleName=moduleName,caseName=caseName,
                  caseDescription=caseDescription,sql=sql,protocol=protocol,host=host,method=method,path=path,headers=headers,
              data=data,file=None,replaceID=replaceID,expect=expect,transmitID=transmitID,
              transmitTargetID=transmitTargetID,checkPoint=checkPoint,author='GRUNMI',editor='GRUNMI')
        return HttpResponse('success')


# 删除用例 action=2
def del_case(request):
    if request.is_ajax():
        projectName = request.GET["projectName"]
        # action = request.GET["action"]
        id = request.GET["id"]
        case_data(projectName=projectName, action=2, id=id)
        return HttpResponse("del success")


# 场景测试页面
def setting_test_page(request):
    return render(request, template_name="settingtest.html")


# 运行场景用例
def run_setting_test_case(request):
    if request.is_ajax():
        projectName = request.GET['projectName']
        id = request.GET['id']
        if id:
            result = run_case(projectname=projectName, type=1, id=id)
            return HttpResponse(result)
        else:
            return HttpResponse('empty')


# 查看场景用例报告
def check_setting_run_result(request):
    if request.is_ajax():
        context = {}
        projectName = request.GET["projectName"]
        # type=1 标识场景用例
        # report = get_html_project_report(projectName, type=1)
        # PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))
        reportFolder = PATH("../report") + "\\" + projectName + "\\" + "htmlReport\\"
        for root, dirs, files in os.walk(reportFolder):
            if files:
                # 倒序查找
                for name in files[::-1]:
                    # 场景用例报告
                    if name.find("settingReport") == 0:
                        Config('ReportName').add_option_value('reportName', 'name', name)
                        return HttpResponse('success')
                        # reportPath = os.path.join(reportFolder, name)
                        # context["reportPath"] = reportPath
                        # return HttpResponse('success')
            else:
                return HttpResponse('reportEmpty')
    return render(request, Config('ReportName').get_option_value('reportName', 'name'))
    #     request.session['msg'] = context
    # context = request.session.get('msg')
    # with open(context["reportPath"], encoding='utf-8') as fp:
    #     template = Template(fp.read())
    #     # Context 针对渲的染模板传值
    #     html = template.render(Context({"1": "1"}))
    #     return HttpResponse(html)


# 测试报告页面
def test_report(request):
    return render(request, template_name="testreport.html")

# 获取项目所有报告
def get_project_all_report(request):
    if request.is_ajax():
        projectName = request.GET["projectName"]
        result = {"projectname": projectName}
        report = []
        projectReportFolder = PATH("../report/{}".format(projectName))
        if os.path.exists(projectReportFolder):
            htmlReportFolder = PATH("../report/{}/htmlReport".format(projectName))
            for root, dirs, files in os.walk(htmlReportFolder):
                # print(files)
                if files:
                    for i in files[::-1]:
                        report.append({"name": i.rstrip('.html')})
                    result.update({"report": report})
                    return JsonResponse(result)
                else:
                    result.update({"report": report})
                    return JsonResponse(result)
        else:
            result.update({"report": report})
            return JsonResponse(result)


# 查看报告
def check_report(request):
    report = []
    # report = ['2018-11-02 13-49-46.html']
    if request.is_ajax():
        context = {}
        projectName = request.GET["projectName"]
        reportName = request.GET["reportName"].rstrip("查看报告")+'.html'
        Config('ReportName').add_option_value('reportName', 'name', reportName)
    return render(request, Config('ReportName').get_option_value('reportName', 'name'))
    #     reportPath = PATH("../report/{}/htmlReport/{}".format(projectName, reportName))
    #     context["reportPath"] = reportPath
    #     request.session['msg'] = context
    # context = request.session.get('msg')
    # with open(context["reportPath"], encoding='utf-8') as fp:
    #     template = Template(fp.read())
    #     # Context 针对渲的染模板传值
    #     html = template.render(Context({"1": "1"}))
    #     return HttpResponse(html)



# 环境配置
def environment_config(request):
    projectName = get_project_name()
    return render(request, template_name="environmentconfig.html", context={'projectName': projectName})


"""AutoDot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from DotDotDot import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', views.navigation, name="菜单栏"),
    url(r'^index', views.index, name="项目首页"),
    url(r'^single/api/test', views.single_api_test_page, name="单接口测试页面"),
    url(r'^api/test', views.api_test, name="单接口测试"),
    url(r'^project/list', views.project_list_page, name="项目列表"),
    url(r'^new/add/project', views.new_add_project, name="新增项目"),
    url(r'^check/project/all/case', views.get_project_case, name="查看项目用例"),
    url(r'^run/current/project/all/case', views.run_project_case, name="运行项目用例"),
    url(r'^check/current/run/result', views.get_project_result, name="查看项目结果"),
    url(r'^case/management', views.case_management_page, name="用例管理"),
    url(r'^case/list', views.get_project_case, name="加载项目所有用例"),
    url(r'^add/case', views.add_case_page, name="新增用例页面"),
    url(r'^add/page/interface/test', views.add_page_interface_test, name="新增用例页面接口测试"),
    url(r'^save/case', views.save_case, name="保存新增的用例"),
    url(r'^editor/run', views.editor_run, name="修改是否执行用例"),
    url(r'^editor/case', views.editor_case_page, name="修改用例页面"),
    url(r'^editor/page/api/test', views.editor_page_api_test, name="修改页面接口测试"),
    url(r'^save/editor/case', views.save_editor_case, name="保存修改的用例"),
    url(r'^del/case', views.del_case, name="删除用例"),
    url(r'^setting/test', views.setting_test_page, name="场景用例页面"),
    url(r'^setting/project/case', views.get_project_case, name="场景项目的用例"),
    url(r'run/setting/test/case', views.run_setting_test_case, name="执行场景用例"),
    url(r'check/setting/run/result', views.check_setting_run_result, name="查看场景运行结果"),
    url(r'^test/report', views.test_report, name="测试报告"),
    url(r'get/project/all/report', views.get_project_all_report, name="获取项目所有报告"),
    url(r'check/report', views.check_report, name="查看报告"),
    url(r'environment/config', views.environment_config, name="环境配置"),

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

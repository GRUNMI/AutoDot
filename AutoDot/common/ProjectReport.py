# coding:utf-8
__author__ = 'GRUNMI'


from pyecharts import Bar, Pie, Timeline
import common.LogOutput
import os
from common.GetRunProjectCaseNumResult import get_project_run_num
import time


def get_html_project_report(project_name, type=0):
    mylogger = common.LogOutput.Log().get_logger()
    mylogger.info("------------------------------------------------------------------")
    mylogger.info("当前运行文件：{}".format(__file__))
    try:
        project_run_num = get_project_run_num(project_name, type)
        # num = [successNum, failedNum, noRunNum]
        num = [project_run_num[0], project_run_num[1], project_run_num[2]]
        attr = ["成功用例", "失败用例", "不执行用例"]
        bar = Bar(project_name, "用例执行结果")
        bar.add("", attr, num, is_more_utils=True)
        bar.show_config()

        pie_1 = Pie(project_name, "用例执行结果")
        pie_1.add(project_name, attr, num,
                  is_label_show=True, radius=[30, 55], rosetype='radius')

        timeline = Timeline(is_auto_play=True, timeline_bottom=0)
        timeline.add(bar, '树形图')
        timeline.add(pie_1, '饼形图')

        PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))
        html_dirname = PATH("../report") + "\\" + project_name + "\\" + "htmlReport\\"

        # 判断是否存在case目录，没有，则创建
        if not os.path.exists(html_dirname):
            os.mkdir(html_dirname)
            mylogger.info("生成用例目录路径：{}".format(html_dirname))
        if type == 0:
            html_report_name = time.strftime('%Y-%m-%d %H-%M-%S') + '.html'
        elif type == 1:
            html_report_name = 'settingReport' + time.strftime('%Y-%m-%d %H-%M-%S') + '.html'
        htmlReportPath = html_dirname + html_report_name
        timeline.render(htmlReportPath)
        return 'success'
    except TypeError as e:
        return 'caseEmpty', e


if __name__ == '__main__':
    get_html_project_report('test', type=1)

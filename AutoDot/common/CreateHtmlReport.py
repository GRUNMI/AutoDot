# coding:utf-8
__author__ = 'GRUNMI'

from bottle import template
import os
import time
from common.LogOutput import Log
mylogger = Log().get_logger()


def create_html_report(data, type=0):

    reportTemplate = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>报告模板</title>
        <script src="http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
        <style>
            input{
                color: #fff;
                width: 90px;
                height: 30px;
                border: none;
                outline:none;
                border-radius: 5px;
            }
            button{
                background-color: #5bc0de;
                border: none;
                outline:none;
                color: white;
                border-radius: 5px;
            }
            .detail:hover{
                text-decoration: underline;
                background-color: #98ff94;
            }
        </style>
    </head>
    <body>
    <div style="width: 1000px;">
        <div style="float: left">
            <h2>{{data["projectName"]}}</h2>
            <p><strong>测试人员：</strong>{{data["testPersonName"]}}</p>
            <p><strong>开始时间：</strong>{{data["startTime"]}}</p>
            <p><strong>合计耗时：</strong>{{data["runTime"]}}</p>
            <p><strong>测试结果：</strong>共 {{data["sum"]}}，通过 {{data["pass"]}}，失败 {{data["failed"]}}，通过率 {{data["passRate"]}}</p>
            <p><strong>运行环境：</strong>{{data["runEnvironment"]}}</p>
            <p>测试用例结果</p>
            <p>
                <input type="button" style="background-color: #428bca;" value="概要{ {{data["passRate"]}} }">
                <input type="button" style="background-color: #5cb85c;" value="成功{ {{data["pass"]}} }">
                <input type="button" style="background-color: #FF0000;" value="失败{ {{data["failed"]}} }">
                <input type="button" style="background-color: #5bc0de;" value="所有{ {{data["sum"]}} }">
            </p>
        </div>
        <div style="float: right;margin-top: 60px">
            <canvas id="circle" width="300" height="200">您的浏览器暂不支持Canvas</canvas>
            <input type="button" style="background-color: #5cb85c;" value="通过{ {{data["passRate"]}} }">
            <input type="button" style="background-color: #FF0000;" value="失败{ {{data["failedRate"]}} }">
        </div>
    </div>
    <div>
    <table style="width: 100%;">
        <caption id="cap">
            <p id="title"></p>

        </caption>
        <thead id="th">
        <tr style="background-color: #d7dbdb">
            <th style="width: 15%">用例名称</th>
            <th style="width: 15%">用例路径</th>
            <th style="width: 55%">测试结果</th>
            <th style="width: 15%">校验详细</th>
        </tr>
        </thead>
        <tbody id="tb" align="center">
            % for value in data["runResult"]:
                <tr style="background-color: #d0e9c6">
                    <td>{{value["moduleName"]}}</td>
                    <td>{{value["path"]}}</td>
                    <td><button>{{value["result"]}}</button></td>
                    <td class="detail" style="color: #00AAFF; cursor: pointer">详细</td>
                </tr>
                <tr class="content" style="display: none">
                    <td></td>
                    <td></td>
                    <td>
                        {{value["checkDetail"]}}
                    </td>
                </tr>
            %end

        </tbody>

        <tfoot id="tf" align="center" style="background-color: #d3d3d3">
        <tr style="font-weight: bold;font-size: small">
            <td>统计</td>
            <td>总计{ {{data["sum"]}} }</td>
            <td>通过{ {{data["pass"]}} }&emsp;&emsp;失败{ {{data["failed"]}} }</td>
            <td>通过率{ {{data["passRate"]}} }</td>
        </tr>
        </tfoot>
    </table>
    </div>
    </body>

    <script type="text/javascript">

        var color = ["#5cb85c","#FF0000"];
        var data = [{{data["pass"]}},{{data["failed"]}}];
        //var text = ["成功","失败"];
        var sumData = {{data["sum"]}};
        var beginAngle = 0;
        var endAngle = 0;
        function drawCircle(){
            var canvas = document.getElementById("circle");
            var ctx = canvas.getContext("2d");
            for(var i=0;i<data.length;i++){
                //绘制饼形图
                ctx.fillStyle = color[i];
                ctx.strokeStyle = color[i];
                beginAngle = endAngle;
                endAngle = beginAngle + Math.PI*2*(data[i]/sumData);
                ctx.beginPath();
                ctx.moveTo(100,100);
                ctx.arc(100,100,100,beginAngle,endAngle);
                ctx.fill();
                ctx.stroke();
                }
        }
        drawCircle();

        $("#tb").on("click",".detail",function () {
            var hideContent = $(this).parent().next();
            if (hideContent.is(':hidden')){
                hideContent.show();
            }else{
                hideContent.hide();
            }
        })
    </script>
    </html>"""
    html = template(reportTemplate, data=data)

    PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))
    html_dirname = PATH("../report") + "\\" + data["projectName"] + "\\" + "htmlReport\\"

    # 判断是否存在case目录，没有，则创建
    if not os.path.exists(html_dirname):
        os.makedirs(html_dirname)
        mylogger.info("生成报告目录路径：{}".format(html_dirname))

    if type == 0:
        html_report_name = time.strftime('%Y-%m-%d %H-%M-%S') + '.html'
    elif type == 1:
        html_report_name = 'settingReport' + time.strftime('%Y-%m-%d %H-%M-%S') + '.html'
    htmlReportPath = html_dirname + html_report_name

    with open(htmlReportPath, 'wb') as f:
        f.write(html.encode('utf-8'))
        mylogger.info("生成报告成功：{}".format(htmlReportPath))


def main():
    text = {
        "projectName": "自动干线",
        "testPersonName": "GRUNMI",
        "startTime": "2018-10-18 16:03:05",
        "runTime": "0:03:08.785000",
        "pass": "2",
        "failed": "1",
        "sum": 3,
        "passRate": "64.3%",
        "failedRate": "33%",
        "runEnvironment": "python3.6+django1.2",
        "runResult": [
            {
                "moduleName": "CaseName",
                "path": "/login/",
                "result": "true",
                "checkDetail": [
                    {
                        "预期结果": {
                            "name": ['1']
                        }
                    },
                    {
                        "运行结果": {
                            "name": ['1']
                        }
                    }
                ]
            },
            {
                "moduleName": "CaseName2",
                "path": "/login2/",
                "result": "false",
                "checkDetail": [
                    {
                        "预期结果": {
                            "name": ['2']
                        }
                    },
                    {
                        "运行结果": {
                            "name": ['3']
                        }
                    }
                ]
            }
        ]
    }
    create_html_report(text, type=1)


if __name__ == '__main__':
    main()

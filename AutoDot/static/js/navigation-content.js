/**
 * Created by GRUNMI.
 */


$("#parm").val("");
    function index(){
        $("#myiframe").attr("src","/index/");
    }

    function singleInterface(){
        $("#myiframe").attr("src","/single/api/test/");


    }
    function projectList(){
        $("#myiframe").attr("src","/project/list/");

    }
    function caseManagement(name){
        //传值给父页面 #parm
        $("#parm").val(name);
        $("#myiframe").attr("src","/case/management/");


    }
    function settingTest(name){
        $("#parm").val(name);
        $("#myiframe").attr("src","/setting/test/");

    }function testReport(name){
        $("#parm").val(name);
        $("#myiframe").attr ("src","/test/report/");

    }function environmentConfig(name) {
        $("#parm").val(name);
        $("#myiframe").attr ("src","/environment/config/");
    }



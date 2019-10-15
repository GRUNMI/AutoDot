/**
 * Created by GRUNMI.
 */
 
 

// 获取父元素的值
var ht = $('#parm', window.parent.document).val();
// 默认加载
window.onload=getCaseList();
function getCaseList(){
    $.ajax({
        type:"get",
        url:"/case/list/",
        data:{'projectName':ht},
        dataType:"json",
        success: function (data) {
            // 获取项目的用例
            console.log(data);

            var title = "";
            title += '<h2>'+data.name+'</h2>';
            //title += '<a href="/add/case/" id="addcase" projectname="'+data.name+'" style="text-decoration:none">新增用例</a>';
            title += '<span id="addcase" projectname="'+data.name+'" style="cursor: pointer;background-color: red;">新增用例</span>';
            $("#cap").html(title);

            var th ="";
            th += '<tr><th>用例编号</th>';
            th += '<th>是否执行</th>';
            th += '<th>模块名称</th>';
            th += '<th>用例名称</th>';
            th += '<th>请求方法</th>';
            th += '<th>协议</th>';
            th += '<th>Host</th>';
            th += '<th>路径</th>';
            th += '<th>参数</th>';
            th += '<th>编辑人</th>';
            th += '<th>操作</th></tr>';
            $("#th").html(th);

            var caseAarry = data.case;
            if(caseAarry.length>0){
                var tb = "";
                $.each(caseAarry,function(index,val){
                    tb +='<tr align="center">';
                    tb +='<td>'+val.ID+'</td>';
                    tb +='<td><select id="runSelect"  projectname="'+data.name+'" rowid="'+val.RowID+'">';
                    if(val.Run == 'YES'){
                        tb +='<option selected value="YES">YES</option>';
                    }else{
                        tb +='<option value="YES">YES</option>';
                    }
                    if(val.Run == 'NO'){
                        tb +='<option selected value="NO">NO</option>';
                    }else{
                        tb +='<option value="NO">NO</option>';
                    }
                    tb +='</select></td>';
                    tb +='<td title="'+val.ModuleName+'">'+val.ModuleName+'</td>';
                    tb +='<td title="'+val.CaseName+'：'+val.CaseDescription+'">'+val.CaseName+'</td>';
                    tb +='<td>'+val.Method+'</td>';
                    tb +='<td>'+val.Protocol+'</td>';
                    tb +='<td>'+val.Host+'</td>';
                    tb +='<td title="'+val.Path+'">'+val.Path+'</td>';
                    tb +='<td title="'+val.Data+'">'+val.Data+'</td>';

                    tb +='<td>'+val.Editor+'</td>';
                    //tb +='<td><a href="/editor/case/'+val.ID+'" id="editor" rowid="'+val.RowID+'" projectname="'+data.name+'" style="text-decoration:none">修改</a><a id="delBtn" rowId="'+val.RowID+'" projectname="'+data.name+'" href="#" style="text-decoration:none">删除</a></td>';
                    tb +='<td><span id="editor" rowid="'+val.RowID+'" projectname="'+data.name+'" style="cursor: pointer;background-color: red;">修改</span><span id="delBtn" rowId="'+val.RowID+'" projectname="'+data.name+'" style="cursor: pointer;">删除</span></td>';
                });
                $("#tb").html(tb);
            }


            var tf = "";
            <!--水平合并单元格-->
            tf +='<tr><td colspan="10">总数</td>';
            tf +='<td id="tf-sum">'+data.num+'</td></tr>';
            tf +='';
            $("#tf").html(tf);
        }
    })
}


// 新增用例
$("#cap").on("click","#addcase",function () {
    var projectname = $(this).attr("projectname");
    //alert("新增用例数据");
    $.ajax({
        type:"get",
        url:"/add/case/",
        data:{"projectname":projectname},
        dataType:"text",
        success:function (data) {
            //alert(data);
            console.log(data);
            //alert("跳转iframe子界面");
            window.location.href="/add/case/";
            //alert("准备跳转整个界面");
            //window.parent.location.href="/add/case/";
        }
    })

});

// 修改选择是否执行用例
 $("#project-case").on("change","#runSelect",function(){
    //alert($(this).val());
     var projectname = $(this).attr("projectname");
     var rowid = $(this).attr("rowid");
     $.ajax({
         type:"get",
         url:"/editor/run/",
         // 修改是否执行用例 "action":4
         data:{"is_run":$(this).val(), "project":projectname, "rowid":rowid},
         //daatType:"json",
         success: function (data) {
             alert("修改成功")

         }

     })
 });


// 修改用例
$("#tb").on("click","#editor",function () {

    var projectname = $(this).attr("projectname");
    //alert(projectname);
    var rowid = $(this).attr("rowid");
    $.ajax({
        type:"get",
        url:"/editor/case/",
        data:{"projectname":projectname,"rowid":rowid},

        success: function (result) {
            //alert("跳转到修改用例页面");
            console.log(result);
            window.location.href="/editor/case/";

        }

    })

});



//删除用例
$("#tb").on("click","#delBtn",function(){
    var rowId = $(this).attr("rowId");
    var projectname = $(this).attr("projectname");
    //alert(projectname);
    var isSuccess = delCase(rowId, projectname);
    if(isSuccess){
        $(this).parent().parent().remove();
        var caseSize = $("#tf-sum").text();
        if(caseSize <= 0){
            caseSize = 0;
        }else{
            caseSize = caseSize -1;
        }
        $("#tf-sum").html(caseSize);
    }

 });

function delCase(rowId, projectname){
    $.ajax({
            type:"get",
            url:"/del/case/",
            // 删除 "action":2
            data:{"projectName":projectname,"rowid":rowId},
            success:function (data) {
                alert("删除成功,rowId="+rowId + projectname);
                console.log(data);
                //回调初始方法，刷新界面
                getCaseList();

                //window.location.href="/case/list/"+projectname;
            }
        });

    return true;
}

 
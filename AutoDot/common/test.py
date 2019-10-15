from pyecharts import Bar,Pie,Timeline
import random


num = [1, 120, 1]
title = "项目名称"
templates_name = "render.html"
attr = ["成功", "失败", "不执行"]
bar = Bar(title, "用例执行结果")
bar.add("", attr, num, is_more_utils=True)
bar.show_config()


pie_1 = Pie(title, "用例执行结果")
pie_1.add(title, attr, num,
          is_label_show=True, radius=[30, 55], rosetype='radius')

timeline = Timeline(is_auto_play=True, timeline_bottom=0)
timeline.add(bar, '树形图')
timeline.add(pie_1, '饼形图')

timeline.render(templates_name)



# from pyecharts import Pie, Timeline
#
#
# bar = Bar("第一个图表")
# bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90], is_more_utils=True)
# # bar.show_config()
#
#
# attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
# pie_1 = Pie("2012 年销量比例", "数据纯属虚构")
# pie_1.add("秋季", attr, [random.randint(10, 100) for _ in range(6)],
#           is_label_show=True, radius=[30, 55], rosetype='radius')
#
#
# pie_2 = Pie("2013 年销量比例", "数据纯属虚构")
# pie_2.add("秋季", attr, [random.randint(10, 100) for _ in range(6)],
#           is_label_show=True, radius=[30, 55], rosetype='radius')
#
# pie_3 = Pie("2014 年销量比例", "数据纯属虚构")
# pie_3.add("秋季", attr, [random.randint(10, 100) for _ in range(6)],
#           is_label_show=True, radius=[30, 55], rosetype='radius')
#
# pie_4 = Pie("2015 年销量比例", "数据纯属虚构")
# pie_4.add("秋季", attr, [random.randint(10, 100) for _ in range(6)],
#           is_label_show=True, radius=[30, 55], rosetype='radius')
#
# pie_5 = Pie("2016 年销量比例", "数据纯属虚构")
# pie_5.add("秋季", attr, [random.randint(10, 100) for _ in range(6)],
#           is_label_show=True, radius=[30, 55], rosetype='radius')
#
# timeline = Timeline(is_auto_play=True, timeline_bottom=0)
# timeline.add(bar, '2011 年')
# timeline.add(pie_1, '2012 年')
# timeline.add(pie_2, '2013 年')
# timeline.add(pie_3, '2014 年')
# timeline.add(pie_4, '2015 年')
# timeline.add(pie_5, '2016 年')
# timeline.render()
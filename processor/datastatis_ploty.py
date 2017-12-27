#!-*-coding:utf-8-*-

from __future__ import division
import plotly.plotly as py
import time
from weixin_processor import get_stats_data
import datetime

def line_plot(target_num):
    py.sign_in('datongxueba', '6OrBp3oNDFEbL2W4lV1Q')
    first_day = datetime.date.today().replace(day=1)
    x1 = 1
    x2 = 30
    y1 = get_stats_data(str(first_day), str(first_day))
    y2 = target_num
    A = (y2 - y1) / (x2 - x1)
    B = y1 - A * x1
    now = time.time()
    dx = []
    dy1 = []
    dy2 = []
    for i in range(30):
        thisday = time.strftime('%Y-%m-%d',
                                time.localtime(time.mktime(time.strptime(str(first_day),
                                                                         '%Y-%m-%d')) + i * 24 * 3600))
        print thisday
        if time.strftime('%Y-%m-%d',time.localtime(time.time())) == thisday:
            break
        stat_data = get_stats_data(thisday, thisday)
        if stat_data == -1:
            break
        #print thisday
        dx.append(thisday)
        dy1.append(int(A * (i + 1) + B))
        dy2.append(stat_data)
    trace1 = {'x': dx, 'y': dy1, 'mode': 'lines','name':'预期增粉'}
    trace2 = {'x': dx, 'y': dy2, 'mode': 'lines','name':'实际增粉'}
    annotations = []
    annotations.append(get_annotation(dy1,'rgba(67,67,67,1)'))
    annotations.append(get_annotation(dy2, 'rgba(115,115,115,1)'))
    layout = dict(title='本月截至%s预期与实际增粉对比'% dx[-1],
        legend=dict(
            y=1,
            x=0.05,
            font=dict(
                size=16
            )
        )
    )
    layout['annotations'] = annotations
    # layout['legend'] = get_legend()

    # trace2 = {'x': dx[0], 'y': dy2, 'mode': 'lines'}
    data = []
    data.append(trace1)
    data.append(trace2)
    fig = {'data': data,'layout':layout}
    py.image.save_as(fig, '/home/myWxbot/data_statis.png', scale=3)

def get_annotation(y,color):
    return dict(xref='paper', x=1, y=y[-1],
                                  xanchor='left', yanchor='middle',
                                  text='{}'.format(y[-1]),
                                  font=dict(family='Arial',
                                            size=16,
                                            color=color,),
                                  showarrow=False)

def get_legend():
    dict(
        y=0.95,
        x = 0.05,
        font=dict(
            size=16
        )
    )

if __name__ == '__main__':
    line_plot(30000)

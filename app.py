import datetime
import time
from collections import deque

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
import requests
from dash.dependencies import Output, Input
from dateutil.relativedelta import relativedelta
from plotly.graph_objs import Layout

url = "https://covid-193.p.rapidapi.com/history"
# tydzien = 5
# miesiac = 0
data_miesiace = []
for i in range(0, 13):
    data_miesiace.append(str(datetime.date.today() - relativedelta(months=i)))
# print(data_miesiace)
# data = str(datetime.date.today() - relativedelta(months=miesiac))
# data1 = str(datetime.date.today() - relativedelta(months=miesiac + 1))
# data2 = str(datetime.date.today() - relativedelta(months=miesiac + 2))
# data3 = str(datetime.date.today() - relativedelta(months=miesiac + 3))
# data4 = str(datetime.date.today() - relativedelta(months=miesiac + 4))
# data5 = str(datetime.date.today() - relativedelta(months=miesiac + 5))
# data6 = str(datetime.date.today() - relativedelta(months=miesiac + 6))
# data7 = str(datetime.date.today() - relativedelta(months=miesiac + 7))
# data8 = str(datetime.date.today() - relativedelta(months=miesiac + 8))
# data9 = str(datetime.date.today() - relativedelta(months=miesiac + 9))
# data10 = str(datetime.date.today() - relativedelta(months=miesiac + 10))
# data11 = str(datetime.date.today() - relativedelta(months=miesiac + 11))
# data12 = str(datetime.date.today() - relativedelta(months=miesiac + 12))
# monthdata = []
# monthdata.append(data6)
# monthdata.append(data5)
# monthdata.append(data4)
# monthdata.append(data3)
# monthdata.append(data2)
# monthdata.append(data1)
# monthdata.append(data)
# print(monthdata)
year2 = []
for i in data_miesiace:
    year2.append({"country": "poland", "day": i})
print(year2)
# year = []
# day0 = {"country": "poland", "day": data}
# day1 = {"country": "poland", "day": data1}
# day2 = {"country": "poland", "day": data2}
# day3 = {"country": "poland", "day": data3}
# day4 = {"country": "poland", "day": data4}
# day5 = {"country": "poland", "day": data5}
# day6 = {"country": "poland", "day": data6}
# day7 = {"country": "poland", "day": data7}
# day8 = {"country": "poland", "day": data8}
# day9 = {"country": "poland", "day": data9}
# day10 = {"country": "poland", "day": data10}
# day11 = {"country": "poland", "day": data11}
# day12 = {"country": "poland", "day": data12}

# year.append(day0)
# year.append(day1)
# year.append(day2)
# year.append(day3)
# year.append(day4)
# year.append(day5)
# year.append(day6)
# year.append(day7)
# year.append(day8)
# year.append(day9)
# year.append(day10)
# year.append(day11)
# year.append(day12)
# print(year)
total = []
new_deaths = []
headers = {
    'x-rapidapi-key': "727e428476msh9d9ec2a0042a970p1e3454jsn31917a65b782",
    'x-rapidapi-host': "covid-193.p.rapidapi.com"
}
for day in year2:
    pom = 0
    pom2 = 0

    response = requests.request("GET", url, headers=headers, params=day)
    result = response.json()
    while result['response'][pom]['cases']['new'] is None:
        pom = pom + 1

    print(str(day) + " cases: " + result['response'][pom]['cases']['new'])
    total.append(result['response'][pom]['cases']['new'])
    while result['response'][pom2]['deaths']['new'] is None:
        pom2 = pom2 + 1

    print(str(day) + " deaths: " + result['response'][pom]['deaths']['new'])
    new_deaths.append(result['response'][pom2]['deaths']['new'])

X = deque(maxlen=20)
X.append(1)

Y = deque(maxlen=20)
Y.append(1)

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Covid-19 Today'"'"'s Statistics'),
            html.H2('compared to every month')
        ], className="header"),
        html.Div([
            # html.H1(children='Hello Dash'),
            dcc.Graph(id="scatter-plot"),
            html.P("New Deaths"),
        ], className="first_row"),

        html.Div([
            # html.H1(children='Hello Dash')
            dcc.Graph(id="scatter-plot2"),
            html.P("New Cases"),
        ], className='first_row'),

    ], className='row'),
    html.Div([
        html.P("Month:"), dcc.Slider(
            id='slider2',
            min=-12, max=0, step=1,
            marks={-12: '06.20', -6: '12.20', 0: '06.21'},
            value=[0]
        ), ], ),
], className='all')

time.sleep(2)
xdeaths = []
ydeaths = []
xcases = []
ycases = []


@app.callback(
    Output("scatter-plot", "figure"),
    [Input("slider2", "value")])
def update_first_chart(slider_value):
    if type(slider_value) != int:
        month = 0
    else:
        month = slider_value * -1
    # mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    n = int(new_deaths[month])
    print(n)
    global xdeaths, ydeaths
    if len(xdeaths) < n:
        for i in range(n-len(xdeaths)):
            xdeaths.append(np.random.uniform(-50, 50))
            ydeaths.append(np.random.uniform(-50, 50))


    fig = go.Figure(data=go.Scattergl(
        x=xdeaths[:n],

        y=ydeaths[:n],
        # fillcolor= 'white',
        # opacity=50,

        mode='markers',
        marker=dict(
            color=np.random.randn(n),
            colorscale='Viridis',
            size=5,
            line_width=1
        )
    ),
        layout=Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False,
            )
        )
    )
    fig2 = go.Figure(data=go.Scattergl(
        x=np.random.randn(n),
        y=np.random.randn(n),
        mode='markers',
        marker=dict(
            color=np.random.randn(n),
            colorscale='Viridis',

            line_width=1
        )
    ))
    return fig


@app.callback(
    Output("scatter-plot2", "figure"),
    [Input("slider2", "value")])
def update_left_chart(slider_value):
    month = slider_value
    print(type(month))
    if type(month) != int:
        month = 0
    else:
        month = slider_value * -1
    # mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    n = int(total[month])
    global xcases, ycases
    if len(xcases) < n:
        for i in range(n - len(xcases)):
            xcases.append(np.random.uniform(-100, 100))
            ycases.append(np.random.uniform(-100, 100))
    fig = go.Figure(data=go.Scattergl(
        x=xcases[:n],
        y=ycases[:n],
        mode='markers',
        marker=dict(
            color=np.random.randn(n),
            colorscale='Viridis',
            size=5,
            line_width=1

        )
    ), layout=Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        )))
    return fig

    # time.sleep(0.5)


if __name__ == '__main__':
    app.run_server()

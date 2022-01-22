import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from web import db

session = db.session.bind
df = pd.read_sql_table('doors', session)
df['open'].astype('datetime64')
df['close'].astype('datetime64')


def pie():
    d = df['location'].value_counts().to_dict()

    return list(d.keys()), list(d.values())


def line(freq='min'):
    d = df.groupby(pd.Grouper(key='open', freq=freq)).count()
    d = d.drop(['close', 'location'], axis=1).to_dict()['id']
    k = d.keys()
    v = d.values()

    return list(k), list(v)

def plot_pie():
    d = df['location'].value_counts().to_dict()

    return px.pie(
        names=d.keys(),
        values=d.values()
    ).to_html(full_html=False, default_height='300px')


def plot_hist(freq='min'):
    d = df.groupby(pd.Grouper(key='open', freq=freq)).count()
    d = d.drop(['close', 'location'], axis=1).to_dict()['id']
    k = d.keys()
    v = d.values()
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.3,
        specs=[[{"type": "table"}],
               [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Scatter(x=list(k), y=list(v))
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Id", "Location", "Open", "Close"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[df[k].tolist() for k in df.columns],
                align="left")
        ),
        row=1, col=1
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=5,
                         label="5 minute",
                         step="minute",
                         stepmode="todate"),
                    dict(count=1,
                         label="hour",
                         step="hour",
                         stepmode="todate"),
                    dict(count=7,
                         label="7 days",
                         step="day",
                         stepmode="todate"),
                    dict(count=6,
                         label="6 month",
                         step="month",
                         stepmode="todate"),
                    dict(count=1,
                         label="year",
                         step="year",
                         stepmode="todate"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date",
        ),
        yaxis=dict(
            tickmode='linear',
            tick0=-1,
            dtick=1
        ),
        width=1000,
        height=1000
    )

    return fig.to_html(full_html=False)


if __name__ == '__main__':
    plot_hist()

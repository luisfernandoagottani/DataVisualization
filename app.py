import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash
import plotly.express as px
from dash.dependencies import Input, Output
from PIL import Image


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv('Indicadores_base.csv')

layout_home = html.Div([
    html.Div([
        dcc.Graph(
            id='world',
            figure = px.choropleth(df[df['Indicator Name'] == 'GDP growth (annual %)'], 
                        locations="Country Code", 
                        color="Value", 
                        hover_name="Country Name",
                        animation_frame="Year",
                        width = 1000,
                        height = 750,
                        range_color = [0,10],
                        title = ' CPLP Countries: GDP growth (annual %) from 2010 to 2020')
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
])

urbanism_indicators = df[df['Area']=='Urbanism']['Indicator Name'].unique()

layout_urbanism = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column_u',
                options=[{'label': i, 'value': i} for i in urbanism_indicators],
                value='Proportion of population using basic drinking water services, RURAL (%)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type_u',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column_u',
                options=[{'label': i, 'value': i} for i in urbanism_indicators],
                value='Proportion of population using basic drinking water services, URBAN (%)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type_u',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter_u',
            hoverData={'points': [{'customdata': 'Portugal'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series_u'),
        dcc.Graph(id='y-time-series_u'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider_u',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter_u', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column_u', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column_u', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type_u', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type_u', 'value'),
     dash.dependencies.Input('crossfilter-year--slider_u', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[(df['Year'] == year_value) & (df['Area'] == 'Urbanism')]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 20, 'r': 0},
            height=500,
            hovermode='closest'
        )
    }

def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 250,
            'margin': {'l': 30, 'b': 60, 'r': 20, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('x-time-series_u', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter_u', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column_u', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type_u', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

@app.callback(
    dash.dependencies.Output('y-time-series_u', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter_u', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column_u', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type_u', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

health_indicators = df[df['Area']=='Health']['Indicator Name'].unique()

layout_health = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column_h',
                options=[{'label': i, 'value': i} for i in health_indicators],
                value='Neonatal mortality rate (deaths per 1,000 live births)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type_h',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column_h',
                options=[{'label': i, 'value': i} for i in health_indicators],
                value='Prevalence of undernourishment (%)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type_h',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter_h',
            hoverData={'points': [{'customdata': 'Portugal'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series_h'),
        dcc.Graph(id='y-time-series_h'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider_h',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter_h', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column_h', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column_h', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type_h', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type_h', 'value'),
     dash.dependencies.Input('crossfilter-year--slider_h', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[(df['Year'] == year_value) & (df['Area'] == 'Health')]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'green'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 20, 'r': 0},
            height=500,
            hovermode='closest'
        )
    }

def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 250,
            'margin': {'l': 30, 'b': 60, 'r': 20, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('x-time-series_h', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter_h', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column_h', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type_h', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

@app.callback(
    dash.dependencies.Output('y-time-series_h', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter_h', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column_h', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type_h', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

monetary_indicators = df[df['Area']=='Monetary']['Indicator Name'].unique()

layout_monetary = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column_m',
                options=[{'label': i, 'value': i} for i in monetary_indicators],
                value='Number of commercial bank branches per 100,000 adults'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type_m',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column_m',
                options=[{'label': i, 'value': i} for i in monetary_indicators],
                value='GDP growth (annual %)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type_m',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter_m',
            hoverData={'points': [{'customdata': 'Portugal'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series_m'),
        dcc.Graph(id='y-time-series_m'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider_m',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter_m', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column_m', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column_m', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type_m', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type_m', 'value'),
     dash.dependencies.Input('crossfilter-year--slider_m', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[(df['Year'] == year_value) & (df['Area'] == 'Monetary')]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 20, 'r': 0},
            height=500,
            hovermode='closest'
        )
    }

def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 250,
            'margin': {'l': 30, 'b': 60, 'r': 20, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('x-time-series_m', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter_m', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column_m', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type_m', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

@app.callback(
    dash.dependencies.Output('y-time-series_m', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter_m', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column_m', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type_m', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

enviroment_indicators = df[df['Area']=='Enviroment']['Indicator Name'].unique()

layout_enviroment = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column_e',
                options=[{'label': i, 'value': i} for i in enviroment_indicators],
                value='Carbon dioxide emissions from fuel combustion (millions of tonnes)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type_e',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column_e',
                options=[{'label': i, 'value': i} for i in enviroment_indicators],
                value='Forest area as a proportion of total land area (%)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type_e',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter_e',
            hoverData={'points': [{'customdata': 'Portugal'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series_e'),
        dcc.Graph(id='y-time-series_e'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider_e',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter_e', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column_e', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column_e', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type_e', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type_e', 'value'),
     dash.dependencies.Input('crossfilter-year--slider_e', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[(df['Year'] == year_value) & (df['Area'] == 'Enviroment')]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 20, 'r': 0},
            height=500,
            hovermode='closest'
        )
    }

def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 250,
            'margin': {'l': 30, 'b': 60, 'r': 20, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('x-time-series_e', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter_e', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column_e', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type_e', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

@app.callback(
    dash.dependencies.Output('y-time-series_e', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter_e', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column_e', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type_e', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

#################################################################################################################################3
# Page Layout

img = Image.open('images_LOG.png')

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.Img(src=img, className = 'logo', height="60px"),
    html.H1(
        children='Tracking the sustainable development goals before the pandemic',
        style={
            'textAlign': 'center',
            'color': '#053B78'
        }
    ),

    html.Div(children='SGD on CPLP Country.', style={
        'textAlign': 'center',
        'color': '#053B78'
    }),
    
    
    dcc.Tabs(
             id="tabs", value='tab-1', children=[
        dcc.Tab(label='Home', value='tab-1'),
        dcc.Tab(label='Urbanism', value='tab-2'),
        dcc.Tab(label='Health', value='tab-4'),
        dcc.Tab(label='Monetary', value='tab-5'),
        dcc.Tab(label='Enviroment', value='tab-6'),
        dcc.Tab(label='Data Source', value='tab-7'),
    ]),
    
     html.Div(id='tabs-content'
    ),
    

])
############################################################################################################################################################


@app.callback(
    Output('tabs-content', 'children'),
     [Input('tabs', 'value')],
     
     )
############################################################################################################################################################




def render_content(tab):
    if tab == 'tab-1':
        return ([dcc.Markdown('''
                    In order to end the poverty and set the world on a path of peace, prosperity and opportunity for all on a healthy planet was launched in 2015 the 2030 Agenda for Sustainable Development by United Nations. The last report available contains data before the covid-19 pandemic. The actual pandemic has been putting at risk the 2030 agenda. As example, according with before the pandemic the progress has been uneven among the areas and after many of the implementations on SDGs turned back ages of progress. 

                    The goal on this dashboard is to track some of the indicators on SDGs among countries who belong to the community of Portuguese Speaker (CPLP) before the pandemic. On the dashboard is possible to compare among the CPLP countries, the progress of 12 indicators before the Covid-19 pandemic. These indicators gave a view of the progress made on the following areas: Urbanisn, Health, Monetary, environment.    

                    The indicator???s data available range between 2010 to 2018, although some have information until 2019. In order to make it easier to analyse the information, were chosen familiar graphics like dote charts, line charts and the user is allowed to select a country and see the progress off each indicator.  among them.
                    '''),    
                    layout_home,
                    dcc.Markdown('''        
                    Group AN: Geraldo Timbe, m20200603 | Manuel A. F. Carreiras, m20200500 | Luis F. R. Agottani, m20200621 | Ven??ncio Munhangane, m20200579 |
                    ''')])
    elif tab == 'tab-2':
        return ([dcc.Markdown('''
                    ## Select indicators and year for analysis.
                    '''),  
                layout_urbanism ])  
    elif tab == 'tab-4':
        return ([dcc.Markdown('''
                    ## Select indicators and year for analysis.
                    '''), 
                layout_health])
    elif tab == 'tab-5':
        return ([dcc.Markdown('''
                    ## Select indicators and year for analysis.
                    '''), 
                layout_monetary])
    elif tab == 'tab-6':
        return ([dcc.Markdown('''
                    ## Select indicators and year for analysis.
                    '''), 
                layout_enviroment])
    elif tab == 'tab-7':
        return dcc.Markdown('''
                    # Links for download:
                    * https://unstats.un.org/sdgs/indicators/database/

                    * http://www.fao.org/faostat/en/#data

                    * https://databank.worldbank.org/source/world-development-indicators

                    # GitHub

                    * https://github.com/luisfernandoagottani/DataVisualization
                    ''')   


if __name__ == '__main__':
    app.run_server(debug= True)

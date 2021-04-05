import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash
import plotly.express as px
from dash.dependencies import Input, Output

df = pd.read_excel('Indicadores_base.xlsx', sheet_name = 'All_data')


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
#################################################################################################################################3
# Page Layout

app = dash.Dash(__name__,suppress_callback_exceptions=True)

server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(
        children='Tracking the sustainable development goals before the pandemic',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='SGD on CPLP Country.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
    
    dcc.Tabs(
             id="tabs", value='tab-1', children=[
        dcc.Tab(label='Home', value='tab-1'),
        dcc.Tab(label='Urbanism', value='tab-2'),
        dcc.Tab(label='Health', value='tab-4'),
        dcc.Tab(label='Monetary', value='tab-5'),
        dcc.Tab(label='Enviroment', value='tab-6'),
        dcc.Tab(label='Data Download', value='tab-7'),
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
        return layout_urbanism
    elif tab == 'tab-2':
        return html.P("This is the content of page 1. Yay!")  
    elif tab == 'tab-4':
        return html.P("This is the content of page 1. Yay!")
    elif tab == 'tab-5':
        return html.P("This is the content of page 1. Yay!")
    elif tab == 'tab-6':
        return html.P("This is the content of page 1. Yay!")
    elif tab == 'tab-7':
        return html.P("This is the content of page 1. Yay!")

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
                'color': '#0470A3',
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


if __name__ == '__main__':
    app.run_server(debug= True)

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

#################################################################################################################################3
# Page Layout

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
        return html.P("This is the content of page 1. Yay!")
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

if __name__ == '__main__':
    app.run_server(debug= True)

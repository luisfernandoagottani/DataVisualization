import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash
import plotly.express as px
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

server = app.server

df = pd.read_excel('Indicadores_base.xlsx', sheet_name = 'All_data')

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
                        title = ' CPLP Countries: GDP growth (annual %)')
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
])
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
        return layout_home
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

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash
import plotly.express as px
from dash.dependencies import Input, Output

df_emissions = pd.read_csv('emission_full.csv')

df_emission_0 = df_emissions.loc[df_emissions['year']==2000]

# Building our Graphs (nothing new here)

data_choropleth = dict(type='choropleth',
                       locations=df_emission_0['country_name'],  #There are three ways to 'merge' your data with the data pre embedded in the map
                       locationmode='country names',
                       z=np.log(df_emission_0['CO2_emissions']),
                       text=df_emission_0['country_name'],
                       colorscale='inferno',
                       colorbar=dict(title='CO2 Emissions log scaled')
                      )

layout_choropleth = dict(geo=dict(scope='world',  #default
                                  projection=dict(type='orthographic'
                                                 ),
                                  #showland=True,   # default = True
                                  landcolor='black',
                                  lakecolor='white',
                                  showocean=True,   # default = False
                                  oceancolor='azure'
                                 ),
                         
                         title=dict(text='World Choropleth Map',
                                    x=.5 # Title relative position according to the xaxis, range (0,1)
                                   )
                        )

fig = go.Figure(data=data_choropleth, layout=layout_choropleth)

layout_teste = html.Div(children=[
    html.H1(children='My First DashBoard'),

    html.Div(children='''
        Example of html Container
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
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
        return layout_teste
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

# import dash
# from dash.dependencies import Input, Output
# import dash_core_components as dcc
# import dash_html_components as html

import pandas as pd
import json

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
# import dash_datetimepicker as dt
from datetime import datetime as dt
import dbm
import plotly.graph_objs as go
import plotly.express as px
import re
# import smtp_alert





global df
global app_sel

df=pd.read_json("sampledata.json")
app_sel=list(set(df['cf_app_name']))
print(df['cf_app_name'].unique())
# Set up the app
app = dash.Dash(__name__)
server = app.server

def get_options(list_items):
    dict_list = []
    for i in list_items:
        dict_list.append({'label': i, 'value': i})

    return dict_list

# app.layout = html.Div()
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='three columns div-user-controls',
                                  children=[
                                 html.H2('APPLICATION ERROR DASHBOARD'),
                                 html.Br(),
                                
                                 html.P('CHOOSE TIME INTERVAL'),
                               
                                

                                 html.Br(),
                                 html.Br(),
                                 html.P('Select Applications'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='appselector', options=get_options(df['cf_app_name'].unique()),
                                                      multi=True, value=[df['cf_app_name'].sort_values()[0]],
                                                      

                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='appselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'}),
                                     html.Br(),
                                     
                                     html.P('Select Exceptions'),
                                html.Div(  
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='exselector', options=get_options(df['Exception_Name'].unique()),
                                                      multi=True, value=[df['Exception_Name'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='exselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'}),
                                     html.Br(),
                                     html.Br(),
                                     

                                     
                               
                                     
                                ]),  # Define the left element
                                  html.Div(className='nine columns div-for-charts bg-grey', style={'font_size': '30px','font_family':'Georgia','text-align':'center'}, # Define the right element
                                  children=[
        # dcc.Graph(id='timeseries',
        #   config={'displayModeBar': False},
        #   animate=True,
        #   figure=px.line(df,
        #                  x='timestamp8601',
        #                  y='cf_app_name',
        #                  color='Exception_Name',
        #                  template='plotly_dark').update_layout(
        #                            {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        #                             'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        #                             ),
                                    html.Div([
                                  html.H2(' ERROR INFORMATION'),
                                  html.Br(),
                                  dash_table.DataTable(
                                      id='logtable',
                                    columns=[
                                        {'name': 'Timestamp', 'id': 'timestamp8601', 'type': 'text'},
                                        {'name': 'Application Name', 'id': 'cf_app_name', 'type': 'text'},
                                        {'name': 'Exception Name', 'id': 'Exception_Name', 'type': 'text'},
                                        {'name': 'Error Message', 'id': 'Error_Message', 'type': 'text'},
                                        {'name': 'Exception Details', 'id': 'Exception_Details', 'type': 'text'}
                                    ],
                                    data=df.to_dict('records'),
                                    filter_action='native',
                                    
        
                                     style_table={
                                        'height': 1400,
                                        'overflow-wrap': 'break-word',
                                    },
                                    style_data={
                                        'width': 'auto', 'maxWidth': '150px',
                                        'height':'auto',
                                        'overflow': 'visible',
                                        'textOverflow': 'ellipsis',
                                        'overflow-wrap': 'break-word',
                                        'word-wrap':'break-word',
                                        # 'font-color':'black'
                                    },
                                    style_header={
                                        # 'backgroundColor': '#0FA0CE',
                                        'backgroundColor': 'orange',
                                        'fontWeight': 'bold',
                                        'font_size':'18px',
                                        # 'font_family': "Open Sans Bold"
                                    },
                                     style_cell = {
                                            'font_family': "Open Sans Semi Bold",
                                            'font_size': '18px',
                                            'text_align': 'left',
                                            'backgroundColor':'white',
                                            'color':'black',
                                            'overflow-wrap': 'break-word',
                                            'white-space':'pre-wrap',
                                            'word-wrap':'break-word',
                                        },
                                        
                                ),
                                    html.P(''),
                                ], style={'width': '100%','height':'50%', 'float': 'right', 'display': 'inline-block'}),

        
                                  ])])])

                                                          
@app.callback(Output('logtable', 'data'), [Input('appselector', 'value'),Input('exselector', 'value')])

def update_rows(appselector,exselector):
    # dff = df[df['cf_app_name'] == selected_value]
    dff = df[df['cf_app_name'].isin(appselector)]
    dff = dff[dff['Exception_Name'].isin(exselector)]
    return dff.to_dict('records')



if __name__ == '__main__':
    app.run_server(debug=True)



# For the product price graph individual
# @app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
# def update_graph(selected_dropdown_value):
#     product_df_filter = product_df[(product_df['product_title'].isin(selected_dropdown_value))]
#
#     return {
#         'data': [{
#             'x': product_df_filter.datetime,
#             'y': product_df_filter.product_price
#         }]
#     }
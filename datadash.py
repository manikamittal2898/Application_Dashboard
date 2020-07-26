# import dash
# from dash.dependencies import Input, Output
# import dash_core_components as dcc
# import dash_html_components as html
from flask import Flask, request
# from datetime import datetime
import os
# import json
from flask.helpers import send_file, send_from_directory
from mongoConnect2 import mongoConnect2
import dateutil.parser as parser
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
from plotly.graph_objs import *
from datetime import datetime as dt
from datetime import date
import dateutil.parser as parser




global df
global sdate
global edate

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

# global app_sel
# print(date.today().year)
mc = mongoConnect2()
path="C:\\Users\\User\\Desktop\\DELL\\dashboard\\Json_local_storage\\"
app_list = ["IPSDashboard-UX", "support-ode-ux", "Documents-UX",
 "Advisories-UX", "guidedPath-ux-prod", "OrderStatusUX", "KbArticle-UX",
  "article-ux", "flatcontents-ux","ProductSupport-UX","security-portal-ux",
  "masthead-ux","support-home-ux","drivers-ux","sonar-validator-ux"]

from_date = dt(2020, 7, 14, 12, 50)
to_date = dt(2020, 7, 14, 12, 55)
r=mc.find_document(from_date, to_date)
out_file = open("file.json", "w")     
json.dump(r, out_file, indent = 6)     
out_file.close()

df=pd.read_json("file.json")
os.remove("file.json")
# df=pd.read_json("sampledata.json")

app_sel=list(set(df['cf_app_name']))
print(df['cf_app_name'].unique())

# Set up the app
# server = Flask(__name__)
app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server


def get_options(list_items):
    dict_list = []
    for i in list_items:
        dict_list.append({'label': i, 'value': i})

    return dict_list

# app.layout = html.Div()
# @server.route('/dashboard')
# def dashdisplay():
app.layout = html.Div(children=[
                        html.Div(className='row',  # Define the row element
                                children=[
                                    html.Div(className='three columns div-user-controls',
                                    children=[
                                    html.H2('APPLICATION ERROR DASHBOARD'),
                                    html.Br(),
                                    
                                    html.H4('Select Start Date'), 
    #                                  dcc.DatePickerRange(id='calendar',
    #     start_date_placeholder_text="Start Period",
    #     end_date_placeholder_text="End Period",
    #     calendar_orientation='vertical',

    # ),
    html.Div(
                                className="div-for-dropdown",
                                children=[
                                    dcc.DatePickerSingle(
                                        id="datepicker",
                                        min_date_allowed=dt(2020, 1, 1),
                                        max_date_allowed=dt(2050, 12, 31),
                                        # today = date.today()
                                        initial_visible_month=add_years(date.today(),-1),
                                        # date=dt(2014, 4, 1).date(),
                                        date=add_years(date.today(),-1),
                                        display_format="MMMM D, YYYY",
                                        style={"border": "0px solid black"},
                                    )
                                ],
                            ),
                            html.H4('Select End Date'), 
    #                                  dcc.DatePickerRange(id='calendar',
    #     start_date_placeholder_text="Start Period",
    #     end_date_placeholder_text="End Period",
    #     calendar_orientation='vertical',

    # ),
    html.Div(
                                className="div-for-dropdown",
                                children=[
                                    dcc.DatePickerSingle(
                                        id="datepicker2",
                                        min_date_allowed=dt(2020, 1, 1),
                                        max_date_allowed=dt(2050, 12, 31),
                                        # today = date.today()
                                        initial_visible_month=date.today(),
                                        # date=dt(2014, 4, 1).date(),
                                        date=date.today(),
                                        display_format="MMMM D, YYYY",
                                        style={"border": "0px solid black"},
                                    )
                                ],
                            ),
                                
                                    

                                    html.Br(),
                                    html.Br(),
                                    html.H4('Select Applications'),
                                    html.Div(
                                        className='div-for-dropdown',
                                        children=[
                                            dcc.Dropdown(id='appselector', options=get_options(df['cf_app_name'].unique()),
                                                        multi=True,
                                                        value=[df['cf_app_name'].sort_values()[0]],
                                                        

                                                        style={'backgroundColor': '#1E1E1E'},
                                                        className='appselector'
                                                        # placeholder="Select certain hours"
                                                        ),
                                        ],
                                        style={'color': '#1E1E1E'}),
                                        html.Br(),
                                        
                                        html.H4('Select Exceptions'),
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

# return "success"                                                         
@app.callback(Output('logtable', 'data'), [Input('appselector', 'value'),Input('exselector', 'value'),Input("datepicker2", "date")])

def update_rows(appselector,exselector,datePicked):
    # dff = df[df['cf_app_name'] == selected_value]
    dff = df[df['cf_app_name'].isin(appselector)]
    dff = dff[dff['Exception_Name'].isin(exselector)]
    # dff = dff[dff['timestamp8601']==calendar]
    date_picked = dt.strptime(datePicked+str("-12-52-02"), "%Y-%m-%d-%H-%M-%S")
    date_picked=parser.parse(str(date_picked)).isoformat()
    # dff = dff[str(dff['timestamp8601'])==str(date_picked)]
    # new_results = results.loc[start_date: end_date]
    # print(dff['timestamp8601']==date_picked)
    print(date_picked)
    # print(parser.parse(str(date_picked)).isoformat())
    print("hello")
    print(dff)

    return dff.to_dict('records')


# @app.callback(Output("logtable", "data"), [Input("date-picker", "date")])
# def update_total_rides(datePicked):
#     date_picked = dt.strptime(datePicked+str("-0"), "%Y-%m-%d-%H")
#     dff = df[df['timestamp8601']==date]
#     return dff.to_dict('records')
    



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
from dash import Dash, html, dcc, Input, Output,dash_table


import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from firebase import firebase
import plotly.graph_objects as go

dash.register_page(__name__,path='/admin')
firebase_app=firebase.FirebaseApplication('https://hospital-data-analysis-default-rtdb.asia-southeast1.firebasedatabase.app/')

def connect_firebase():
    result=firebase_app.get('https://hospital-data-analysis-default-rtdb.asia-southeast1.firebasedatabase.app/users','')
    yesc=0
    noc=0
    for i in result:
        if result[i]['feed1']=="Yes":
            yesc+=1
        else:
            noc+=1
    total=len(result.keys())
    return result,total,yesc,noc
result,total,yesc,noc=connect_firebase()
print(result)
# feeds=[dbc.Card([html.Div([html.P(result[_]["feed2"],style={'color':'white'})],className='container')],className="sm-cards border border-danger" ,color="dark")
# for _ in result.keys()]
layout=[
      html.H1("Admin Dashboard"),
    #   html.Div(id='intermediate-value', style={'display': 'none'}, children = [result,yesc,noc,total]),
      

        html.Div([
              dbc.Row(
                [
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P("Total feedback", className="card-title"),
                                    html.H4(
                                        [total],
                                        className="card-text",id='total'
                                    ),
                                ]
                            ),className="sm-cards border border-info" ,color="dark"
                        )
                    ],sm=4),
                    dbc.Col([dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P("Total positive feedback", className="card-title"),
                                    html.H4(
                                        [yesc],
                                        className="card-text",id='yes'
                                    ),
                                ]
                            ),className="sm-cards border border-info" ,color="dark")],sm=4),

                    dbc.Col([dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P("Total negative feedback", className="card-title"),
                                    html.H4(
                                        [noc],
                                        className="card-text",id='no'
                                    ),
                                ]
                            ),className="sm-cards border border-info" ,color="dark")],sm=4)

                ]),
                dbc.Row(
                    [
                        html.Center(html.H3("Feedback:")),
                        dbc.Row([
                            dbc.Col([],sm=4),
                            dbc.Col([ 
                                dbc.Card([html.Div([html.P(result[_]["feed2"],style={'color':'white'})],className='container')],className="sm-cards border border-danger" ,color="dark")for _ in result.keys()

                        
                        ],sm=4,id='feed')
                       
                        
                    ]
                )
        ])
])]

# @dash.callback(
#     Output('total', 'children'),
#     Output('yes','children'),
#     Output('no','children'),
#     Output('feed','children')
# )

# def update():
    
#     return total,yesc,noc,feeds

# @dash.callback(Output('intermediate-value', 'children'),
#               [Input('interval-component', 'n_intervals')])

# def update_global_var():
#     return connect_firebase()



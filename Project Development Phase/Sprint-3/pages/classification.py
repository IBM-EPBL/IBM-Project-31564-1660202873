from dash import Dash, html, dcc, Input, Output,dash_table
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__,path='/classification')
hospital_code_options =[x for x in range(1,33)]
hospital_type_code_options =[{'label':'a','value':0},{'label':'b','value':1},{'label':'c','value':2},{'label':'d','value':3},{'label':'e','value':4},{'label':'f','value':5},{'label':'g','value':6}]
department_options=[{'label':'TB & chest disease','value':0},{'label':'anesthesia','value':1},{'label':'gynecology','value':2},{'label':'radiotherapy','value':3},{'label':'surgery','value':4}]
wardType_options=[{'label':'P','value':0},{'label':'Q','value':1},{'label':'R','value':2},{'label':'S','value':3},{'label':'T','value':4},{'label':'U','value':5}]
bedGrade_options=[{'label':'1','value':0},{'label':'2','value':1},{'label':'3','value':2},{'label':'4','value':3}]
typeofAdmission_options=[{'label':'Emergency','value':0},{'label':'Trauma','value':1},{'label':'Urgent','value':2}]
Age_options=[{'label':'0-10','value':0},{'label':'11-20','value':1},{'label':'21-30','value':2},{'label':'31-40','value':3},{'label':'41-50','value':4},
 {'label':'51-60','value':5},{'label':'61-70','value':6},{'label':'71-80','value':7},{'label':'81-90','value':8},{'label':'91-100','value':9},{'label':'more than 100','value':10}]

layout= html.Div(
    [
        dbc.Container(
            [
                html.H1("Prediction of Lenght of Stay"),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col([
                                    
                                ])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)




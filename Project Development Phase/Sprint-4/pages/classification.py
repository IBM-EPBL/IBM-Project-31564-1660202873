from dash import Dash, html, dcc, Input, Output,State
import dash
import dash_bootstrap_components as dbc
# from app import model
import numpy as np
import pickle
from firebase import firebase
dash.register_page(__name__,path='/classification')
firebase_app=firebase.FirebaseApplication('https://hospital-data-analysis-default-rtdb.asia-southeast1.firebasedatabase.app/')


with open('rfc_model.pickle', 'rb') as f:
        model = pickle.load(f)




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
                html.Div(
                    [
                    html.H1("Prediction of Lenght of Stay"),
                    html.Div(
                        [
                            dbc.Row(
                                [

                                    dbc.Col([html.Label("Hospital Code: "),dcc.Dropdown(options=hospital_code_options,value=1,id="hospital_code")]),
                                    dbc.Col([html.Label("Hospital Type Code: "),dcc.Dropdown(options=hospital_type_code_options,value=0,id="Hospitaltypecode")]),
                                    dbc.Col([html.Label("Department: "),dcc.Dropdown(options=department_options,value=0,id="Department")])
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col([html.Label("Ward Type: "),dcc.Dropdown(options=wardType_options,value=0,id="wardType")]),
                                    dbc.Col([html.Label("Bed Grade: "),dcc.Dropdown(options=bedGrade_options,value=0,id="bedGrade")]),

                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col([html.Label("Type of Admission: "),dcc.Dropdown(options=typeofAdmission_options,value=0,id="typeofAdmission")]),
                                    
                                ]
                            ),
                            html.Br(),
                            html.Center([
                            html.Label("No of visitors: "),html.Br(),dcc.Input(type="number",value=0,id="no_visitors"),html.Br(),
                            ]),
                            html.Br(),
                            dbc.Row(dbc.Col([html.Label("Age: "),dcc.Dropdown(options=Age_options,value=0,id='Age')])),
                            html.Br(),
                            html.Center(dbc.Button("Predict", color="info",n_clicks=0,id='predict'))
                            


                        ],className='boxed'
                    ),
                    html.Div([
                        html.H5('Predicted Length of Stay: '),
                        html.Div(id="output"),
                        html.Div([
                        html.Br(),
                        html.Center([html.H5("Feedback"),
                            html.Label("Are you satisfied with the prediction: "),
                            dcc.RadioItems(['Yes','No'],value="Yes",id="feed1",style={'width':'60%'}),
                        html.Label("Give feedback:"),
                        html.Br(),
                        dcc.Textarea(id='feed2',style={'width':'60%'}),
                        html.Center(dbc.Button("Submit", color="info",n_clicks=0,id='submit')),
                        html.P(id='out2')

        ])
        ])
                    ],className='boxed1')
                ]
            )
            ])
    ]
)



@dash.callback(
    Output('output', 'children'),
    Input('predict', 'n_clicks'),
    State('hospital_code', 'value'),
    State('Hospitaltypecode','value'),
    State('Department','value'),
    State('wardType','value'),
    State('bedGrade','value'),
    State('typeofAdmission','value'),
    State('no_visitors','value'),
    State('Age','value')
)

def update_output(n_clicks,hospital_code,hospitaltypecode,Department,wardType,bedGrade,typeofAdmission,no_visitors,Age):
    prediction=model.predict([np.array([hospital_code,hospitaltypecode,Department,wardType,bedGrade,typeofAdmission,no_visitors,Age])])
    
    if prediction[0]==0:
        prediction_ans= "0-10 days"
    elif prediction[0]==1:
        prediction_ans="11-20 days"
    elif prediction[0]==2:
        prediction_ans="21-30 days"
    elif prediction[0]==3:
        prediction_ans="31-40 days"
    elif prediction[0]==4:
        prediction_ans="41-50 days"
    elif prediction[0]==5:
        prediction_ans="51-60 days"
    elif prediction[0]==6:
        prediction_ans="61-70 days"
    elif prediction[0]==7:
        prediction_ans="71-80 days"
    elif prediction[0]==8:
        prediction_ans="81-90"
    elif prediction[0]==9:
        prediction_ans="91-100"
    elif prediction[0]==10:
        prediction_ans="more than 100 days"
    else:
        prediction_ans="Sorry couldn't predict Lenght of Stay"
    return [html.H3(prediction_ans)]
@dash.callback(
        Output('out2', 'children'),
        Input('submit', 'n_clicks'),
        State('feed1', 'value'),
        State('feed2','value')
    )
def update2(n_clicks,feed1="",feed2=""):
    ret_val=""
    if feed1!="" and feed2!=None:

        ret_val =html.P("Feedback Submitted",style={'color':'green'})
        data={'feed1':feed1, 'feed2':feed2}
        result=firebase_app.post('https://hospital-data-analysis-default-rtdb.asia-southeast1.firebasedatabase.app/users',data)
        print(result)
    return ret_val


    






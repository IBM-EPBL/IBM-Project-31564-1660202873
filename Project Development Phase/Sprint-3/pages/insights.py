from dash import Dash, html, dcc, Input, Output,dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy
from sklearn import preprocessing
import plotly.graph_objects as go
from collections import OrderedDict

import dash

table_data = OrderedDict(
    [
        ("Stay", [0,1,2,3,4,5,6,7,8,9,10]),
        ("Days", ["0-10 days","11-20 days","21-30 days","31-40 days","41-50 days","51-60 days","61-70 days","71-80 days","81-90 days","91-100 days","more than 100 days"])
    ])
table_df = pd.DataFrame(table_data)

dash.register_page(__name__,path='/insights')
le = preprocessing.LabelEncoder()
hospital = pd.read_csv('train_data.csv')
dpb_options3=["Hospital_code","Department","Bed Grade","Type of Admission","Severity of Illness","Age","Ward_Type","Ward_Facility_Code","Hospital_region_code","Hospital_type_code"]
col_dropdown = dcc.Dropdown(options=dpb_options3,value="Hospital_code")

layout= html.Div(
    [
        html.H3("Mean Length of Stay",className='heading'),
                    dbc.Row(
                        [
                            dbc.Col("",sm=1),
                            dbc.Col(html.H5("Select Attribute for x-axis: ",id="label"),sm=3),
                            dbc.Col(col_dropdown,sm=7)
                        ],className='top-space'
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dash_table.DataTable(
                                 data=table_df.to_dict('records'),
                                 columns=[{'id': c, 'name': c} for c in table_df.columns],
                                 style_header={
                                    'backgroundColor': 'rgb(30, 30, 30)',
                                    'color': 'white'
                                },
                                style_data={
                                    'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white'
                                },
                                ),sm=3
                            ),
                            dbc.Col(
                                dbc.Card
                                (
                                    dbc.CardBody(
                                        [    
                                               dcc.Graph(id='final_graph'),
                                            #    dcc.RangeSlider(min=0, max=7000, step=1000, value=[3000, 6000], id='admission_deposit_slider')
                                        ]
                                    ),color='secondary'
                                ),
                            
                            )
                        ]
                    )
    ]
)

@dash.callback(
    Output(component_id='final_graph', component_property='figure'),  
    Input(component_id=col_dropdown, component_property='value'),
    # Input(component_id='admission_deposit_slider', component_property='value')
)

def update_final_graph(selected_col):
    le.fit(hospital["Stay"])
    transformed = le.transform(hospital["Stay"])
    hospital["Stay"] = transformed
    df=hospital.groupby(selected_col).mean()
    count_=hospital.groupby(selected_col).count()
    df['Stay']=df['Stay'].round(decimals=2)
    df['Admission_Deposit']=df['Admission_Deposit'].round(decimals=2)
   
    bubble=px.scatter(df,x=df.index,y='Stay',color='Admission_Deposit',size=count_['patientid'],labels={'size':'No of patients','Stay':'Mean Stay','Admission_Deposit':'Mean Admission Deposit'})
    bubble.update_layout(yaxis_range=[0,11])
    return bubble
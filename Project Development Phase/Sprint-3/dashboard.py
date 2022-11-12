from dash import Dash, html, dcc, Input, Output,dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy
from sklearn import preprocessing
import plotly.graph_objects as go
from collections import OrderedDict

le = preprocessing.LabelEncoder()

hospital = pd.read_csv('train_data.csv')
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

hospital.info()

dpb_options=sorted(hospital['Hospital_code'].unique())
dpb_options2=numpy.append(dpb_options,["ALL"])
dpb_options3=["Hospital_code","Department","Bed Grade","Type of Admission","Severity of Illness","Age"]
hos_dropdown = dcc.Dropdown(options=dpb_options2,value="ALL")
col_dropdown = dcc.Dropdown(options=dpb_options3,value="Hospital_code")
noPatient=len(hospital['patientid'])
noHospitals=len(hospital['Hospital_code'].unique())
noDepartments=len(hospital['Department'].unique())

table_data = OrderedDict(
    [
        ("Stay", [0,1,2,3,4,5,6,7,8,9,10]),
        ("Days", ["0-10 days","11-20 days","21-30 days","31-40 days","41-50 days","51-60 days","61-70 days","71-80 days","81-90 days","91-100 days","more than 100 days"])
    ])
table_df = pd.DataFrame(table_data)


"""___nav bar___"""
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="#",active=True),className="navstyle"),
        dbc.NavItem(dbc.NavLink("Classification",href="#"),className="navstyle")
           
    ],
    brand="Health Care Data Analysis",
    brand_href="#",
    color="primary",
    dark=True,
)

app.layout = html.Div(
    children=[
        navbar,
        html.Div(dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col([
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P("Total no of cases", className="card-title"),
                                        html.H4(
                                            noPatient,
                                            className="card-text",
                                        ),
                                    ]
                                ),className="sm-cards border border-info" ,color="dark"
                            )
                        ],sm=4),
                        
                        dbc.Col([
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P("Total no of hospitals", className="card-title"),
                                        html.H4(
                                            noHospitals,
                                            className="card-text",
                                        ),
                                    ]
                                ),className="sm-cards border border-info",color="dark"
                            )
                        ],sm=4),
                        
                        dbc.Col([
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P("Total no of Departments", className="card-title"),
                                        html.H4(
                                            noDepartments,
                                            className="card-text",
                                        ),
                                    ]
                                ),className="sm-cards border border-info",color="dark"
                            )
                        ],sm=4)

                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col("",sm=3),
                        dbc.Col(html.H5("Select Hospital: ",id="label"),sm=3),
                        dbc.Col(hos_dropdown,sm=3)
                        ],className='top-space'),
                dbc.Row(
                    [
                        dbc.Col([
                            dbc.Card
                            (
                                dbc.CardBody(
                                    [
                                        
                                            dcc.Graph(id='graph')
                        
                                    ]
                                ),color="dark"
                            ),
                            dbc.Card
                            (
                                dbc.CardBody(
                                    [    
                                            dcc.Graph(id='Severity_graph')
                                    ]
                                ),color='secondary'
                            ),
                            ],sm=7),
                        dbc.Col(
                            [
                            dbc.Row(
                                # dcc.Graph(figure=DepartmentFig,className='border border-warning')
                                dcc.Graph(id='dept_graph'),className='border border-warning'
                            ),
                            dbc.Row(
                                dcc.Graph(id='Admission_graph'),className='border border-danger top-space'
                            )
                            ],sm=5                          
                        )
                        
                    ]),
                    html.H3("Mean Lenght of Stay",className='heading'),
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
                                               dcc.Graph(id='final_graph')
                                        ]
                                    ),color='secondary'
                                ),
                            
                            )
                        ]
                    )
            ]
            ))
        ])
@app.callback(
    Output(component_id='graph', component_property='figure'),  
    Output(component_id='dept_graph', component_property='figure'), 
    Output(component_id='Admission_graph',component_property='figure'),
    Output(component_id='Severity_graph',component_property='figure'),
    Input(component_id=hos_dropdown, component_property='value')
)
def update_graph(selected_Hospital_code):
    if(selected_Hospital_code=='ALL'):
        filtered_hospital=hospital
    else:
        filtered_hospital = hospital[hospital['Hospital_code'] == int(selected_Hospital_code)]
    stay_df=filtered_hospital.groupby('Stay').count()
    department_df=filtered_hospital.groupby('Department').count()
    DepartmentFig=px.scatter(department_df,x=department_df.index,y='patientid',template='plotly_dark',labels={'patientid':'No of patients'},height=250)
    line_fig=px.line(stay_df,x=stay_df.index,y='patientid',template='plotly_dark',title='No of patients in each stay',labels={'patientid':'No of patients'},height=250)

    Admission_df=filtered_hospital.groupby('Age').count()
    pie_fig=px.pie(Admission_df,names=Admission_df.index,values='patientid',template='plotly_dark',labels={'patientid':'No of patients'},height=250,color_discrete_sequence=px.colors.sequential.RdBu,title='Patients by age')
    pie_fig.update_layout(margin=dict(t=35, b=25, l=0, r=0))


    Severity_df=filtered_hospital.groupby('Severity of Illness').count()
    bar_fig=px.bar(Severity_df,x=Severity_df.index,y='patientid',height=200,template='plotly_dark',labels={'patientid':'No of patients'})
    return line_fig,DepartmentFig,pie_fig,bar_fig




# print(hospital.head(10))

@app.callback(
    Output(component_id='final_graph', component_property='figure'),  
    
    Input(component_id=col_dropdown, component_property='value')
)

def update_final_graph(selected_col):
    le.fit(hospital["Stay"])
    transformed = le.transform(hospital["Stay"])
    hospital["Stay"] = transformed
    df=hospital.groupby(selected_col).mean()
    count_=hospital.groupby(selected_col).count()
    df['Stay']=df['Stay'].round(decimals=2)
    df['Admission_Deposit']=df['Admission_Deposit'].round(decimals=2)
    # df['Stay']=le.inverse_transform(df['Stay'])
    bubble=px.scatter(df,x=df.index,y='Stay',color='Admission_Deposit',size=count_['patientid'],labels={'size':'No of patients','Stay':'Mean Stay','Admission_Deposit':'Mean Admission Deposit'})
    bubble.update_layout(yaxis_range=[0,11],template='plotly_dark')
    return bubble

if __name__ == '__main__':
    app.run_server(debug=True)
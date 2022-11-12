from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy
hospital = pd.read_csv('train_data.csv')
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

hospital.info()
# print("Otha",type(hospital['Hospital_code'].unique()))
dpb_options=sorted(hospital['Hospital_code'].unique())
dpb_options2=numpy.append(dpb_options,["ALL"])
hos_dropdown = dcc.Dropdown(options=dpb_options2,value="ALL")
noPatient=len(hospital['patientid'])
noHospitals=len(hospital['Hospital_code'].unique())
noDepartments=len(hospital['Department'].unique())




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
                        
                    ])
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

    Admission_df=filtered_hospital.groupby('Type of Admission').count()
    pie_fig=px.pie(Admission_df,names=Admission_df.index,values='patientid',template='plotly_dark',labels={'patientid':'No of patients'},height=250,color_discrete_sequence=px.colors.sequential.RdBu,title='Type of Admission')
    pie_fig.update_layout(margin=dict(t=35, b=25, l=0, r=0))


    Severity_df=filtered_hospital.groupby('Severity of Illness').count()
    bar_fig=px.bar(Severity_df,x=Severity_df.index,y='patientid',height=200,template='plotly_dark',labels={'patientid':'No of patients'})
    return line_fig,DepartmentFig,pie_fig,bar_fig


if __name__ == '__main__':
    app.run_server(debug=True)
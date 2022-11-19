from dash import Dash, html, dcc, Input, Output,dash_table
import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy
from sklearn import preprocessing
import plotly.graph_objects as go
from collections import OrderedDict
import pickle



dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],use_pages=True)





"""___nav bar___"""
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="/"),className="navstyle"),
        dbc.NavItem(dbc.NavLink("Insights", href="/insights"),className="navstyle"),
        dbc.NavItem(dbc.NavLink("Classification",href="/classification"),className="navstyle")
           
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
                dash.page_container
                    
            ]
            ))
        ])






# print(hospital.head(10))



if __name__ == '__main__':
    
    app.run_server(debug=True)
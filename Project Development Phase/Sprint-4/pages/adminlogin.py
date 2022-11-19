from dash import  html, dcc, Input, Output,State
import dash
import dash_bootstrap_components as dbc

# from app import model
dash.register_page(__name__,path='/adminlogin')

layout=[html.Div(
    [
        html.H1("Admin Login"),
        html.Div([
            html.Center([
            html.Label("Enter Email: "),
            html.Br(),
            dcc.Input(id='email',type='email'),
            html.Br(),
            html.Label("Enter Password: "),
            html.Br(),
            dcc.Input(id='password',type='password'),
            html.Br(),
            html.Br(),
            dbc.Button("Login", color="info",n_clicks=0,id='admin_login'),
            html.Br(),
            html.P(id="loginout",style={'color':'white'})
            # html.Link(dbc.Button("Login", color="info",n_clicks=0,id='admin_login'),href='/admin',hidden=True)])
        ],className='boxed2')
    ]
)]
)]


@dash.callback(
    Output("loginout","children"),
    Input("admin_login","n_clicks"),
    State('email','value'),
    State('password','value')    
)

def update(n_clicks,email,password):
    if email=="admin@gmail.com" and password=="admin":
        return dcc.Link("Login!!",href="/admin")
    return "Enter the correct email and password"
    
       
        



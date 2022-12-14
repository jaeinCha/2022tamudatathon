from dash import Dash, dcc, html, Input, Output
from dash import html
import plotly.express as px
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np, json
import plotly.graph_objects as go
import urllib.request

dash_app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app = dash_app.server

with urllib.request.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv")
pred=pd.read_csv('model_output.csv').iloc[:,1:].rename(columns={'geoid':'fips'})
pred.value=np.int64(pred.value.to_numpy())
df_new=pd.merge(df,pred, on='fips')
temp_fips=[]
for i in range(len(df_new.fips)):
    if df_new.fips[i]<10000:
        temp_fips.append('0'+str(df_new.fips[i]))
    else:
        temp_fips.append(str(df_new.fips[i]))
df_new.fips=temp_fips
df_new=df_new[['fips','value']][df_new.value!=0]
df_new['value_log']=np.log10(df_new['value'])

df_dl=pd.read_csv('deep_learning.csv')
df_new_dl=pd.merge(df,df_dl, on='fips')
temp_fips_dl=[]
for i in range(len(df_new_dl.fips)):
    if df_new_dl.fips[i]<10000:
        temp_fips_dl.append('0'+str(df_new_dl.fips[i]))
    else:
        temp_fips_dl.append(str(df_new_dl.fips[i]))
df_new_dl.fips=temp_fips_dl
df_new_dl=df_new_dl[['fips','value']][df_new_dl.value!=0]
df_new_dl['value_log']=np.log10(df_new_dl['value'])


# app.config.external_stylesheets = [dbc.themes.LUX]
directed_edges=[
    {'data': {'id': 'A', 'label':'Per Capita Income','height':'100px', 'width':'180px'},
     'position':{'x':175, 'y':50}, 'classes':'ellipse1'},
    {'data': {'id': 'B', 'label':'Total Population','height':'100px', 'width':'180px'},
     'position':{'x':500, 'y':300}, 'classes':'ellipse1'},
    {'data': {'id': 'C', 'label':'Poverty','height':'100px', 'width':'180px'},
     'position':{'x':225, 'y':450}, 'classes':'ellipse1'},
    {'data': {'id': 'D', 'label':'Population Above the Age of 65','height':'100px', 'width':'180px'},
     'position':{'x':400, 'y':600}, 'classes':'ellipse1'},
    {'data': {'id': 'E', 'label':'Minority Population','height':'100px', 'width':'180px'},
     'position':{'x':600, 'y':500}, 'classes':'ellipse1'},
    {'data': {'id': 'F', 'label':'Number of Mobile Home','height':'100px', 'width':'180px'},
     'position':{'x':700, 'y':50}, 'classes':'ellipse1'},
    {'data': {'id': 'G', 'label':'Household with No Vehicle','height':'100px', 'width':'180px'},
     'position':{'x':1000, 'y':50}, 'classes':'ellipse1'},
    {'data': {'id': 'H', 'label':'Population Below the Age of 17','height':'100px', 'width':'180px'},
     'position':{'x':950, 'y':350}, 'classes':'ellipse1'},
    {'data': {'id': 'I', 'label':'Structure with more than 10 Units','height':'100px', 'width':'180px'},
     'position':{'x':1200, 'y':250}, 'classes':'ellipse1'},
    {'data': {'id': 'J', 'label':'Population with no High School Diploma','height':'100px', 'width':'180px'},
     'position':{'x':850, 'y':500}, 'classes':'ellipse1'},
    {'data': {'id': 'K', 'label':'Population who Speak English less than well','height':'100px', 'width':'180px'},
     'position':{'x':1300, 'y':500}, 'classes':'ellipse1'},
    {'data': {'id': 'L', 'label':'Number of Household','height':'100px', 'width':'180px'},
     'position':{'x':1100, 'y':725}, 'classes':'ellipse1'},
    {'data': {'id': 'M', 'label':'Household with more People than Rooms','height':'100px', 'width':'180px'},
     'position':{'x':1100, 'y':725}, 'classes':'ellipse1'},
    {'data': {'id': 'N', 'label':'Expected Number of COVID-19 Cases','height':'100px', 'width':'180px'},
     'position':{'x':1700, 'y':250}, 'classes':'hexagon1'},  
    {'data':{'id':'A_B', 'source':'A','target':'G'}},
    {'data':{'id':'A_C', 'source':'B','target':'D'}},
    {'data':{'id':'A_F', 'source':'B','target':'E'}},
    {'data':{'id':'A_I', 'source':'B','target':'H'}},
    {'data':{'id':'A_K', 'source':'C','target':'F'}},
    {'data':{'id':'A_M', 'source':'C','target':'I'}},
    {'data':{'id':'A_N', 'source':'C','target':'J'}},
    {'data':{'id':'B_F', 'source':'D','target':'N'}},
    {'data':{'id':'B_G', 'source':'E','target':'K'}},
    {'data':{'id':'B_I', 'source':'F','target':'L'}},
    {'data':{'id':'B_H', 'source':'G','target':'N'}},
    {'data':{'id':'B_J', 'source':'H','target':'M'}},
    {'data':{'id':'B_K', 'source':'I','target':'M'}},
    {'data':{'id':'B_M', 'source':'C','target':'J'}},
    {'data':{'id':'C_E', 'source':'J','target':'N'}},
    {'data':{'id':'C_G', 'source':'M','target':'N'}},
    {'data':{'id':'C_I', 'source':'L','target':'N'}},
    {'data':{'id':'C_H', 'source':'K','target':'N'}},
    ]
style=[{'selector':'node','style':{'label':'data(label)','text-halign':'center','text-valign':'center','width':'data(width)',
                                   'height':'data(height)','shape':'ellipse','font-size':'25', 
                                   'text-wrap':'wrap','text-max-width':'4'}},
       {'selector':'edge','style':{'curve-style':'bezier'}},
       {'selector':'.ellipse1','style':{'background-color':'#ACEFF0','shape':'ellipse'}},
       {'selector':'.ellipse2','style':{'background-color':'#6FC01A','shape':'ellipse'}},
       {'selector':'.ellipse3','style':{'background-color':'#CFA993','shape':'ellipse'}},
       {'selector':'.ellipse4','style':{'background-color':'#9A45A3','shape':'ellipse'}},
       {'selector':'.hexagon1','style':{'background-color':'#ECF477','shape':'ellipse'}}]
for i in range(len(directed_edges[14:])):
    name=directed_edges[14+i]['data']['id']
    style.append({'selector':f'#{name}','style':{'target-arrow-color':'#808080','target-arrow-shape':'triangle',
                                                 'line-color':'#808080'}})

# the style arguments for the sidebar.
SIDEBAR_STYLE = {'position': 'fixed','top': 0,'left': 0,'bottom': 0,'width': '20%','padding': '20px 10px',
                 'background-color': '#f8f9fa'}
CONTENT_STYLE = {'margin-left': '25%','margin-right': '5%','top': 0,'padding': '10px 10px'}
TEXT_STYLE = {'textAlign': 'center','color': '#191970'}
control=html.Div([html.P('Choose Evidence', style={'textAlign':'center'}),
                      dcc.Dropdown(
                          id='dropdown',
                          options=[
                              {'label':'Oyster Production in Campeche, MX','value':'1'},
                              {'label':'Oyster Production in Tamaulipas, MX','value':'2'},
                              {'label':'Oyster Production in Veracruz, MX','value':'3'},
                              {'label':'Oyster Production in Tabasco, MX','value':'4'},
                              {'label':'Oil Production in Gulf of Mexico, MX','value':'5'},
                              {'label':'Natural Gas Production in Gulf of Mexico, MX','value':'6'},
                              {'label':'Sea Level Rise from Tide Gauge Measured in Port Isabel, TX','value':'7'},
                              {'label': 'Oyster Production in Alabama, US', 'value': '8'},
                              {'label': 'Oyster Production in Florida, US', 'value': '9'},
                              {'label': 'Oyster Production in Louisiana, US', 'value': '10'},
                              {'label': 'Oyster Production in Mississippi, US', 'value': '11'},
                              {'label': 'Oyster Production in Texas, US', 'value': '12'},
                              {'label': 'Oil Production in Gulf of Mexico, US', 'value': '13'},
                              {'label': 'Average High Temperature in Louisiana, US', 'value': '14'},], 
                          value='1'
    )])
sidebar=html.Div([html.H2('Gulf of Mexico Risk Region',style=TEXT_STYLE),
                html.Hr(),control,html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br()],
               style=SIDEBAR_STYLE,)


def choro_fig_bn():
    fig = px.choropleth(df_new, geojson=counties, locations='fips', color='value_log',
                               color_continuous_scale="Plasma",
                               range_color=(0, round(max(df_new.value_log))),
                               scope="usa",
                               hover_data=df_new[['fips','value']],
                               labels={'value':'Expected Covid Cases'}
                              )

    fig.update_layout(coloraxis_colorbar=dict(
        title="Expected Covid 19 Cases",
        tickvals=[1,2,3,4,5,6,7],
        ticktext=["10","100","1000","10K","100k", "1M", "10M"],))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def choro_fig_dl():
    fig = px.choropleth(df_new_dl, geojson=counties, locations='fips', color='value_log',
                               color_continuous_scale="Plasma",
                               range_color=(0, round(max(df_new_dl.value_log))),
                               scope="usa",
                               hover_data=df_new[['fips','value']],
                               labels={'value':'Expected Covid Cases'}
                              )

    fig.update_layout(coloraxis_colorbar=dict(
        title="Predicted Covid 19 Cases",
        tickvals=[1,2,3,4,5,6,7],
        ticktext=["10","100","1000","10K","100k", "1M", "10M"],))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

bn_network=html.Div(cyto.Cytoscape(id='three_node',zoom=0.5,zoomingEnabled=False,layout={'name':'preset', 'fit':False},
                                   style={'width':'100%','height':'400px','align':'center'},elements=directed_edges,
                                   stylesheet=style))
graph=dcc.Graph(id='graph-with-slider', figure=choro_fig_bn())


content=html.Div([
    html.H2('COVID-19 TOTAL CASES MODEL BENCHMARK', style=TEXT_STYLE),
    html.Hr(),
    html.H4('Bayesian Network Model (Not Validated Yet)', style=TEXT_STYLE),
    bn_network,
    html.Hr(),
    html.H5('Expected Total COVID-19 Cases per County Predicted from Bayesian Network', style=TEXT_STYLE),
    html.Div(children=[dcc.Graph(id='choropleth_bn', figure=choro_fig_bn())]),
    html.Hr(),
    html.H5('Predicted Total COVID-19 Cases per County using Neural Network Regression Model', style=TEXT_STYLE),
    html.Div(children=[dcc.Graph(id='choropleth_dl', figure=choro_fig_dl())])])
# bins=20
app.layout = html.Div([sidebar,content])


# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     Input('dropdown', 'value'))
# def update_figure(selected_year):
#     if selected_year=='1':
#         fig = px.line(data_oys,x='period',y='campeche_oys',labels={"period": "Time","campeche_oys":"Oyster Production (kg)"},
#                          title='Annual Monthly Oyster Production in Campeche, MX')
#         return fig

if __name__ == '__main__':
    dash_app.run_server(debug=True)

from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
pd.set_option('display.max_columns',None)
import plotly.express as px
import pycountry as pc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors


app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server


##########   DATA   ##########
DATA = pd.read_csv('ds_salaries.csv')

DATA = DATA.drop(columns = ['salary','salary_currency'])
# probably yearly salary
# data sourced from aijobs.net.
DATA.rename(columns = {'work_year':'Work Year'}, inplace = True)
DATA.rename(columns = {'experience_level':'Experience Level'}, inplace = True)
DATA.rename(columns = {'employment_type':'Employment Type'}, inplace = True)
DATA.rename(columns = {'job_title':'Job Title'}, inplace = True)
DATA.rename(columns = {'salary':'Yearly Salary'}, inplace = True)
DATA.rename(columns = {'salary_currency':'Salary Currency'}, inplace = True)
DATA.rename(columns = {'salary_in_usd':'Salary (USD)'}, inplace = True)
DATA.rename(columns = {'employee_residence':'Employment Residence'}, inplace = True)
DATA.rename(columns = {'remote_ratio':'Remote Ratio'}, inplace = True)
DATA.rename(columns = {'company_location':'Company Location'}, inplace = True)
DATA.rename(columns = {'company_size':'Compani Size'}, inplace = True)


DATA['Experience Level'].replace(to_replace=['EN'], value='Entry Level', inplace=True)
DATA['Experience Level'].replace(to_replace=['MI'], value='Mid-Senior Level', inplace=True)
DATA['Experience Level'].replace(to_replace=['SE'], value='Senior Level', inplace=True)
DATA['Experience Level'].replace(to_replace=['EX'], value='Executive Level', inplace=True)

DATA['Employment Type'].replace(to_replace=['FT'], value='Full-time', inplace=True)
DATA['Employment Type'].replace(to_replace=['PT'], value='Part-Time', inplace=True)
DATA['Employment Type'].replace(to_replace=['CT'], value='Contractor', inplace=True)
DATA['Employment Type'].replace(to_replace=['FL'], value='Freelancer', inplace=True)

DATA['Job Title'].replace(to_replace=['ML Engineer'], value='Machine Learning Engineer', inplace=True)
DATA['Job Title'].replace(to_replace=['Machine Learning Research Engineer'], value='Machine Learning Researcher', inplace=True)
DATA['Job Title'].replace(to_replace=['Finance Data Analyst'], value='Financial Data Analyst', inplace=True)
DATA['Job Title'].replace(to_replace=['Data Science Tech Lead'], value='Data Science Lead', inplace=True)
DATA['Job Title'].replace(to_replace=['Lead Data Analyst'], value='Data Analytics Lead', inplace=True)
DATA['Job Title'].replace(to_replace=['Lead Data Scientist'], value='Data Science Lead', inplace=True)
DATA['Job Title'].replace(to_replace=['Data Scientist Lead'], value='Data Science Lead', inplace=True)

DATA['Job Title'].replace(to_replace=['BI Analyst'], value='BI Data Analyst', inplace=True)
DATA['Job Title'].replace(to_replace=['Business Data Analyst'], value='BI Data Analyst', inplace=True)
DATA['Job Title'].replace(to_replace=['Analytics Engineer'], value='Data Analytics Engineer', inplace=True)
DATA['Job Title'].replace(to_replace=['Cloud Data Architect'], value='Cloud Database Engineer', inplace=True)
DATA['Job Title'].replace(to_replace=['Cloud Data Engineer'], value='Cloud Database Engineer', inplace=True)

JOB_TITLES_DF = pd.DataFrame({'Job Title':DATA['Job Title'].value_counts().head(20).index,
                              'Count':DATA['Job Title'].value_counts().head(20).values})


##########   FIGURE 1   ##########
fig = px.bar(JOB_TITLES_DF, y="Count", x="Job Title", color="Count", color_continuous_scale='Teal')
                # width=900, height=700)

fig.update_layout(yaxis_title="Count (#)", yaxis={'categoryorder':'total ascending'}, width=1210, height=450,
                  title=dict(text='<b>Top 20 Most Popular Jobs</b>', x=0.51, y=1, font=dict( family="Arial", size=30) ),
                  title_font_color='#536872')


##########   FIGURE 2   ##########
TOP_SALARIES_DF =  DATA.groupby('Job Title').agg({'Salary (USD)':'mean'}).round(2).sort_values('Salary (USD)', ascending=False).head(20)
fig2 = px.bar(TOP_SALARIES_DF, y=TOP_SALARIES_DF['Salary (USD)'], x=TOP_SALARIES_DF.index, color='Salary (USD)',
                 width=1210, height=450, color_continuous_scale='Teal')

fig2.update_layout(yaxis={'categoryorder':'total ascending'},
                  title=dict(text='<b>Top 20 Highest-Paying Jobs</b>', x=0.51, y=1, font=dict( family="Arial", size=30) ),
                   title_font_color='#536872')


##########   FIGURE 3   ##########
fig3 = px.violin(DATA, y='Salary (USD)', x='Experience Level', box=True, width=600, height=400,
                category_orders={'Experience Level': ['Entry Level', 'Mid-Senior Level', 'Senior Level', 'Executive Level']},
                hover_data=DATA.columns)
fig3.update_traces(fillcolor = 'lightseagreen', marker=dict(color='black', line=dict(color='Black',  )),
                  line_color = 'black', opacity = 0.5 )
fig3.update_layout(title=dict(text='<b>Salaries by Experience Level</b>', x=0.51, y=0.99, font=dict( family="Arial", size=25) ),
                   title_font_color='#536872')


##########   FIGURE 4   ##########
fig4 = px.violin(DATA, y='Salary (USD)', x='Employment Type', box=True, width=600, height=400,
                category_orders={'Experience Level': ['Entry Level', 'Mid-Senior Level', 'Senior Level', 'Executive Level']},
                hover_data=DATA.columns)

fig4.update_traces(fillcolor = 'lightseagreen', marker=dict(color='black', line=dict(color='Black')),
                  line_color = 'black', opacity = 0.5  )
fig4.update_layout(title=dict(text='<b>Salaries by Employment Type</b>', x=0.51, y=0.99, font=dict( family="Arial", size=25) ),
                   title_font_color='#536872')


##########   FIGURE 5   ##########
DATA['Remote Ratio'].replace(to_replace=0, value='On Site', inplace=True)
DATA['Remote Ratio'].replace(to_replace=50, value='Hybrid', inplace=True)
DATA['Remote Ratio'].replace(to_replace=100, value='Remote', inplace=True)

Remote_Count = DATA['Remote Ratio'].value_counts()

REMOTE_DF = pd.DataFrame({'Remote Ratio': Remote_Count.index, 'Count': Remote_Count.values}).copy()

Colors = [px.colors.qualitative.Vivid[7], px.colors.qualitative.D3[9], px.colors.qualitative.Safe[0]]

fig5 = px.pie(REMOTE_DF, values='Count', names='Remote Ratio', title='Remote Ratio Distribution',
             color_discrete_sequence=Colors,  height=400, hole=0.4)

fig5.update_traces(marker=dict(line=dict(color=px.colors.qualitative.Dark24[19], width=0.5)),
                  texttemplate='<b>%{percent:.1%}</b></span>', textfont=dict(size=15, color='black'),
                  )
fig5.update_layout(legend=dict(title_font_family="Times New Roman",
                              font=dict(size=14), entrywidth=60, orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=1.2),
                  title=dict(text='<b>Work Mode Distribution</b>', x=0.51, y=0.99, font=dict(family="Arial", size=25)),
                   title_font_color='#536872')


##########   FIGURE 6   ##########
A3COUNTRIES = []
for country_alpha_2 in DATA['Employment Residence']:
    country_alpha_2 = pc.countries.get(alpha_2=country_alpha_2)
    if country_alpha_2:
        alpha3_code = country_alpha_2.alpha_3
        A3COUNTRIES.append(alpha3_code)
    else:
        print("Invalid alpha-3 country code")

DATA['Country of Residence'] = A3COUNTRIES

fig6 = px.choropleth(DATA, locations="Country of Residence", width=800,# height=600,
                    color="Salary (USD)", # lifeExp is a column of gapminder
                    hover_name="Country of Residence", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Teal)

fig6.update_layout(title=dict(text='<b>Geographical Distribution</b>', x=0.51, y=0.99, font=dict( family="Arial", size=25) ),
                   title_font_color='#536872')













##########   Customize Layout   ##########
# app.layout = dbc.Container([mytext])

app.layout = html.Div(
    style={'margin-top': '30px', 'marginLeft' : '30px'},
    children=[
        dbc.Row(
            dbc.Col(html.H1("Data Science Jobs & Salaries Overview"), width={'size':8, 'offset':2})
        ),
        html.Br(),
        html.Div(
            dbc.Col(
                html.Div(
                    [
                        "A brief overview of data science job distributions, popularity and salaries. The data was extracted from ai-jobs.net.",
                        #dbc.Button("Hello", color="success", className="mr-1"),
                     ]
                ), width={'size':8, 'offset':2}
            )
        ),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                #dcc.Graph(id='example-graph-5', figure=fig5)
                dcc.Graph(id='output_plot'),
                dcc.Dropdown(
                    options=[{'label':x, 'value':x} for x in DATA['Experience Level'].unique()]+
                            [{'label': 'Select all', 'value': 'all_values'}],
                    value='all_values',
                    # multi=True,
                    searchable=True,
                    # search_value='',
                    clearable=True,
                    placeholder='Please select...',
                    style={'width':'70%', 'marginLeft' : '50px'},
                    persistence='string',
                    persistence_type='session',
                    id='dropdown'
                )
            ], xs=12, sm=12, md=12, lg=4, xl=4 #width={'size': 4, 'offset': 0}
            ),
            dbc.Col([
                dcc.Graph(id='example-graph-6', figure=fig6)
            ], xs=12, sm=12, md=12, lg=8, xl=8 #width={'size': 8, 'offset': 0}
            ),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='example-graph-3', figure=fig3)# width={'size':6}),
            ], xs=12, sm=12, md=12, lg=6, xl=6 #width={'size':6, 'offset':0}
            ),
            dbc.Col([
                dcc.Graph(id='example-graph-4', figure=fig4)  # , width={'size':6}),
            ], xs=12, sm=12, md=12, lg=6, xl=6 #width={'size': 6, 'offset': 0} #style={'width': '49%', 'display': 'inline-block'}
            ),
        ]),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='example-graph-1', figure=fig), xs=12, sm=12, md=12, lg=12, xl=12 #{'size':12, 'offset':"70px"}
            )
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='example-graph-2', figure=fig2),xs=12, sm=12, md=12, lg=12, xl=12 #{'size':12, 'offset':"70px"}
            )
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            dbc.Col(
                html.Div(
                    "José Ricardo Torres Heredia"
                ), style={'margin-top': '0px', 'marginLeft' : '475px'},
            )
        ),
        html.Br(),
        html.Div(
            dbc.Col(
                html.Div(
                    [
                        dmc.Group(
                            [
                                html.A(DashIconify(icon="ion:logo-linkedin", width=25), href="https://www.linkedin.com/in/josé-ricardo-torres-heredia-740849238/"),
                                html.A(DashIconify(icon="cib:kaggle", width=25), href="https://www.kaggle.com/ricardotorresheredia"),
                                html.A(DashIconify(icon="ion:logo-github", width=25), href="https://github.com/JRicardoTH"),
                            ],
                        )
                    ]
                ), style={'margin-top': '0px', 'marginLeft' : '520px'},
            )
        ),
        html.Br(),
    ]
)

##########   App Callback   ##########
@app.callback(
    Output('output_plot','figure'),
    Input('dropdown','value')
)

def build_graph(drop_down_option):
    Colors = [px.colors.qualitative.Vivid[7], px.colors.qualitative.D3[9], px.colors.qualitative.Safe[0]]

    if drop_down_option in ['all_values']:
        DATA_F = DATA
        Remote_Count = DATA_F['Remote Ratio'].value_counts()
    else:
        DATA_F = DATA[DATA['Experience Level'] == drop_down_option]
        Remote_Count = DATA_F['Remote Ratio'].value_counts()

    REMOTE_DF = pd.DataFrame({'Remote Ratio': Remote_Count.index, 'Count': Remote_Count.values}).copy()

    figOut = px.pie(REMOTE_DF, values='Count', names='Remote Ratio', title='Remote Ratio Distribution',
                  color_discrete_sequence=Colors, height=400, hole=0.4)

    figOut.update_traces(marker=dict(line=dict(color=px.colors.qualitative.Dark24[19], width=0.5)),
                       texttemplate='<b>%{percent:.1%}</b></span>', textfont=dict(size=15, color='black'),
                       )
    figOut.update_layout(legend=dict(title_font_family="Times New Roman",
                                   font=dict(size=14), entrywidth=60, orientation="h", yanchor="bottom", y=1.06,
                                   xanchor="right", x=1.2),
                       title=dict(text='<b>Work Mode Distribution</b>', x=0.51, y=0.99,
                                  font=dict(family="Arial", size=25)), title_font_color='#536872')

    return figOut          # return objects are assigned to the component property of the Output


##########   Run App   ##########
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

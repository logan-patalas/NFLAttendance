import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


#import file
file="NFLAttendanceData2015thru2022no2020.csv"
NFL_Attendance=pd.read_csv(file)
NFL_Attendance



team_name=list(NFL_Attendance['Team'].unique())
year_attendance=list(NFL_Attendance['Year'].unique())
team_attendance= [
    'Total',
    'Home',
    'Away',
]


nfl_reshaped = NFL_Attendance.melt(id_vars=['Team', 'Year'], value_vars=['Total', 'Home', 'Away'], var_name='Stat', value_name='Attendance')

nfl_reshaped['Attendance'] = nfl_reshaped['Attendance'].str.replace(',', '')
nfl_reshaped['Attendance'] = nfl_reshaped['Attendance'].astype(int)

app= Dash(__name__,external_stylesheets=[dbc.themes.SANDSTONE])

server = app.server

app.layout = dbc.Container(
        children=[
    
            html.H1('NFL Attendance Totals from 2015-2022, excluding 2020', className = 'mr-3,mt-6,ml-3'),

        dbc.Row([
            dbc.Col(
                width=6,
                children=[
                    html.H3('NFL single year chart', className='text-center text-primary mt-3 mb-3 m-4'),
                    dcc.Graph(
                        id='attendance_chart',
                        className= 'mt-4',
                    ),
                    dcc.Graph(
                        id='year_by_year_attendance',
                        className= 'mt-4',
                    ),
                ],
           ),
        ],
        ),            
        dbc.Row(
            dbc.Col(
                width=dict(size=4,offset=1),
                children=[
                    dcc.Dropdown(
                        id='team_name_dropdown',
                        multi=False,
                        options=[{'label' : team_name, 'value' : team_name} for team_name in team_name],
                        placeholder='Team Name',
                        value=[],
                        optionHeight=12

                    ),
                    dcc.RadioItems(
                        id='year_radio',
                        options=[
                            dict(label=2015, value=2015),
                            dict(label=2016, value=2016),
                            dict(label=2017, value=2017),
                            dict(label=2018, value=2018),
                            dict(label=2019, value=2019),
                            dict(label=2021, value=2021),
                            dict(label=2022, value=2022),
                        ],
                        value= 2015,
                    ),
                    dbc.Checklist(
                        id='stats_checklist',
                        options=[
                            dict(label='Total', value='Total'),
                            dict(label='Home', value='Home'),
                            dict(label='Away', value='Away'),
                        ],
                        value=['Total'],
                    ),
                ],
            ),
        ),
        dbc.Row(
            dbc.Col(
                width=dict(size=4, offset=1),
                children=[
                    dcc.Dropdown(
                        id='multi_team_name_dd',
                        multi=True,
                        options=[{'label' : team_name, 'value' : team_name} for team_name in team_name],
                        placeholder='Team Name',
                        value=['Arizona Cardinals'],
                        optionHeight=16
                    ),
                    dcc.RadioItems(
                        id='stats_item',
                        options=[
                            dict(label='Total', value='Total'),
                            dict(label='Home', value='Home'),
                            dict(label='Away', value='Away'),
                        ],
                    value='Total',
                    ),
                    html.Div(
                        children=[
                            'Data Source:',
                            html.A('NFL Attendance Data', href='https://www.pro-football-reference.com')
                        ]
                    ),
                ],
            ),
        ),
    ],
    fluid=True,
)


# callbacks

@app.callback(
    Output('attendance_chart', 'figure'),
    Input('team_name_dropdown', 'value'),
    Input('stats_checklist', 'value'),
    Input('year_radio', 'value'),
)
def update_attendance_chart(team_select, stats_select, year_select):

    if len(team_select) == 0:
        team_select = 'Minnesota Vikings'

    if len(stats_select)== 0:
        stats_select = ['Home']

    subset_filter = (nfl_reshaped['Year'] == year_select) & (nfl_reshaped['Team'] == team_select ) & (nfl_reshaped['Stat'].isin(stats_select))
    subset_data = nfl_reshaped[subset_filter].copy()

    attendance_figure = px.bar(
        subset_data,
        x='Stat',
        y='Attendance',
        orientation='v',
    )

    return attendance_figure

@app.callback(
    Output('year_by_year_attendance', 'figure'),
    Input('multi_team_name_dd', 'value'),
    Input('stats_item', 'value'),
)
def update_year_by_year_chart(multi_team_select, single_stat_select):
    if len(multi_team_select) == 0:
        multi_team_select = ['Arizona Cardinals']


    subset2_NFLAttendance_Data = NFL_Attendance[NFL_Attendance['Team'].isin(multi_team_select)][['Year','Team', single_stat_select]].copy()    

    year_by_year_figure = px.line(
        subset2_NFLAttendance_Data,
        x='Year',
        y=single_stat_select,
        color='Team'
    )

    return year_by_year_figure

if __name__ == '__main__':
    app.run_server(debug=True)

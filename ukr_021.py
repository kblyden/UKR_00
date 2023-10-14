# 9/25/2023.  First project for Github
# 9/17/2023  Adding graphs from all pages of the excel file.
# disabled the dropdown, using clickData for the callback
# 10/13/2023.
# v01: Creating more tabs SubTabAnalysis and SubTabData.  Each with tabs to click.
# I hope after I complete the tabs and graphs, I'll Convert to Page and tabs on the right.
# v02: update Region PIN
from dash import Dash, html, dcc, dash_table, Input, Output  # , Input, Output
# from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json
import os

pathNm = '/Users/kelvinb/Documents/Skills/PYTHON/Udemy/Plotly/UKR_00/Ukraine HNO Data/'
ukrG2 = json.load(open('UA_FULL_Ukraine.geojson', 'r'))
dfOP = pd.read_excel('ukraine-2023-hno-pin-and-severity-for-hdx-20230215.xlsx',
                     sheet_name='obl_pop',
                     header=0)
Oblast = list(dfOP['Oblast'])

map_fig1 = px.choropleth(dfOP, locations='Oblast PCode',
                       geojson=ukrG2, featureidkey='properties.iso3166-2',
                       #zoom=9,
                       color_continuous_scale='Inferno',
                       hover_name='Oblast',
                       color='Population Estimate ',
                       scope='europe')

map_fig2 = px.choropleth_mapbox(dfOP, locations='Oblast PCode',
                       geojson=ukrG2, featureidkey='properties.iso3166-2',
                       color_continuous_scale='Inferno',
                       color='Population Estimate ',
                       hover_name='Oblast',
                       mapbox_style='carto-positron',
                       zoom=3,
                       center={'lat': 48.37, 'lon':31.16})

# 'Population Group PIN By Cluster'
column_data_types = {'A': str, 'B': int, 'C': int, 'D': int, 'E': int}
dfPIN = pd.read_excel('ukraine-2023-hno-pin-and-severity-for-hdx-20230215.xlsx',
                     sheet_name='Population Group PIN By Cluster',
                     #header=0, #index_col=0,
                     dtype=column_data_types,
                     names=['cluster', 'Internally Displaced People', 'Non-Displaced People', 'Returnees',
                             'Overall People in Need'],
                     skiprows=range(1, 5), usecols='A:E', nrows=13)

pd.options.display.float_format = '{:,.0f}'.format

data = {'cat':[dfPIN.columns[1], dfPIN.columns[2], dfPIN.columns[3]],
        'total': [dfPIN[dfPIN.columns[1]].sum(), dfPIN[dfPIN.columns[2]].sum(), dfPIN[dfPIN.columns[3]].sum()]}

dfPINsum = pd.DataFrame(data)

p_fig = px.pie(dfPINsum, names='cat', values='total',
               # hole=0.5,
               title='All Categories',
               height=750,
               color_discrete_sequence=px.colors.sequential.RdBu)
p_fig.update_layout(legend=dict(
                        orientation="h",
                        font=dict(size=9), yanchor="bottom", xanchor="left",
                        itemsizing='trace'))


app = Dash(external_stylesheets=[dbc.themes.MINTY])

ein = dbc.Row([
            dbc.Col(  # 1, 6 wide
                dbc.Card([
                    html.H4('Ukraine'),  # ,
                    # html.H5(f'{round(avg_age, 1)} years')
                    dcc.Graph(id='map-graph', figure=map_fig1)
                    ],
                    body=True,
                    style={'textAlign': 'center', 'color': 'white',  "box-shadow": "1px 2px 7px 0px grey"}
                    # color='red',
                    # className='mr-1'  #margin
                    # className='shadow-lg'
                ),
                className='col-6'
            ),
            dbc.Col([  # 2, 2 wide
                dbc.Row(
                    dbc.CardGroup([
                        dbc.Card(

                            dbc.CardBody([
                                html.H4('Ukraine General Data', className="card-title"),
                                html.H6('Population Number', className="card-text"),
                                html.H6('Land Area', className="card-text"),
                                html.H6('Number of Oblasts', className="card-text")
                            ]), className='m-1'
                        ),
                        dbc.Card(
                            dbc.CardBody([
                                html.H4('HNO Data', className="card-title"),
                                html.H6('PIN Population Number'),
                                html.H6('Pct of Total in country'),
                                html.H6('Pct of Total out of country')
                            ]), className='m-1'
                        ),
                        dbc.Card(
                            dbc.CardBody([
                                html.H4('Ukraine HNO Vectors', className="card-title"),
                                html.H6('Locations'),
                                html.H6('SADD'),
                                html.H6('Needs')
                            ]), className='m-1'
                        )
                    ]),  # card GROUP
                    # className='m-2 mr-2'
                ),
                #  # Row for cards
                dbc.Row(
                    dbc.CardGroup([
                        dbc.Card(  #1
                            dbc.Button(Oblast[0], style={"font-size": "8px"})
                        ),
                        dbc.Card(  #2
                            dbc.Button(Oblast[1][:2])
                        ),
                        dbc.Card(  #3
                            dbc.Button(Oblast[2][:2])
                        ),
                        dbc.Card(  #4
                            dbc.Button(Oblast[3][:2])
                        ),
                        dbc.Card(  #5
                            dbc.Button(Oblast[4][:2])
                        ),
                        dbc.Card(  #6
                            dbc.Button(Oblast[5][:2])
                        )
                    ]),  # card group
                    className='m-1'
                ),  # row for card group
                dbc.Row(
                    dbc.CardGroup([
                        dbc.Card(  # 1
                            dbc.Button(Oblast[6][:2])
                        ),
                        dbc.Card(  # 2
                            dbc.Button(Oblast[7][:2])
                        ),
                        dbc.Card(  # 3
                            dbc.Button(Oblast[8][:2])
                        ),
                        dbc.Card(  # 4
                            dbc.Button(Oblast[9][:2])
                        ),
                        dbc.Card(  # 5
                            dbc.Button(Oblast[10][:2])
                        ),
                        dbc.Card(  # 6
                            dbc.Button(Oblast[11][:2])
                        )
                    ]),  # card group
                    className='m-1'
                ),  # row for card group
                dbc.Row(
                    dbc.CardGroup([
                        dbc.Card(  # 1
                            dbc.Button(Oblast[12][:2])
                        ),
                        dbc.Card(  # 2
                            dbc.Button(Oblast[13][:2])
                        ),
                        dbc.Card(  # 3
                            dbc.Button(Oblast[14][:2])
                        ),
                        dbc.Card(  # 4
                            dbc.Button(Oblast[15][:2])
                        ),
                        dbc.Card(  # 5
                            dbc.Button(Oblast[16][:2])
                        ),
                        dbc.Card(  # 6
                            dbc.Button(Oblast[17][:2])
                        )
                    ]),  # card group
                    className='m-1'
                ),  # row for card group
                dbc.Row(
                    dbc.CardGroup([
                        dbc.Card(  # 1
                            dbc.Button(Oblast[18][:2])
                        ),
                        dbc.Card(  # 2
                            dbc.Button(Oblast[19][:2])
                        ),
                        dbc.Card(  # 3
                            dbc.Button(Oblast[20][:2])
                        ),
                        dbc.Card(  # 4
                            dbc.Button(Oblast[21][:2])
                        ),
                        dbc.Card(  # 5
                            dbc.Button(Oblast[22][:2])
                        ),
                        dbc.Card(  # 6
                            dbc.Button(Oblast[23][:2])
                        )
                    ]),  # card group
                    className='m-1'
                )  # row for card group
            ])  # Col graph and boxes
      ])  # Row ein

zwei = dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H4('Ukraine with other country names'),  # ,
                    # html.H5(f'{round(avg_age, 1)} years')
                    dcc.Graph(id='map-graph2', figure=map_fig2)
                    ],
                    body=True,
                    style={'textAlign': 'center', 'color': 'white',  "box-shadow": "1px 2px 7px 0px grey"}
                    # color='red',
                    # className='mr-1'  #margin
                    # className='shadow-lg'
                ),
                className='col-6'
            ),
            dbc.Col(
                dbc.Card([
                    html.H4('Ukraine Pop Data'),
                    dash_table.DataTable(data=dfOP.to_dict('records'),
                                         style_table={'overflowX': 'auto'})
                ],
                    body=True,
                    style={'textAlign': 'center', "box-shadow": "1px 2px 7px 0px grey"}  # ,
                ),
                className='col-5'
            )
])

drei = dbc.Row([
            dbc.Col(dcc.Graph(figure=p_fig, id='donut_1'), className='col-6'),
            dbc.Col(dcc.Graph(id='donut_2'), className='col-6'),
            dbc.Col(dcc.Graph(id='bar_pin_cat'))  #, className='col-4')
            ])

subTabData = dbc.Tabs(
    id='subTabD',
    # vertical=True,
    children=[
    dbc.Tab(label='Region PIN', tab_id='geoT', children=ein),
    dbc.Tab(label='PIN Counntrywide', tab_id='geoM', children=zwei),
    dbc.Tab(label='Combined Data', tab_id='pinT', children=drei)
    ])

subTabAnalysis = dbc.Tabs(
    id='subTabA',
    # vertical=True,
    children=[
    dbc.Tab(label='Patterns', tab_id='patterns'),
    dbc.Tab(label='Questions and Analysis 1', tab_id='an1'),
    dbc.Tab(label='Questions and Analysis 2', tab_id='an2')
    ])

app.layout = dbc.Container([
    html.H1('Ukraine Humanitarian Needs Overview HDX Data'),
    dbc.Tabs(
        [
            dbc.Tab(label="Ukraine Data Observations", tab_id="ein", children=subTabData),
            dbc.Tab(label="Observation Analysis", tab_id="zwei", children=subTabAnalysis),
            dbc.Tab(label="Analysis Summary", tab_id="three")
        ],
        id="tabs"
    )
])

@app.callback(
    Output('donut_2', 'figure'),
    Output('bar_pin_cat', 'figure'),
    Input('donut_1', 'clickData'))

def update_graph(clicked):
    # print(clicked)
    if clicked is None:
        fig = px.pie(dfPIN, names='cluster',
                     values=dfPINsum['cat'][0],
                     title=dfPINsum['cat'][0],
                     height=750,
                     hole=0.5,
                     color_discrete_sequence = px.colors.sequential.RdBu)
        fig.update_layout(
            legend=dict(
                orientation="h",
                font=dict(size=9), yanchor="bottom", xanchor="left", itemsizing='constant')  #,  # Set the orientation to horizontal
        )

        barfig = px.bar(dfPIN.sort_values('Overall People in Need'), x='cluster',
               y=[ 'Internally Displaced People', 'Non-Displaced People', 'Returnees' ],
               barmode='stack',
               title='All Categories')
        barfig.update_layout(
            legend=dict(
                orientation="h",  # Set the orientation to horizontal
                yanchor="bottom",
                y=1.02,  # Adjust the Y-coordinate for the legend's position
                xanchor="left",
                x=0,
            )
        )
    else:
        labl = clicked['points'][0]['label']
        fig = px.pie(dfPIN, names='cluster',
                     values=labl,
                     title=labl,
                     hole=0.5,
                     height=750,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(
            legend=dict(
                orientation="h",
                font=dict(size=9), yanchor="bottom", xanchor="left", itemsizing='constant') #,  # Set the orientation to horizontal
            )
        barfig = px.bar(dfPIN.sort_values('Overall People in Need'),
               x='cluster',
               y=labl,
               title=labl)
    return fig, barfig

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

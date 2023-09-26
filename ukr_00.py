# 9/25/2023.  First project for Github
# 9/17/2023  Adding graphs from all pages of the excel file.
# disabled the dropdown, using clickData for the callback
from dash import Dash, html, dcc, dash_table  # , Input, Output
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json

ukrG2 = json.load(open('UA_FULL_Ukraine.geojson', 'r'))
dfOP = pd.read_excel('ukraine-2023-hno-pin-and-severity-for-hdx-20230215.xlsx',
                     sheet_name='obl_pop',
                     header=0)

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
            dbc.Col(
                dbc.Card([
                    html.H4('2nd Card'),  # ,
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
            dbc.Col(
                dbc.Card([
                    html.H4('Ukraine Pop Data'),
                    dash_table.DataTable(data=dfOP.to_dict('records'),
                                         style_table={'overflowX': 'auto'})
                    #, 'maxWidth': '800px'},)
                    # ,
                    # html.H5(f'{round(avg_age, 1)} years')
                ],
                    body=True,
                    style={'textAlign': 'center', "box-shadow": "1px 2px 7px 0px grey"}  #,
                    # color='red',
                    # className='mr-1'  # margin
                    # className='shadow-lg'
                ),
                className='col-5'
            )

])

zwei = dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H4('Ukrainw with other country names'),  # ,
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

app.layout = dbc.Container([
    html.H1('Ukraine Template Dashboard With Tabs'),
    dbc.Tabs(
        [
            dbc.Tab(label="Tab Ein", tab_id="ein", children=ein),
            dbc.Tab(label="Tab Zwei", tab_id="zwei", children=zwei),
            dbc.Tab(label="Tab Drei", tab_id="drei", children=drei)
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

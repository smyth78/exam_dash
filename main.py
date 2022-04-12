# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.express as px
from dash import no_update
import dash._callback_context as cb_ctx

from server import app, server
from useful_functions import *




navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('rchk_logo.png'), height="40px"), width=3),
                    dbc.Col(dbc.NavbarBrand("RCHK Data Study"), width=9),
                ],
                align="center",

            ),

        ]
    ),
    color="dark",
    dark=True,
)
app.layout = html.Div(
    [
        navbar,
        dcc.Location(id='base-url', refresh=True),
        dbc.Container([
                html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div(
                                [
                                    dbc.Label("Group 1"),
                                    dbc.Checklist(
                                        options=[],
                                        value=[],
                                        id={'type': 'sub-choice', 'index': 0},
                                        inline=True,
                                    ),
                                ]
            )
            ], width=2),
                dbc.Col([
                    html.Div(
                        [
                            dbc.Label("Group 2"),
                            dbc.Checklist(
                                options=[],
                                value=[],
                                id={'type': 'sub-choice', 'index': 1},
                                inline=True,
                            ),
                        ]
                    )
                ], width=2),
                dbc.Col([
                    html.Div(
                        [
                            dbc.Label("Group 3"),
                            dbc.Checklist(
                                options=[],
                                value=[],
                                id={'type': 'sub-choice', 'index': 2},
                                inline=True,
                            ),
                        ]
                    )
                ], width=2),
                dbc.Col([
                    html.Div(
                        [
                            dbc.Label("Group 4"),
                            dbc.Checklist(
                                options=[],
                                value=[],
                                id={'type': 'sub-choice', 'index': 3},
                                inline=True,
                            ),
                        ]
                    )
                ], width=2),
                dbc.Col([
                    html.Div(
                        [
                            dbc.Label("Group 5"),
                            dbc.Checklist(
                                options=[],
                                value=[],
                                id={'type': 'sub-choice', 'index': 4},
                                inline=True,
                            ),
                        ]
                    )
                ], width=2),
                dbc.Col([
                    html.Div(
                        [
                            dbc.Label("Group 6"),
                            dbc.Checklist(
                                options=[],
                                value=[],
                                id={'type': 'sub-choice', 'index': 5},
                                inline=True,
                            ),
                        ]
                    )
                ], width=2),
            ], style={'margin-bottom': ROW_MARGIN}),
            dbc.Row(dbc.Col([
                html.Div(
                    [
                        dbc.Label("Components"),
                        dbc.Checklist(
                            options=[{"label": 'OG', "value": 'OG'}],
                            value=['OG'],
                            id='comp-choice',
                            inline=True,
                        ),
                    ]
                )
            ]), style={'margin-bottom': ROW_MARGIN}),
            dbc.Row(dbc.Col([
                html.Div(
                    [
                        dbc.Label("Level"),
                        dbc.Checklist(
                            options=[{"label": 'HL', "value": 'HL'},
                                     {"label": 'SL', "value": 'SL'}],
                            value=['HL'],
                            id='level-choice',
                            inline=True,
                        ),
                    ]
                )
            ]), style={'margin-bottom': ROW_MARGIN}),
            dbc.Row(dbc.Col([
                html.Div(
                    [
                        dbc.Label("Aggregation type"),
                        dbc.RadioItems(
                            options=[
                                {"label": "Mean", "value": 'mean'},
                                {"label": "Number", "value": 'count'},
                            ],
                            value='mean',
                            id='agg-choice',
                            inline=True,
                        ),
                    ]
                )

            ]), style={'margin-bottom': ROW_MARGIN}),
                    dbc.Row(dbc.Col(html.Div(id='alert')), style={'margin-bottom': ROW_MARGIN}),
                    dbc.Row(dbc.Col(dcc.Graph(id='main-chart')), style={'margin-bottom': ROW_MARGIN}),
                    dbc.Row(id='table-row'),
                    dbc.Row(style={'margin-bottom': BOTTOM_MARGIN})
        ])
        ]),
    ]
)

# this callback is when choices are made using the checkboxes
@app.callback(
    [Output('main-chart', 'figure'),
     Output('alert', 'children'),
     Output('table-row', 'children')],
    [Input({'type': 'sub-choice', 'index': ALL}, 'value'),
     Input('comp-choice', 'value'),
     Input('level-choice', 'value'),
     Input('agg-choice', 'value')]
)
def choices_made(sub_choices, comp_choice, level_choice, agg_choice):
    ctx = cb_ctx
    df = DFORIGINAL
    concat_subs = [n for sublist in sub_choices for n in sublist if n != []]
    is_valid_choices, alert = check_valid_choices(concat_subs, comp_choice, level_choice)

    df_prep = prep_dataframe_for_graph(df, concat_subs, comp_choice, level_choice) if \
        is_valid_choices else no_update
    is_mean = True if 'mean' in agg_choice else False
    figure, alert = make_graph(df_prep, is_mean, is_valid_choices, alert)
    table_row = make_table_div(df_prep, is_valid_choices, is_mean)
    return figure, alert, table_row


# this callback setup the initial option boxes
@app.callback(
    [Output({'type': 'sub-choice', 'index': ALL}, 'options'),
     Output('comp-choice', 'options')],
    [Input({'type': 'sub-choice', 'index': ALL}, 'value')]
)
def initial_setup(sub_choices):
    ctx = cb_ctx
    df = DFORIGINAL
    concat_subs = [n for sublist in sub_choices for n in sublist if n != []]
    subject_options = get_subjects_by_group(df)
    if concat_subs:
        # dynaically create the comp choices based on subject choice
        comp_list = df[df['Subject'].isin(concat_subs)]['Comp'].unique()
        component_options = make_option_dict(comp_list)
    else:
        component_options = [{"label": 'OG', "value": 'OG'}]
    return subject_options, component_options


if __name__ == '__main__':
    app.run_server(debug=True)





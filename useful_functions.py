import plotly.express as px
from dash import no_update
import dash_table

from constants import *
from alerts import *


def check_valid_choices(sub, comp, level):
    is_valid = True
    alert = no_update
    if not sub:
        is_valid = False
        alert = select_sub
    elif comp and level:
        if not comp:
            is_valid = False
            alert = select_comp
        elif not level:
            is_valid = False
            alert = select_level
    return is_valid, alert


def get_subjects_by_group(df):
    group_names = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5', 'Group 6']
    list_of_options_list = []
    for name in group_names:
        df_grouped = df.loc[df['Group'] == name]
        # reverse order of rows (to get more recent options first
        df_grouped = df_grouped.iloc[::-1]
        group_subjects = []
        for subject in df_grouped['Subject'].unique():
            group_subjects.append(subject)
        list_of_options_list.append(make_option_dict(group_subjects))
    return list_of_options_list


def make_option_dict(values):
    return [{"label": i, "value": i} for i in values]


def make_table_div(df, is_valid, is_mean):
    # make a table for each component...
    row = []
    if is_valid:
        for comp in df['Sub'].unique():
            df_filtered = df[df['Sub'] == comp]
            cols, data = make_table(df_filtered, is_mean)
            table = dash_table.DataTable(
                style_cell={
                    'height': 'auto',
                    # all three widths are needed
                    'minWidth': '10px', 'width': '20px', 'maxWidth': '30px',
                    'whiteSpace': 'normal'
                },
                id='table',
                columns=cols,
                data=data,
                export_format="csv",
            )
            row.append(dbc.Col(table, width=3, style={'padding': PAD_TABLE}))
    return row


def make_table(df_filtered, is_mean):
    agg = 'Grade' if is_mean else 'Count'
    df = df_filtered[['Sub', 'Year', agg]]
    data = df.to_dict('records'),
    columns = [{"name": i, "id": i} for i in df.columns]
    # HACK unsure why....
    data = data[0]
    mean = df[agg].mean(axis=0).round(1)
    data.append({'Sub': 'Mean', 'Year': '/', agg: mean})
    return columns, data

# NEED TO SEND MESSAGE WHEN SUBECT HAS ONLY 1 ENTRY (KOREAN)
def make_graph(df_prep, is_mean, is_valid, alert):
    fig = {}
    if is_valid:
        try:
            y = 'Grade' if is_mean else 'Count'
            fig = px.line(df_prep, x='Year', y=y, color='Sub', markers=True)
            fig.update_layout(template='simple_white', legend_title="Subjects", title="Component grades",
                              xaxis_range=[2012, 2019])
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)
        except KeyError:
            print('No sub key....try again...')
    return fig, alert


def prep_dataframe_for_graph(df, subjects, components, levels):
    # choose rows based on SLC
    df = df[df['Subject'].isin(subjects)]
    df = df[df['Comp'].isin(components)]
    df = df[df['Level'].isin(levels)]

    # now combine the first 3 cols into the name of sub
    df['Sub'] = df['Subject'] + ' ' + df['Level'] + ' ' + df['Comp']
    return df



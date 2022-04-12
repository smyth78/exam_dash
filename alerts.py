import dash_bootstrap_components as dbc
import dash_html_components as html

alert_duration = 3000

empty_df = dbc.Alert(
    html.H5("The chosen combination has no results..."),
    color='warning',
    fade=True,
    duration=alert_duration
)

select_sub = dbc.Alert(
    html.H5("You must choose at least one subject..."),
    color='warning',
    fade=True,
    duration=alert_duration
)

select_comp = dbc.Alert(
    html.H5("You must choose at least one component..."),
    color='warning',
    fade=True,
    duration=alert_duration
)

select_level = dbc.Alert(
    html.H5("You must choose at least one level..."),
    color='warning',
    fade=True,
    duration=alert_duration
)
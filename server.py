import dash
import dash_bootstrap_components as dbc



app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
)

app.config.suppress_callback_exceptions = True
app.title = 'data_study'

server = app.server


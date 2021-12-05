"""
LegTextScraper Plotly Dash Dashboard
"""
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import base64

app = dash.Dash(__name__,
                external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css",
                                      {'href': "https://codepen.io/chriddyp/pen/bWLwgP.css",
                                       'rel': 'stylesheet'}])
image_filename = 'data//hhs_analysis//April.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')

colors = {"background": "#F3F6FA", "background_div": "#DFDDDF", 'text': '#009999'}


def create_card(card_id, title):
    return dbc.Card(
        dbc.CardBody(
            [
                # html.Div(style={'backgroundColor': colors['background_div']}, children=[
                html.H4(title, id=f"{card_id}-title"),
                html.H6("100", id=f"{card_id}-value"),
                html.Img(src='data:image/png;base64,{}'.format(encoded_image))
                    # ]
                # )
            ]
        )
    )

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Legislature Text Scraper', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children=[

        html.Div(children=[
            html.Label('State'),
            dcc.Dropdown(
                options=[
                    {'label': 'Nevada', 'value': 'NV'},
                ],
                value='NV',
                style=dict(
                    width='100%',
                )
            ),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '30%', 'margin-left': '6vw', 'margin-top': '2vw', 'margin-bottom': '2vw'}),

        html.Div(children=[
            html.Label('Committee'),
            dcc.Dropdown(
                options=[
                    {'label': 'Health and Human Service Committee', 'value': 'HHS'},
                    {'label': 'Finance Committee', 'value': 'FIN'},
                ],
                value='HHS',
                style=dict(
                    width='100%',
                )
            ),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '50%', 'margin-left': '10vw', 'margin-top': '2vw', 'margin-bottom': '2vw'}),

        html.Br(),
        html.Label('Time by month'),
        dcc.RangeSlider(
            min=1,
            max=5,
            step=None,
            marks={
                1: 'JAN',
                2: 'FEB',
                3: 'MAR',
                4: 'APR',
                5: 'MAY',
            },
            value=[1, 4]
        ),

        html.Br(),
        html.Label('Search Topic'),
        dcc.Input(value='Covid 19', type='text', style=dict(width='100%', )),

    ], style={'padding': 10, 'flex': 1}),

    html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H3("Content analysis", style={
            'textAlign': 'left',
            'margin-left': '6vw',
            'margin-top': '6vw',
        }),

        # first column of first row
        html.Div(children=[
            create_card('1', 'Title')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

        # second column of first row
        html.Div(children=[
            create_card('2', 'Title')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

        # Third column of first row
        html.Div(children=[
            create_card('3', 'Title')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)



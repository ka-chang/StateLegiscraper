"""
LegTextScraper Plotly Dash Dashboard
"""
import base64

import json
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output

from LegTextScraper import dashboard_helper

app = dash.Dash(__name__,
                external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css",
                                      {'href': "https://codepen.io/chriddyp/pen/bWLwgP.css",
                                       'rel': 'stylesheet'}])
colors = {"background": "#F3F6FA", "background_div": "#DFDDDF", 'text': '#009999'}


def create_card(card_id, title):
    image_filename = 'data//hhs_analysis//April.png'
    encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
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
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '30%', 'margin-left': '6vw',
                  'margin-top': '2vw', 'margin-bottom': '2vw'}),

        html.Div(children=[
            html.Label('Committee'),
            dcc.Dropdown(
                id='committee',
                options=[
                    {'label': 'Health and Human Service Committee', 'value': 'HHS'},
                    {'label': 'Finance Committee', 'value': 'FIN'},
                ],
                value='HHS',
                style=dict(
                    width='100%',
                )
            ),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '50%', 'margin-left': '10vw',
                  'margin-top': '2vw', 'margin-bottom': '2vw'}),

        html.Br(),
        html.Label('Time by month'),
        dcc.RangeSlider(
            id='slider',
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
        dcc.Input(id='query', value='Covid 19', type='text', style=dict(width='100%', )),

    ], style={'padding': 10, 'flex': 1}),

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

    html.Div(id='div_variable'),

    html.H3("Sentiment analysis", style={
        'textAlign': 'left',
        'margin-left': '6vw',
        'margin-top': '6vw',
    }),

    # first column of first row
    html.Div(children=[
        create_card('11', 'Title')
    ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

    # second column of first row
    html.Div(children=[
        create_card('22', 'Title')
    ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

])


def create_wordcloud(card_id, title, key_words, file_name):
    image_path = 'dashboard//wordcloud//' + file_name
    encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('ascii')
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, id=f"{card_id}-title"),
                html.H6("Keywords: " + ", ".join(key_words)),
                html.Img(src='data:image/png;base64,{}'.format(encoded_image))
            ]
        )
    )

@app.callback(
    Output('div_variable', 'children'),
    [Input('slider', 'value')],
    Input('committee', 'value'),
    Input('query', 'value'),
)
def update_div(num_div, file, query):
    if file == "HHS":
        data_by_date = dashboard_helper.NVHelper.nv_extract_date("data//hhs_analysis//cleaned_data.json")
    elif file == 'FIN':
        data_by_date = dashboard_helper.NVHelper.nv_extract_date("data//fin_analysis//cleaned_data.json")
    else:
        data_by_date = dashboard_helper.NVHelper.nv_extract_date("data//hhs_analysis//cleaned_data.json")

    sm_search = dashboard_helper.NVSemanticSearching(data_by_date, query, 5)
    # filtered_dict = sm_search.rapid_searching("data//hhs_data//")
    file_dict = open("data//hhs_analysis//hhs_nv_filter.json", 'r', encoding='utf-8')
    filtered_dict = json.load(file_dict)

    text_preprocessing = dashboard_helper.NVTextProcessing(filtered_dict)
    text_preprocessing.text_processing()
    processed_dict = text_preprocessing.json

    word_freq_month = {}
    for i in processed_dict.keys():
        month = i[:2]
        if month not in word_freq_month:
            word_freq_month[month] = processed_dict[i]
        else:
            word_freq_month[month].extend(processed_dict[i])

    analysis_freq = dashboard_helper.NVTextAnalysis(word_freq_month)
    _, word_freq = analysis_freq.word_frequency()
    _, word_key = analysis_freq.key_word_by_month()
    for i in range(num_div[0]+1, num_div[1]+1):
        dashboard_helper.NVVisualizations.word_cloud(word_freq[str(i).zfill(2)], "dashboard//wordcloud//", str(i).zfill(2))
    results = dashboard_helper.NVVisualizations.key_word_display(word_key, 6)
    month = {'05': 'May', '04': 'April', '03': 'March', '02': 'February', '01': 'January', }
    return [html.Div(children=[
            create_wordcloud(f'{i}', month[str(i).zfill(2)], results[str(i).zfill(2)], str(i).zfill(2) + '.png')
            # create_card(f'{i}', "Title")
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}
        ) for i in range(num_div[0]+1, num_div[1]+1)]


if __name__ == '__main__':
    app.run_server(debug=True)

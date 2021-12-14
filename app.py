"""
LegTextScraper Plotly Dash Dashboard
"""
import base64

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
'''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
'''
from statelegiscraper import dashboard_helper

app = dash.Dash(__name__,
                external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css",
                                      {'href': "https://codepen.io/chriddyp/pen/bWLwgP.css",
                                       'rel': 'stylesheet'}])

##########################################
# App Layout
##########################################


def create_card(card_id, title,file_name):
    image_filename = 'data//dashboard//plots//'+file_name
    encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
    return dbc.Card(
        dbc.CardBody(
            [
                # html.Div(style={'backgroundColor': colors['background_div']}, children=[
                html.H4(title, id=f"{card_id}-title"),
                #html.H6("100", id=f"{card_id}-value"),
                html.Img(src='data:image/png;base64,{}'.format(encoded_image))
                # ]
                # )
            ]
        )
    )


colors = {"background": "#F3F6FA", "background_div": "#DFDDDF", 'text': '#009999'}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('StateLegiscraper', style={
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
            value=[2, 5]
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

    html.Div(id='div_variable'),
    html.Div(id='div_variable2'),
   

    

])


##########################################
# Interactive Parts
##########################################


def create_wordcloud(card_id, title, key_words, file_name):
    """Takes word cloud plot and keywords. Generate a Card component"""
    image_path = 'data//dashboard//plots//' + file_name
    encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('ascii')
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, id=f"{card_id}-title"),
                html.H6("Keywords: " + ", ".join(key_words)),
                html.Img(src='data:image/png;base64,{}'.format(encoded_image),
                         style={'height': '100%', 'width': '100%'})
            ]
        )
    )


@app.callback(
    Output('div_variable', 'children'),
    Output('div_variable2', 'children'),
    [Input('slider', 'value')],
    Input('committee', 'value'),
    Input('query', 'value'),
)
def update_div(num_div, file, query):
    """Takes committee, time, and topic. Run semantic searching, text processing and analysis.
    Update the Content Analysis part of the web."""
    # Read in data
    if file == "HHS":
        data_by_date = dashboard_helper.NVHelper.nv_extract_date("data//dashboard//nv_hhs_analysis//cleaned_data.json")
    elif file == 'FIN':
        data_by_date = dashboard_helper.NVHelper.nv_extract_date("data//dashboard//nv_fin_analysis//cleaned_data.json")
    else:
        data_by_date = {}

    # Semantic searching
    sm_search = dashboard_helper.NVSemanticSearching(data_by_date, query, 5)
    if file == "HHS":
        filtered_dict = sm_search.rapid_searching("data//dashboard//nv_hhs_analysis//")
    elif file == 'FIN':
        filtered_dict = sm_search.rapid_searching("data//dashboard//nv_fin_analysis//")
    else:
        filtered_dict = {}

    # Organize the data by the month
    data_by_month = {}
    for i in filtered_dict.keys():
        month = i[:2]
        if month == '06' or month == '09':
            continue
        if month not in data_by_month:
            data_by_month[month] = filtered_dict[i]
        else:
            data_by_month[month].extend(filtered_dict[i])
    dashboard_helper.sentiment_analysis(data_by_month,'data//dashboard//plots//')

    # Text cleaning
    text_preprocessing = dashboard_helper.NVTextProcessing(data_by_month)
    text_preprocessing.text_processing()
    processed_dict = text_preprocessing.json

    # Analysis: word frequency, tf-idf for key word extraction
    analysis_freq = dashboard_helper.NVTextAnalysis(processed_dict)
    _, word_freq = analysis_freq.word_frequency()
    _, word_key = analysis_freq.tf_idf_analysis()

    # Visualization: save word cloud plots, generate yop key words
    month = {'05': 'May', '04': 'April', '03': 'March', '02': 'February', '01': 'January', }
    for i in range(2, 4 + 1):
        dashboard_helper.NVVisualizations.word_cloud(word_freq[str(i).zfill(2)], "data//dashboard//plots//", str(i).zfill(2))
    results = dashboard_helper.NVVisualizations.key_word_display(word_key, 4)


    
    
    return [html.Div(children=[
        create_wordcloud(f'{i}', month[str(i).zfill(2)], results[str(i).zfill(2)], str(i).zfill(2) + '.png')
    ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}
    ) for i in range(num_div[0], num_div[1] + 1)],[html.H3("Sentiment analysis", style={
        'textAlign': 'left',
        'margin-left': '6vw',
        'margin-top': '6vw',
    }),html.Div(children=[
        create_card('77', 'sentiment variability','sentiment.png')
    ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw',
              'margin-bottom': '6vw', })]


if __name__ == '__main__':
    app.run_server(debug=True)

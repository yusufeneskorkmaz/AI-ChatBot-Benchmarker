import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from src.AIAppReviewAnalyzer.pipeline.review_analysis_pipeline import ReviewAnalysisPipeline

# Initialize the Dash app with a dark Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define the app IDs and their corresponding names and links
APP_INFO = {
    'com.openai.chatgpt': {'name': 'ChatGPT',
                           'link': 'https://play.google.com/store/apps/details?id=com.openai.chatgpt'},
    'com.anthropic.claude': {'name': 'Claude by Anthropic',
                           'link': 'https://play.google.com/store/apps/details?id=com.anthropic.claude'},
    'com.google.android.apps.bard': {'name': 'Google Gemini',
                                     'link': 'https://play.google.com/store/apps/details?id=com.google.android.apps.bard'},
    'com.microsoft.copilot': {'name': 'Microsoft Copilot',
                              'link': 'https://play.google.com/store/apps/details?id=com.microsoft.copilot'},
    'com.microsoft.bing': {'name': 'Bing: Chat with AI & GPT-4',
                           'link': 'https://play.google.com/store/apps/details?id=com.microsoft.bing'},
    'com.codespaceapps.aichat': {'name': 'Chatbot AI & Smart Assistant',
                                 'link': 'https://play.google.com/store/apps/details?id=com.codespaceapps.aichat'},
    'ai.chat.gpt.bot': {'name': 'ChatOn - AI Chat Bot Assistant',
                        'link': 'https://play.google.com/store/apps/details?id=ai.chat.gpt.bot'},
    'ai.perplexity.app.android': {'name': 'Perplexity - Ask Anything',
                                  'link': 'https://play.google.com/store/apps/details?id=ai.perplexity.app.android'},
    'com.mlink.ai.chat.assistant.robot': {'name': 'AI Chat・Ask Chatbot Assistant',
                                          'link': 'https://play.google.com/store/apps/details?id=com.mlink.ai.chat.assistant.robot'},
    'co.appnation.geniechat': {'name': 'Chatbot 4o AI Chat - Genie',
                               'link': 'https://play.google.com/store/apps/details?id=co.appnation.geniechat'}
}

# Run the analysis pipeline
pipeline = ReviewAnalysisPipeline(list(APP_INFO.keys()))
sentiment_summaries = pipeline.run()

# Prepare data for visualization
df_list = []
for app_id, summary in sentiment_summaries.items():
    df = summary.reset_index()
    df['app_id'] = app_id
    df['app_name'] = APP_INFO[app_id]['name']
    df_list.append(df)

df_all = pd.concat(df_list)

# Calculate overall sentiment score
df_all['sentiment_score'] = df_all.apply(
    lambda row: row['Percentage'] if row['sentiment'] == 'POSITIVE' else -row['Percentage'] if row['sentiment'] == 'NEGATIVE' else 0,
    axis=1)
overall_sentiment = df_all.groupby('app_name')['sentiment_score'].sum().sort_values(ascending=False).reset_index()
overall_sentiment['rank'] = overall_sentiment['sentiment_score'].rank(ascending=False, method='dense')

# Custom color scheme
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'positive': '#00FFA3',
    'negative': '#FF3863',
    'neutral': '#7C7C7C'
}

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("AI Chat App Review Sentiment Analysis", className="text-center mb-4 text-info"), width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='app-dropdown',
                options=[{'label': APP_INFO[app_id]['name'], 'value': app_id} for app_id in APP_INFO],
                value=list(APP_INFO.keys())[0],
                className="mb-4"
            )
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sentiment Distribution", className="bg-primary text-white"),
                dbc.CardBody(dcc.Graph(id='sentiment-pie-chart'))
            ], color="dark")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("App Details", className="bg-primary text-white"),
                dbc.CardBody([
                    html.H4(id='app-name', className="text-info"),
                    html.P(id='app-link'),
                    html.H5("Sentiment Breakdown:", className="text-warning"),
                    html.Div(id='sentiment-breakdown')
                ])
            ], color="dark")
        ], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sentiment Comparison Across Apps", className="bg-primary text-white"),
                dbc.CardBody(dcc.Graph(id='sentiment-comparison-chart'))
            ], color="dark")
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("App Ranking by Overall Sentiment", className="bg-primary text-white"),
                dbc.CardBody(dash_table.DataTable(
                    id='ranking-table',
                    columns=[
                        {"name": "Rank", "id": "rank"},
                        {"name": "App Name", "id": "app_name"},
                        {"name": "Overall Sentiment Score", "id": "sentiment_score"}
                    ],
                    data=overall_sentiment.to_dict('records'),
                    style_table={'backgroundColor': colors['background']},
                    style_header={
                        'backgroundColor': '#1E1E1E',
                        'color': colors['text'],
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'backgroundColor': colors['background'],
                        'color': colors['text'],
                        'border': f'1px solid {colors["text"]}',
                        'textAlign': 'left'
                    },
                    style_data_conditional=[
                        {
                            'if': {'column_id': 'sentiment_score'},
                            'color': colors['positive'],
                            'fontWeight': 'bold'
                        },
                        {
                            'if': {'filter_query': '{sentiment_score} < 0'},
                            'color': colors['negative'],
                            'fontWeight': 'bold'
                        }
                    ]
                ))
            ], color="dark")
        ], width=12)
    ])
], fluid=True, style={'backgroundColor': colors['background'], 'color': colors['text']})

# Callback for updating the pie chart
@app.callback(
    Output('sentiment-pie-chart', 'figure'),
    Input('app-dropdown', 'value')
)
def update_pie_chart(selected_app):
    df_app = df_all[df_all['app_id'] == selected_app]
    fig = px.pie(df_app, values='Percentage', names='sentiment',
                 title=f"Sentiment Distribution for {APP_INFO[selected_app]['name']}",
                 color='sentiment',
                 color_discrete_map={'POSITIVE': colors['positive'], 'NEGATIVE': colors['negative'], 'NEUTRAL': colors['neutral']})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        legend_title_text='Sentiment',
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

# Callback for updating the comparison chart
@app.callback(
    Output('sentiment-comparison-chart', 'figure'),
    Input('app-dropdown', 'value')
)
def update_comparison_chart(selected_app):
    fig = px.bar(df_all, x='app_name', y='Percentage', color='sentiment',
                 title="Sentiment Comparison Across Apps",
                 labels={'app_name': 'App Name', 'Percentage': 'Percentage of Reviews'},
                 color_discrete_map={'POSITIVE': colors['positive'], 'NEGATIVE': colors['negative'], 'NEUTRAL': colors['neutral']},
                 height=500)
    fig.update_layout(
        barmode='stack',
        xaxis={'categoryorder': 'total descending'},
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

# Callback for updating app details
@app.callback(
    [Output('app-name', 'children'),
     Output('app-link', 'children'),
     Output('sentiment-breakdown', 'children')],
    Input('app-dropdown', 'value')
)
def update_app_details(selected_app):
    app_name = APP_INFO[selected_app]['name']
    app_link = dcc.Link(f"View on Google Play Store", href=APP_INFO[selected_app]['link'], target="_blank", className="text-info")

    df_app = df_all[df_all['app_id'] == selected_app]
    breakdown = [
        html.P(f"{sentiment}: {percentage:.2f}%", style={'color': colors['positive'] if sentiment == 'POSITIVE' else colors['negative'] if sentiment == 'NEGATIVE' else colors['neutral']})
        for sentiment, percentage in zip(df_app['sentiment'], df_app['Percentage'])
    ]

    return app_name, app_link, breakdown

if __name__ == '__main__':
    app.run_server(debug=True)
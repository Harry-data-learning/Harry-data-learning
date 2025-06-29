# ----------------------------------------------------------
# SpaceX Rocket Launch Data Project Script 7
# SpaceX Rocket Launch Dashboard (Plotly Dash)
# Purpose: Create interactive dashboard with dropdown, pie chart, range slider, and scatter plot
# Author: Harry.Zhang
# ----------------------------------------------------------

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Extract payload range boundaries
min_payload = df['Payload Mass (kg)'].min()
max_payload = df['Payload Mass (kg)'].max()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "SpaceX Launch Dashboard"

# Layout definition
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Launch site dropdown filter
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),

    html.Br(),

    # Pie chart output
    dcc.Graph(id='success-pie-chart'),

    html.Br(),
    html.P("Payload range (Kg):"),

    # Payload range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # Scatter plot output
    dcc.Graph(id='success-payload-scatter-chart'),
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(df, values='class', names='Launch Site',
                     title='Total Success Launches By Site')
    else:
        filtered_df = df[df['Launch Site'] == selected_site]
        site_counts = filtered_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        site_counts['class'] = site_counts['class'].replace({1: 'Success', 0: 'Failure'})
        fig = px.pie(site_counts, values='count', names='class',
                     title=f'Total Launch Outcomes for site {selected_site}')
    return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    filtered_df = df[(df['Payload Mass (kg)'] >= payload_range[0]) &
                     (df['Payload Mass (kg)'] <= payload_range[1])]

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Correlation between Payload and Success')
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)

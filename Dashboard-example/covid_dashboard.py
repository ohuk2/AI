import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# URLs to the datasets
confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

# Load datasets
df_confirmed = pd.read_csv(confirmed_url)
df_deaths = pd.read_csv(deaths_url)
df_recovered = pd.read_csv(recovered_url)

#print(df_confirmed)
# Function to transform the data
def preprocess_data(df):
    df = df.drop(["Province/State", "Lat", "Long"], axis=1)
    df = df.groupby("Country/Region").sum()
    df = df.transpose()
    df.index = pd.to_datetime(df.index)
    return df

df_confirmed = preprocess_data(df_confirmed)
df_deaths = preprocess_data(df_deaths)
df_recovered = preprocess_data(df_recovered)

print (df_confirmed)

# Function to transform the data

print (df_confirmed)
# Initialize the app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("COVID-19 Dashboard"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df_confirmed.columns],
        value='United States',
        multi=True
    ),
    dcc.Graph(id='covid-graph'),
    dcc.RadioItems(
        id='data-type',
        options=[
            {'label': 'Confirmed', 'value': 'confirmed'},
            {'label': 'Deaths', 'value': 'deaths'},
            {'label': 'Recovered', 'value': 'recovered'}
        ],
        value='confirmed',
        labelStyle={'display': 'inline-block'}
    )
])

# Update the graph based on selected countries and data type
@app.callback(
    Output('covid-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('data-type', 'value')]
)
def update_graph(selected_countries, data_type):
    if not isinstance(selected_countries, list):
        selected_countries = [selected_countries]

    if data_type == 'confirmed':
        df = df_confirmed
    elif data_type == 'deaths':
        df = df_deaths
    else:
        df = df_recovered

    traces = []
    for country in selected_countries:
        traces.append(go.Scatter(
            x=df.index,
            y=df[country],
            mode='lines+markers',
            name=country
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title=f'COVID-19 {data_type.capitalize()} Cases Over Time',
            xaxis={'title': 'Date'},
            yaxis={'title': f'Number of {data_type.capitalize()} Cases'},
            hovermode='closest'
        )
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
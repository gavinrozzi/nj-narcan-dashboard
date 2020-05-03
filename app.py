# Gavin Rozzi
# Data Visualization
# Spring, 2020
# Final Project

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 
import dash
import dash_core_components as dcc
import dash_html_components as html
import time


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#1a1a1a'
}

mapbox_access_token = open(".mapbox_token").read()

# Load dataset and parse the date / time
data = pd.read_csv("data/narcan.csv", parse_dates=['Date'])
data = data.sort_values(by='Date',ascending=True)

# Create new columns for analyzing based upon year and month and over time. Could be extended with additional data.
data['Date'+"_year"] = data['Date'].apply(lambda x: x.year)
data['Date'+"_month"] = data['Date'].apply(lambda x: x.month)

# Get the count of Narcan administrations per day
data['Incident Count'] = range(1, 1+len(data))

mintime = data['Date'].min()
readable = mintime.strftime("%m/%d/%Y")

# Get county-level stats from other file
county_stats = pd.read_csv("data/counties.csv")

# Read monthly summary data file
monthly = pd.read_csv("data/month_summary.csv")

# Plot first figure, map of points
fig = px.scatter_mapbox(data, lat="Latitude", lon="Longitude", hover_name="Date", hover_data=["Town", "Vic Town"],
                        color_discrete_sequence=["white"], zoom=6, height=800)
fig.update_layout(mapbox_style="dark",mapbox_accesstoken=mapbox_access_token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=40,
            lon=-74
        ),
        pitch=0,
        zoom=7.5
    )
)

# Second figure, line chart
fig2 = px.line(data, x='Date', y= 'Incident Count',title='Narcan Deployments Over Time')


# Third figure, bar chart by county
fig3 = px.bar(county_stats, x='County', y= 'Incidents',title='Narcan Deployments By County', color = 'Incidents')

# Fourth figure, bar chart by month
fig4 = px.bar(monthly, x='Month', y= 'Count',title='Narcan Deployments By Month', color = 'Count', color_continuous_scale=px.colors.sequential.Viridis)


app.layout = html.Div(children=[
    html.H1(children='New Jersey Narcan Deployment Dashboard',
        style={
        'textAlign': 'center',
        'color': colors['background']}
    ),

    html.P(children='Narcan is a life-saving drug that can reverse opiate overdoses. This dashboard is tracking incidents where it was used in New Jersey during 2019.',
         style={
        'textAlign': 'center'}
        ),
    html.H4(children='Tracking '+str(data['Date'].count())+' incidents statewide since '+str(readable),
        style={
        'textAlign': 'center'}
    ),

    html.Div(children='Data provided by New Jersey State Police, Office of Drug Monitoring & Analysis',
        style={
        'textAlign': 'center'}
        ),
  
    dcc.Graph(
        figure=fig),
    dcc.Graph(
        figure=fig2),
    dcc.Graph(
        figure=fig3),
    dcc.Graph(
        figure=fig4)
])
if __name__ == '__main__':
    app.run_server(debug=True)
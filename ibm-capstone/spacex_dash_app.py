# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(min_payload, max_payload)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                              options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                ],
                                                value='ALL',
                                                placeholder='Select a Launch Site here',
                                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                                id='payload-slider',
                                                min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1, 1000)},
                                                value=[min_payload, max_payload]
                                            ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(selected_site):
    if selected_site == 'ALL':
        success_counts = spacex_df['class'].value_counts()
        fig = px.pie(
            names=success_counts.index,
            values=success_counts.values,
            title="Total Success vs Failure Launches"
        )
        return fig
    else:
        df_filtered = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_counts = df_filtered['class'].value_counts()
        fig = px.pie(
            names=success_counts.index,
            values=success_counts.values,
            title=f"Success vs Failure Launches for site: {selected_site}"
        )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter dataframe based on payload range
    min_payload, max_payload = payload_range
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                            (spacex_df['Payload Mass (kg)'] <= max_payload)]

    if selected_site == 'ALL':
        # Render scatter plot for all sites
        fig = px.scatter(
            df_filtered,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title="Correlation between Payload Mass and Launch Success"
        )
    else:
        # Filter further based on selected site
        df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]
        fig = px.scatter(
            df_filtered,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f"Correlation between Payload Mass and Launch Success for site: {selected_site}"
        )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

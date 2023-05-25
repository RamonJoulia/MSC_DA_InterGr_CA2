import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('nda_pivot.csv')

# Create the Dash app
app = dash.Dash(__name__)

# Set up the app layout
app.layout = html.Div([ 
    html.H1('New Dwellings by year',style={'fontSize':50, 'textAlign':'center'}), # title
    html.H2("By property type:",style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id='prop-type-dropdown', # dropdown name
                options=[{'label':i,'value':i}
                        for i in df['prop_type'].unique()], # dropdown content
                value=[],  # default value
                multi=True 
                #style={'width':'40%'}
                ),
    dcc.Graph(id='nda-graph'),
    html.H2(''),
    html.H2("Property type proportion by year:",style={'fontSize':30, 'textAlign':'center'}),
    html.H2(''),
    html.Label('Select year:',style={'fontSize':20}),
    dcc.Slider(id='year-slider',
              min=df['year'].min(),
              max=df['year'].max(),
              step=1,
              marks=None,
              tooltip={'placement':'bottom','always_visible':True}
              ),
    dcc.Graph(id='year-graph')
    ])

# Input1: prop-type-dropdown
# Output1: nda-graph

# Input2: year-slider
# Output2: year-graph

# Set up the callback funtion (makes it interactive)

# Decorator
@app.callback(
    Output(component_id='nda-graph', component_property='figure'),
    Input(component_id='prop-type-dropdown', component_property='value')
)

# Function
def update_graph(selected_prop): # selected_prop from Input callback function
   
    # Empty dataframe to store each loop
    selected = {'year':[],'prop_type':[],'avg_dwelling_size':[],'dwelling_type_perc':[],'new_dwelling':[]}
    selected_df = pd.DataFrame(selected)

    for i in selected_prop:
        loop_df = df[df['prop_type']==i]
        selected_df = pd.concat([selected_df, loop_df], ignore_index=True, sort=False)  
        
    line_fig = px.line(selected_df,
                       x='year', y='new_dwelling', color='prop_type')
    return line_fig # to Output callback function


@app.callback(
    Output(component_id='year-graph', component_property='figure'),
    Input(component_id='year-slider', component_property='value')
)

# Function
def update_graph(year): # selected_prop from Input callback function

    df2 = df[(df['year'] == year)&(df['prop_type'] != 'all_types')]
    
    pie_fig = px.pie(df2, values="new_dwelling", names="prop_type")
    
    return pie_fig # to Output callback function

# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)

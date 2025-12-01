import plotly.express as px
import pandas as pd
import plotly
import json
import plotly.io as pio

#creating the progress graphs using plotly
def stirring_graph(date_value_list):
    stirring_g = pd.DataFrame(date_value_list,
                    columns=['DateTime', 'Stirring'])
    df = pd.DataFrame(stirring_g)
    df['Stirring'] = df['Stirring'].astype(float)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    fig = px.line(df, x="DateTime", y="Stirring", markers=True) 
    fig.update_traces(marker_size=8)
    fig_dict = fig.to_dict()
    if 'data' in fig_dict and len(fig_dict['data']) > 0:
        fig_dict['data'][0]['x'] = df['DateTime'].astype(str).tolist()
        fig_dict['data'][0]['y'] = df['Stirring'].tolist()
    graphJSON = json.dumps(fig_dict)
    return graphJSON

def temperature_graph(date_value_list):
    temperature_g = pd.DataFrame(date_value_list,
                    columns=['DateTime', 'Temperature'])
    df = pd.DataFrame(temperature_g)
    df['Temperature'] = df['Temperature'].astype(float)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    fig = px.line(df, x="DateTime", y="Temperature", markers=True) 
    fig.update_traces(marker_size=8)
    fig_dict = fig.to_dict()
    if 'data' in fig_dict and len(fig_dict['data']) > 0:
        fig_dict['data'][0]['x'] = df['DateTime'].astype(str).tolist()
        fig_dict['data'][0]['y'] = df['Temperature'].tolist()
    graphJSON = json.dumps(fig_dict)
    return graphJSON

def ph_graph(date_value_list):
    ph_g = pd.DataFrame(date_value_list,
                    columns=['DateTime', 'PH'])
    df = pd.DataFrame(ph_g)
    df['PH'] = df['PH'].astype(float)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    fig = px.line(df, x="DateTime", y="PH", markers=True) 
    fig.update_traces(marker_size=8)
    fig_dict = fig.to_dict()
    if 'data' in fig_dict and len(fig_dict['data']) > 0:
        fig_dict['data'][0]['x'] = df['DateTime'].astype(str).tolist()
        fig_dict['data'][0]['y'] = df['PH'].tolist()
    graphJSON = json.dumps(fig_dict)
    return graphJSON
import plotly.express as px
import pandas as pd
import plotly
import json

#creating the progress graphs using plotly
def stirring_graph(datetime_list,stirring_list):
    array = []
    for x in range(len(datetime_list)):
        array.append([datetime_list[x],stirring_list[x]])
    stirring_g = pd.DataFrame(array,
                    columns=['DateTime', 'Stirring Speeds'])

    df = pd.DataFrame(stirring_g)
    fig = px.line(df, x="DateTime", y="Stirring Speeds", markers=True) 
    fig.update_traces(marker_size=8)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
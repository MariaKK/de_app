import os
from dash import Dash, html, dash_table, Input, Output
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

df = pd.read_sql(
    '''
    SELECT 
        name_common, 
        name_official, 
        name_native, 
        capital, 
        population, 
        flag, 
        tld, 
        cca2, 
        ccn3, 
        cioc, 
        independent, 
        status, 
        "unMember", 
        currencies, 
        idd, 
        "altSpellings", 
        region, 
        subregion, 
        languages, 
        latlng, 
        landlocked, 
        borders, 
        area, 
        demonyms, 
        cca3, 
        translations, 
        maps, 
        gini, 
        fifa, 
        timezones, 
        continents, 
        "startOfWeek", 
        car_signs, 
        car_side, 
        flag_png, 
        flag_svg, 
        "coatOfArms_png", 
        "coatOfArms_svg", 
        capital_lat, 
        capital_lng, 
        "postalCode_format", 
        "postalCode_regex", 
        fetch_time, 
        source, 
        api_version
    FROM countries
    ''',
    engine
)
app = Dash(__name__)

app.layout = html.Div(style={'display': 'flex', 'gap': '20px', 'alignItems': 'flex-start'}, children=[

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left', 'minWidth': '100px', 'whiteSpace': 'normal'},
        style_table={'overflowX': 'auto', 'width': '70vw', 'maxHeight': '80vh', 'overflowY': 'auto'},
        page_size=10,
        row_selectable='single',
        selected_rows=[],
       # hidden_columns=['flag_png'], #hide the column with the link to make the table look cleaner
        sort_action='native',
        filter_action='native'
    ),

    html.Div(id='flag-container', style={
        'width': '25vw',
        'minWidth': '200px',
    #    'border': '1px solid #ccc',
        'padding': '10px',
        'textAlign': 'center',
        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',
        'borderRadius': '5px',
        'height': 'fit-content'
    })
])

@app.callback(
    Output('flag-container', 'children'),
    Input('table', 'selected_rows')
)
def display_flag(selected_rows):
    if selected_rows:
        row = df.iloc[selected_rows[0]]
        flag_url = row['flag_png']                  #take the link on the flag for drawing the picture
        country = row['name_official']
        return html.Div([
            html.H3("Flag of selected country"),
            html.Img(src=flag_url, style={'height': '120px', 'marginTop': '10px','border': '1px solid #ccc'}),
            html.P(country, style={'marginTop': '10px', 'fontWeight': 'bold', 'fontSize': '18px'})
        ])
    else:
        return html.Div("No country selected", style={'color': '#888', 'fontStyle': 'italic'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)

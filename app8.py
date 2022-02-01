import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import decomposition
from sklearn import preprocessing
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_daq as daq

from functions_8 import circles, blank_fig

bg_color = '#4d6887'

colors = {
    'background': bg_color,
    'text': '#111111'
}

correlation = pd.read_csv('data_correlation.csv')
compare = pd.read_csv('data_compare.csv')
data_all = pd.read_csv('data_all.csv')
data_rec = pd.read_csv('data_rec.csv')
data_all_scatter = pd.read_csv('data_all_scatter.csv')
data_all_scaled = pd.read_csv('data_all_scaled.csv')

databio = pd.read_excel("agri_bio.xlsx", sheet_name = "AGB organic product")

impact = databio.iloc[0, 5:].values
unit = databio.iloc[1, 5:].values
units = dict(zip(impact, unit))

pca_columns = ['PCA - F1 - ', 'PCA - F2 - ', 'PCA - F3 - ', 'PCA - F4 - ']

columns_rec = ['Climate change',
       'Ozone depletion', 'Photochemical ozone formation, HH', 'Respiratory inorganics',
       'Acidification terrestrial and freshwater', 'Eutrophication freshwater',
       'Eutrophication marine', 'Eutrophication terrestrial']

columns_rec_simple = ['climat', 'ozone', 'qualite_air', 'particules_fines', 'acidification', 'eau_douce', 'marine', 'terrestre']

rec_dict = dict(zip(columns_rec_simple, columns_rec))

page1 = "Comparaisons entre deux produits"
page2 = "Bio / Conventionnel"
page3 = "Algorithme, suggestion de produit"
page4 = "Répartition des produits"

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR, dbc_css])

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link(page1, href='/page-1'),
    html.Br(),
    dcc.Link(page2, href='/page-2'),
    html.Br(),
    dcc.Link(page3, href='/page-3'),
    html.Br(),
    dcc.Link(page4, href='/page-4'),
])


#PAGE1--------------------------------------------------------------------



page_1_layout = html.Div(children=[
    
        html.H1("Impact environnemental des différents produits"),
    
        dcc.Dropdown(id='product-dropdown',
                    options=[{'label': i, 'value': i}
                            for i in data_all["Nom du Produit"]
                            ],
                    className = 'dbc',
                    value=data_all["Nom du Produit"][0],
                    style={"width": "50%"}
                    ),
    
        dcc.Dropdown(id='product-dropdown-2',
                    options=[{'label': i, 'value': i}
                            for i in data_all["Nom du Produit"]
                            ],
                    className = 'dbc',
                    value=data_all["Nom du Produit"][0],
                    style={
                        "width": "50%",
                        }
                    ),
    
        dcc.Dropdown(id='filter_dropdown',
                    options=[{'label': i, 'value' : i}
                            for i in data_all.columns[4:]
                            ],
                     className = 'dbc',
                     value = ["Climate change", 'Ozone depletion', 'Respiratory inorganics'],
                     multi = True,
                     style={"width": "50%"}
                    ),
        
        html.Br(),
        
        dcc.Graph(
            id='all-graph',
            figure = blank_fig()
            
        ),
    
        html.Div(id='page-1-content'),
        html.Br(),
        dcc.Link(page2, href='/page-2'),
        html.Br(),
        dcc.Link(page3, href='/page-3'),
        html.Br(),
        dcc.Link(page4, href='/page-4'),
        html.Br(),
        dcc.Link('Home', href='/'),
    ])


@app.callback(
    
    Output(component_id = 'all-graph', component_property = 'figure'),
    [
    Input(component_id = 'product-dropdown', component_property = 'value'),
    Input(component_id = 'product-dropdown-2', component_property = 'value'),
    Input(component_id = 'filter_dropdown', component_property = 'value')
    ]
    
)

def update_graph(selected_product, selected_product_2, selected_filter) :
    
    y1 = data_all_scaled[data_all_scaled["Nom du Produit"] == selected_product][selected_filter].values.tolist()[0]
    y2 = data_all_scaled[data_all_scaled["Nom du Produit"] == selected_product_2][selected_filter].values.tolist()[0]
    
    text = []
    num = data_all[data_all["Nom du Produit"] == selected_product][selected_filter].values.tolist()[0]
    
    for x, y in zip(num, units) :
            
        if x >= 1 :
            text.append(str(round(x, 3)) + " " + units[y]) 
        else :
            text.append('{:.3e}'.format(x) + " " + units[y])
    
    bar_fig = px.bar(x=selected_filter, 
                     y=[y1, y2],
                     text = text,
                     barmode = "group",
                     width=1600, 
                     height=800)
    
    bar_fig.update_traces(textfont_size=16)
    
    bar_fig.data[0].name = selected_product
    bar_fig.data[1].name = selected_product_2
    
    bar_fig.update_layout(   
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        
        xaxis_tickfont_size=16,
        yaxis=dict(
        title=' '
    ),
        
    legend=dict(
        x=1,
        y=1.0,
    ),
        
)

    return bar_fig

#PAGE2--------------------------------------------------------------------

page_2_layout = html.Div(children=[
    
    html.H1("Impact environnemental des différentes catégories de produits"),
    
    dcc.Dropdown(id='category-dropdown',
                options=[{'label': i + " ( " + units[i] + " - per kg )" , 'value': i}
                        for i in compare.columns[3:]],
                className = 'dbc',
                value=compare.columns[3]),
    
    dcc.Dropdown(id='aliment_dropdown',
                options=[{'label': 'Plant', 'value' : 1},
                        {'label': 'Animal', 'value' : 0}
                        ],
                 className = 'dbc',
                 value = ["Climate change", 1],
                 multi = True
                ),
    
    html.Br(),
    
    dcc.Graph(
        id='categ-graph',
        figure = blank_fig()
        
    ),
    
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link(page1, href='/page-1'),
    html.Br(),
    dcc.Link(page3, href='/page-3'),
    html.Br(),
    dcc.Link(page4, href='/page-4'),
    html.Br(),
    dcc.Link('Home', href='/')
])

@app.callback(
    
    Output(component_id = 'categ-graph', component_property = 'figure'),
    [Input(component_id = 'category-dropdown', component_property = 'value'),
    Input(component_id = 'aliment_dropdown', component_property = 'value')]
    
)

def update_graph(selected_category, selected_aliments) :
    
    bar_fig = px.bar(compare[compare["Plant?"].isin(selected_aliments)],
                     x=[i.split("\\")[-2] for i in compare[compare["Plant?"].isin(selected_aliments)]["Catégorie"]], 
                     y=selected_category, 
                     color="Type", 
                     barmode="group")
    
    bar_fig.update_layout(   
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
    )
    
    return bar_fig

#PAGE3----------------------------------------------------------------

dozens = {10:'10', 20:'20', 30:'30', 40:'40', 50:'50', 60:'60', 70:'70', 80:'80', 90:'90'}

page_3_layout = html.Div(children=[
    
    html.H1("Proposition de produits en fonction de l'importance portée"),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    
                    dcc.Slider( 
                        id = 'slider-climat',
                        min=0,
                        max=100,
                        step=1,
                        value=100,
                        marks=dozens,
                        className = 'dbc',
                        tooltip={'always visible' : True, 'placement' : 'top'},
                        ),
                ], style={'padding-top':11}),
                
            width = 3,
                    ),
            dbc.Col(
                html.Div("Changement Climatique", style={'fontSize': 20})
            ),
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    
                    dcc.Slider( 
                        id = 'slider-ozone',
                        min=0,
                        max=100,
                        step=1,
                        value=100,
                        marks=dozens,
                        className = 'dbc',
                        tooltip={'always visible' : True, 'placement' : 'top'},
                        ),
                ], style={'padding-top':11}),
                
            width = 3,
                    ),
            dbc.Col(
                html.Div("Appauvrissement de la couche d'ozone", style={'fontSize': 20})
            ),
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    
                    dcc.Slider( 
                        id = 'slider-particules_fines',
                        min=0,
                        max=100,
                        step=1,
                        value=100,
                        marks=dozens,
                        className = 'dbc',
                        tooltip={'always visible' : True, 'placement' : 'top'},
                        ),
                ], style={'padding-top':11}),
                
            width = 3,
                    ),
            dbc.Col(
                html.Div("Exposition aux particules fines", style={'fontSize': 20})
            ),
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    
                    dcc.Slider( 
                        id = 'slider-acidification',
                        min=0,
                        max=100,
                        step=1,
                        value=100,
                        marks=dozens,
                        className = 'dbc',
                        tooltip={'always visible' : True, 'placement' : 'top'},
                        ),
                ], style={'padding-top':11}),
                
            width = 3,
                    ),
            dbc.Col(
                html.Div("Acidification", style={'fontSize': 20})
            ),
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    
                    dcc.Slider( 
                        id = 'slider-eau_douce',
                        min=0,
                        max=100,
                        step=1,
                        value=100,
                        marks=dozens,
                        className = 'dbc',
                        tooltip={'always visible' : True, 'placement' : 'top'},
                        ),
                ], style={'padding-top':11}),
                
            width = 3,
                    ),
            dbc.Col(
                html.Div("Euthrophisation eau douce", style={'fontSize': 20})
            ),
            dbc.Col(
                html.Div("Sélectionner une catégorie de produit", style={'fontSize': 20})
            ),
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    
                    dcc.Slider( 
                        id = 'slider-marine',
                        min=0,
                        max=100,
                        step=1,
                        value=100,
                        marks=dozens,
                        className = 'dbc',
                        tooltip={'always visible' : True, 'placement' : 'top'},
                        ),
                ], style={'padding-top':11}),
                
            width = 3,
                    ),
            dbc.Col(
                html.Div("Euthrophisation marine", style={'fontSize': 20})
            ),
            dbc.Col(
                dcc.Dropdown(id='category-rec_dropdown',
                options=[{'label': i, 'value': i}
                        for i in data_rec["categ_rec"].unique()],
                value = 'Viande',
                className = 'dbc'),
            )
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    
                    dcc.Slider( 
                        id = 'slider-terrestre',
                        min=0,
                        max=100,
                        step=1,
                        value=100,
                        marks=dozens,
                        className = 'dbc',
                        tooltip={'always visible' : True, 'placement' : 'top'},
                        ),
                ], style={'padding-top':11}),
                
            width = 3,
                    ),
            dbc.Col(
                html.Div("Euthrophisation terrestre", style={'fontSize': 20})
                
            ),
            dbc.Col(
                html.Div("Sélectionner un produit", style={'fontSize' : 20})
            )
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    
                    dcc.Slider( 
                        id = 'slider-qualite_air',
                        min=0,
                        max=100,
                        step=1,
                        value=100,
                        marks=dozens,
                        className = 'dbc',
                        tooltip={'always visible' : True, 'placement' : 'top'},
                        ),
                ], style={'padding-top':11}),
                
            width = 3,
                    ),
            dbc.Col(
                html.Div("Drégadation de la qualité de l'air", style={'fontSize': 20})
            ),
            dbc.Col(
                html.Div([
                    dcc.Dropdown(id='product-rec_dropdown',
                    options=[{'label': data_rec[data_rec["Nom du Produit"] == i]["categ_rec"] + ' - ' + i, 'value': i}
                            for i in data_rec["Nom du Produit"].unique()],
                    className = 'dbc',
                    value='Poulet, Bleu Blanc Coeur, at farm gate/FR U'),
                ])
            )
        ]
    ),
    
    dcc.Graph(
            id='rec_graph',
            figure = blank_fig()
    ),
    
    html.Div(id='page-3-content'),
    html.Br(),
    dcc.Link(page1, href='/page-1'),
    html.Br(),
    dcc.Link(page2, href='/page-2'),
    html.Br(),
    dcc.Link(page4, href='/page-4'),
    html.Br(),
    dcc.Link('Home', href='/')
])

@app.callback(
    Output('rec_graph', 'figure'),
    [Input('slider-climat', 'value'),
    Input('slider-ozone', 'value'),
    Input('slider-particules_fines', 'value'),
    Input('slider-acidification', 'value'),
    Input('slider-eau_douce', 'value'),
    Input('slider-marine', 'value'),
    Input('slider-terrestre', 'value'),
    Input('slider-qualite_air', 'value'),
    Input('product-rec_dropdown', 'value'),
    Input('category-rec_dropdown', 'value')]
)

def update_ozone(climat, ozone, particules_fines, acidification, eau_douce, marine, terrestre, qualite_air, product_dropdown, categ_dropdown) :
    
    if dash.callback_context.triggered[0]['prop_id'] != '.' :
        name_s = dash.callback_context.triggered[0]['prop_id'].split('.')[0].split('-')[1]
    else :
        name_s = 'climat'

    
 #Modifie la valeur d'impact en fonction de l'importance accordée par l'utilisateur
    if name_s in ['climat', 'ozone', 'particules_fines', 'acidification', 'eau_douce', 'marine', 'terrestre', 'qualite_air'] :
        name = rec_dict[name_s]
        data_rec[name] = data_all_scaled[name]*(vars()[name_s]/100)
    
    
    data_rec["total"] = 0

    for col in columns_rec :
        data_rec["total"] = data_rec["total"] + data_rec[col]
    
    graph_list = (data_rec[data_rec["categ_rec"] == categ_dropdown].sort_values(by=["total"]).head(3)["Nom du Produit"].values.tolist() 
    + [product_dropdown] 
    + data_rec[data_rec["categ_rec"] == categ_dropdown].sort_values(by=["total"]).tail(3)["Nom du Produit"].values.tolist())
    
    
    value_list = []
    for i in graph_list :
        value_list.append(data_rec[data_rec["Nom du Produit"] == i]["total"].values[0])

    graph_list[3] = graph_list[3] + ' '
    
    if categ_dropdown == 'Poisson' :
        graph_list[4] = graph_list[4] + ' '
    
    bar_fig = px.bar(x=graph_list, 
                     y=value_list,
                     color = value_list,
                     hover_name = graph_list,
                     color_continuous_scale='Turbo',
                     width=1900, 
                     height=800,
                    barmode = 'group')
    
    
    bar_fig.update_layout(   
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
    )
    
    return bar_fig


#PAGE4---------------------------------------------------------------


page_4_layout = html.Div(children=[
    
    html.H1('Répartition des produits en fonction des différentes catégories d\'impact'),
    
    dbc.Row([
            dbc.Col(
                html.Div('Abscisse X :', style={'fontSize': 20})
            ),
            dbc.Col(
                html.Div("Ordonnée Y :", style={'fontSize': 20})
            ),
    ]),
    
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='x_dropdown',
                options=[{'label': i, 'value': i}
                        for i in columns_rec + pca_columns],
                className = 'dbc',
                value = 'Climate change'),
        ),
        dbc.Col(
            dcc.Dropdown(id='y_dropdown',
                options=[{'label': i, 'value': i}
                        for i in columns_rec + pca_columns],
                className = 'dbc',
                value = 'Ozone depletion'),
        ),
    ]),
    
    dbc.Row([
            dbc.Col(
                html.Div('Taile des individus :', style={'fontSize': 20})
            ),
            dbc.Col(
                html.Div("Produit à mettre en valeur :", style={'fontSize': 20})
            ),
    ]),
    
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='size_dropdown',
                options=[{'label': i, 'value': i}
                        for i in columns_rec],
                value = 'Respiratory inorganics',
                className = 'dbc'),
        ),
        dbc.Col(
            dcc.Dropdown(id='highlight_dropdown',
                options=[{'label': data_rec[data_rec["Nom du Produit"] == i]["categ_rec"] + ' - ' + i, 'value': i}
                        for i in data_all["Nom du Produit"].unique()],
                value = None,
                className = 'dbc'),
        ),
    ]),
    
    dbc.Row([
        dbc.Col(
            html.Div('Catégories de produits selectionnées :', style={'fontSize' : 20}),
        ),
    ]),
    
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='categ_dropdown',
                options=[{'label': i, 'value': i}
                        for i in data_all_scatter["categ_s"].unique()],
                value = data_all_scatter['categ_s'].unique(),
                multi = True,
                className = 'dbc'),
        ),
    ]),
    
    html.Br(),
    
    dcc.Graph(
        id='scatter_graph',
        figure = blank_fig()
    ),
    
    html.Br(),
    html.Div('Cercles de corrélations ACP : ', style={'fontSize' : 20}),
    html.Br(),
    
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                figure = circles(correlation.columns[0], correlation.columns[1], correlation)
            ),
        ),
        
        dbc.Col(
            dcc.Graph(
                figure = circles(correlation.columns[2], correlation.columns[3], correlation)
            ),
        ),
    ]),
    
    html.Div(id='page-4-content'),
    dcc.Link(page1, href='/page-1'),
    html.Br(),
    dcc.Link(page2, href='/page-2'),
    html.Br(),
    dcc.Link(page3, href='/page-3'),
    html.Br(),
    dcc.Link('Home', href='/'),
])

@app.callback(
    Output('scatter_graph', 'figure'),
    [Input('x_dropdown', 'value'),
    Input('y_dropdown', 'value'),
    Input('size_dropdown', 'value'),
    Input('highlight_dropdown', 'value'),
    Input('categ_dropdown', 'value')]
)

def scatter_graph(x, y, size, highlight, categ) :
    
    if highlight is not None :
        
        temp = data_all_scatter[data_all_scatter["Nom du Produit"] == highlight]["Plant&Type"].values[0]
        data_all_scatter.loc[data_all_scatter["Nom du Produit"] == highlight, 'Plant&Type'] = 'Highlight'
    
    scatter_fig = px.scatter(data_all_scatter[data_all_scatter['categ_s'].isin(categ)],
                            x = x,
                            y = y,
                            size = size,
                            color = "Plant&Type",
                            hover_name = 'Nom du Produit',
                            color_discrete_map={'Animal conv': 'orange',
                                                'Animal organic': 'pink',
                                                'Non Animal conv' : 'lightblue',
                                                'Non Animal organic' : 'lightgreen',
                                               'Highlight' : 'red'},
                            size_max=80,
                            opacity = 0.6,
                            width=1800, 
                            height=1000,
                            )

    scatter_fig.update_traces(marker = dict(line = dict( width = 0)))

    scatter_fig.update_layout(   
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
    )

    if highlight is not None :
        data_all_scatter.loc[data_all_scatter["Nom du Produit"] == highlight, 'Plant&Type'] = temp
    
    return scatter_fig

#INDEX---------------------------------------------------------------
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)

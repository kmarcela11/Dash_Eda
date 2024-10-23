import dash
import numpy as np
import pandas as pd
from dash import dcc, html
from dash import dash_table
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc  

# Estilo de Dash con Bootstrap
app = dash.Dash(external_stylesheets=[dbc.themes.ZEPHYR], suppress_callback_exceptions=True)
server = app.server

# Datos a usar
file_path = r'eda.xlsx'
df = pd.read_excel(file_path)
df.rename(columns={'SoftwareVersion': 'Fecha'}, inplace=True)

# Asegurarte de que la columna 'Fecha' está en formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  # Convierte a datetime, ignorando errores
df['Mes'] = df['Fecha'].dt.month  # Extraer el mes de la columna 'Fecha'

# Definir las variables de interés
variables = ['WindSpeed80_2', 'Presion', 'temperatura 100m', 'Humedad']
titles = ['Velocidad del Viento a 80 m (Sensor 2)', 'Presión Promedio', 'Temperatura Promedio a 100 m', 'Humedad Promedio']
y_labels = ['Velocidad del Viento (m/s)', 'Presión (hPa)', 'Temperatura (°C)', 'Humedad (%)']

# Layout de la app
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([html.Img(src='/assets/images.png', style={'width': '195px', 'marginTop': 'auto'})]),
                html.Hr(style={'border': '2px solid #A7C6ED'}),
                dbc.Nav([
                    dbc.NavLink('INICIO', href='/', active='exact', style={'color': '#FFF', 'textAlign': 'center'}),
                    dbc.NavLink('EDA', href='/eda', active='exact', style={'color': '#FFF', 'textAlign': 'center'}),
                    dbc.NavLink('MODELOS', href='/modelos', active='exact', style={'color': '#FFF', 'textAlign': 'center'}),
                ], vertical=True, pills=True, style={'textAlign': 'center'})
            ], style={
                'position': 'fixed', 'top': 0, 'left': 0, 'bottom': 0, 'width': '15rem', 'padding': '20px', 'background-color': '#004F6D'
            })
        ]),
        dbc.Col([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ], width=10)
    ])
])

# Layout de las páginas
layout_pagina1 = html.Div([
    html.H1('De vientos y datos', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '3rem', 'color': '#004F6D', 'textShadow': '1px 1px 2px #000000'}),
    html.H5('Análisis de Series de Tiempo en Energía Eólica', style={'textAlign': 'center', 'color': '#000000'}),
    dcc.Tabs(id='tabs-intro', value='tab-intro', children=[
        dcc.Tab(label='Introducción', value='tab-int', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
        dcc.Tab(label='Descripción de los datos', value='tab-descripcion', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
        dcc.Tab(label='Diccionario de variables', value='tab-diccionario', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
    ]),
    html.Div(id='tabs-intro-content')
])

layout_pagina2 = html.Div([
    html.H1('Análisis exploratorio de datos', style={'fontWeight': 'bold', 'textAlign': 'center', 'color': '#004F6D'}),
    html.H5('En esta sección se mostrará por medio de gráficas y tablas el comportamiento de las variables y los datos.', style={'color': '#000000'}),
    dcc.Tabs(id='tabs-eda', value='tab-eda', children=[
        dcc.Tab(label='Análisis de variables', value='tab-graficos', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
        dcc.Tab(label='Descomposición Estacional', value='tab-tablas', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
        dcc.Tab(label='Datos faltantes', value='tab-estadisticas', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
    ]),
    html.Div(id='tabs-eda-content')
])

layout_pagina3 = html.Div([
    html.H1('Modelos de regresión lineal', style={'fontWeight': 'bold', 'textAlign': 'center', 'color': '#004F6D'}),
    dcc.Tabs(id='tabs-modelos', value='tab-modelo', children=[
        dcc.Tab(label='Modelo 1', value='tab-modelo1', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
        dcc.Tab(label='Modelo 2', value='tab-modelo2', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
        dcc.Tab(label='Modelo 3', value='tab-modelo3', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
        dcc.Tab(label='Modelo 4', value='tab-modelo4', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
        dcc.Tab(label='Modelo 5', value='tab-modelo5', style={'border': '2px solid #004F6D', 'color': '#004F6D', 'fontWeight': 'bold'}),
    ]),
    html.Div(id='tabs-modelos-content')
])

# Diccionario de variables
tabla = {
    'Variable': ['Fecha', 'WindSpeed100m_1', 'WinSpeed100m_2', 'WindSpeed80_1', 'WindSpeed80_2', 'WindSpeed60', 'Presion', 'humedad', 'temperatura 100m', 'temperatura 21 m', 'canal vacio', 'WindDirection100', 'WindDirection80', 'WindDirection60'],
    'Descripción': ['Fecha de la medición', 'Velocidad del viento a 100 metros, primer sensor', 'Velocidad del viento a 100 metros, segundo sensor', 'Velocidad del viento a 80 metros, primer sensor', 'Velocidad del viento a 80 metros, segundo sensor', 'Velocidad del viento a 60 metros', 'Presión atmosférica en la ubicación de la medición', 'Humedad relativa (%) en la ubicación de la medición', 'Temperatura a 100 metros de altura', 'Temperatura a 21 metros de altura', 'Variable de canal no utilizada, sin datos disponibles', 'Dirección del viento a 100 metros', 'Dirección del viento a 80 metros', 'Dirección del viento a 60 metros']
}
tabla_df = pd.DataFrame(tabla)


# Callback para mostrar el contenido en las pestañas de introducción
@app.callback(
    dash.dependencies.Output('tabs-intro-content', 'children'),
    [dash.dependencies.Input('tabs-intro', 'value')]
)
def tab_layout1(tab):
    if tab == 'tab-int':
        return html.Div([
            html.P([
                'Un sistema de monitoreo instalado en una región costera recoge datos cada 10 minutos sobre variables como ',
                html.B('velocidad y dirección del viento, temperatura, presión atmosférica y humedad relativa'),
                ', con el objetivo de evaluar la viabilidad de la generación de energía eólica. Estos sensores son fundamentales para ',
                html.B('cuantificar recursos eólicos y monitorear condiciones climáticas'),
                '. Este proyecto, liderado por ',
                html.B('Emanuel Carbonell y Kanery Camargo'),
                ', utiliza técnicas de ',
                html.B('Machine Learning (ARIMA, Prophet, LSTM)'),
                ' para analizar estas series de tiempo, identificar patrones y optimizar la predicción de energía eólica. Además, se desarrollarán visualizaciones interactivas para facilitar la toma de decisiones estratégicas basadas en estos datos.'
            ], style={'margin-top': '40px', 'text-align': 'justify'}),
            html.Div([
                html.Img(src='/assets/intro2.png', style={'width': '34%', 'height': '340px', 'margin-right': '4%'}),
                html.Img(src='/assets/intro.png', style={'width': '34%', 'height': '340px'})
            ], style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'})
        ])

    elif tab == 'tab-descripcion':
        return html.Div([
            html.Div([
                html.P("""
                    Este proyecto utiliza un conjunto de datos meteorológicos capturados a través de sensores instalados a diferentes alturas
                    (40 m, 60 m, 80 m y 100 m) para analizar las condiciones atmosféricas en una región costera. El objetivo principal con este conjunto de datos es identificar patrones clave y utilizar técnicas avanzadas de Machine Learning para optimizar la predicción de la energía eólica.
                """, style={'text-align': 'justify', 'margin-bottom': '20px', 'margin-top': '20px'})
            ]),
            html.Div([
                html.Div([
                    html.Img(src='/assets/desc1.png', style={'width': '180px', 'height': '180px', 'margin-bottom': '20px'}),
                    html.Img(src='/assets/desc2.png', style={'width': '180px', 'height': '180px', 'margin-bottom': '20px'})
                ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'flex-start', 'margin-right': '20px'}),
                html.Div([
                    dbc.Button('Variables Clave', id='collapse-button-1', className='mb-3', color='primary',
                               style={'background-color': '#004F6D', 'width': '250px', 'font-size': '16px', 'margin-right': '10px'}),
                    dbc.Button('Reducción de Dimensionalidad', id='collapse-button-2', className='mb-3', color='primary',
                               style={'background-color': '#004F6D', 'width': '250px', 'font-size': '16px', 'margin-right': '10px'}),
                    dbc.Button('Agrupación de los Datos', id='collapse-button-3', className='mb-3', color='primary',
                               style={'background-color': '#004F6D', 'width': '250px', 'font-size': '16px', 'margin-right': '10px'})
                ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'}),
                html.Div([
                    html.Img(src='/assets/desc3.png', style={'width': '180px', 'height': '180px', 'margin-bottom': '10px'}),
                    html.Img(src='/assets/desc4.png', style={'width': '180px', 'height': '180px', 'margin-bottom': '10px'})
                ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'flex-start', 'margin-left': '20px'})
            ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-top': '40px'}),
            dbc.Collapse(
                html.Div([
                    html.P("""
                        - Velocidad del viento (m/s), medida en cada una de las alturas.
                        - Dirección del viento (grados), correspondiente a la orientación en cada nivel.
                        - Temperatura del aire (°C), registrada a 20 m y 100 m.
                        - Presión atmosférica (hPa) y humedad relativa (%), medidas por los sensores.
                    """, style={'text-align': 'justify', 'white-space': 'pre-wrap'}),
                ], style={'background-color': '#f0f0f0', 'padding': '15px', 'border-radius': '15px', 'width': '60%', 'margin': '20px auto'}),
                id='collapse-1', is_open=False
            ),
            dbc.Collapse(
                html.Div([
                    html.P("""
                        Para evitar la colinealidad, se utilizó el Factor de Inflación de Varianza (VIF), 
                        que identifica y elimina variables altamente correlacionadas. Esto mejora la precisión y eficiencia de los modelos,
                        asegurando que solo las variables más relevantes se usen en el análisis, evitando resultados distorsionados o sobreajuste.
                    """, style={'text-align': 'justify'}),
                ], style={'background-color': '#f0f0f0', 'padding': '15px', 'border-radius': '15px', 'width': '60%', 'margin': '20px auto'}),
                id='collapse-2', is_open=False
            ),
            dbc.Collapse(
                html.Div([
                    html.P("""
                        Los datos se agruparon por la altura de los sensores (40 m, 60 m, 80 m, 100 m)
                        para un análisis más preciso de las condiciones atmosféricas en distintos niveles. 
                        Esto permite evaluar cómo varían el viento y la temperatura, lo cual es clave para la viabilidad de proyectos eólicos.
                        El agrupamiento también facilita la visualización y el análisis de patrones, mejorando la interpretación de los datos.
                    """, style={'text-align': 'justify'}),
                ], style={'background-color': '#f0f0f0', 'padding': '15px', 'border-radius': '15px', 'width': '60%', 'margin': '20px auto'}),
                id='collapse-3', is_open=False
            )
        ])

    elif tab == 'tab-diccionario':
        return html.Div([
            html.P("""
                A continuación, se presenta un diccionario de variables con una breve descripción de cada una, esto es importante para entender el significado de cada columna en el conjunto de datos.:
            """, style={'text-align': 'justify', 'margin-bottom': '20px', 'margin-top': '20px'}),
            html.Div([
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in tabla_df.columns],
                    data= tabla_df.to_dict('records'),
                    style_table={'width': '600px', 'overflowX': 'scroll'},  # Ancho fijo con scroll horizontal
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'fontFamily': 'Arial',
                        'whiteSpace': 'normal',  # Ajustar contenido de la celda
                        'height': 'auto',  # Permitir altura automática
                        'maxWidth': '300px',  # Limitar el ancho de las celdas
                        'overflow': 'hidden',  # Ocultar el desbordamiento
                        'textOverflow': 'ellipsis',  # Recortar texto largo
                        'border': '2px solid #004F6D'
                    },
                    style_header={
                        'backgroundColor': '#004F6D',  # Fondo azul oscuro
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'color': 'white',  # Cambiar el color de la letra del encabezado
                        'border': '2px solid #004F6D'  # Borde en el encabezado
                    },
                )
            ], style={'width': '600px', 'margin': '0 auto', 'padding': '20px'})  # Contenedor de ancho fijo
        ], style={'display': 'block', 'align-items': 'center', 'height': '100vh'})


# Callbacks para manejar el contenido en las pestañas
@app.callback(
    dash.dependencies.Output('tabs-eda-content', 'children'),
    [dash.dependencies.Input('tabs-eda', 'value')]
)

def tab_layout2(tab):
    if tab == 'tab-graficos':
        return html.Div([
            html.H5('Estadísticas generales del conjunto de datos', style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.describe().reset_index().columns],
                data=df.describe().reset_index().to_dict('records'),
                style_table={'width': '100%', 'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},  # Scroll vertical y horizontal
                style_cell={
                    'textAlign': 'center',
                    'padding': '4px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '50px',
                    'maxWidth': '80px',
                    'fontSize': '11px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': '#004F6D',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '1px solid black',
                    'fontSize': '12px',
                },
                style_data_conditional=[
                    {
                        'if': {'column_id': 'count'},
                        'backgroundColor': '#f0f0f0',
                        'color': 'black',
                        'fontWeight': 'bold'
                    }
                ],
                export_format='csv',
            ),
            # Gráficos de líneas de velocidades del viento
            html.H3('Gráficos de Líneas para Velocidades del Viento', style={
                'textAlign': 'center',
                'marginTop': '20px',  # Espacio en la parte superior
                'color': '#004F6D',
                'fontWeight': 'bold'
            }),
            dcc.Graph(id='wind-speed-subplots', figure=create_wind_speed_figure()),  # Aquí se añade la gráfica de velocidades del viento

            html.H3('Gráficos de dispersión polar', style={
                'textAlign': 'center',
                'marginTop': '40px',
                'color': '#004F6D',
                'fontWeight': 'bold'
            }),
            html.H5('Velocidad y dirección del viento a diferentes alturas (100m, 80m, 60m)', style={'textAlign': 'center'}),
            dcc.Graph(id='windrose-graph', figure=create_polar_scatter()),  # Llamada a la función que genera las rosas de los vientos

            html.H3('Gráficos de Temperatura a Diferentes Alturas', style={
                'textAlign': 'center',
                'marginTop': '40px',
                'color': '#004F6D',
                'fontWeight': 'bold'
            }),
            dcc.Graph(id='temperature-graphs', figure=create_temperature_figure()),  # Gráfico de temperaturas a diferentes alturas
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})  # Centrar los gráficos

    elif tab == 'tab-tablas':
        return html.Div([
            html.H3('Descomposición Estacional de Velocidades del Viento', style={'textAlign': 'center'}),
            dcc.Graph(id='seasonal-decompose-wind', figure=create_seasonal_decomposition_figure())  # Llamar a la función que genera la descomposición estacional
        ])

    elif tab == 'tab-estadisticas':
        return html.Div([
            html.H5('Datos faltantes, según rango de valores variables meteorológicas', style={'textAlign': 'center'}),
            dcc.Graph(id='missing-data-graph', figure=create_missing_data_plot()),  # Mostrar el gráfico de datos faltantes

        ])



# Callback para manejar el contenido de los modelos
@app.callback(
    dash.dependencies.Output('tabs-modelos-content', 'children'),
    [dash.dependencies.Input('tabs-modelos', 'value')]
)

def tab_layout3(tab):
    if tab == 'tab-modelo1':
        data1 = pd.DataFrame({
            'Modelo': ['Regresión K-NN', 'Regresión Lasso', 'Regresión Lineal', 'Regresión Ridge'],
            'MAPE': [5.894020, 4.030474, 4.013425, 4.013893],
            'RMSE': [1.227196, 0.851866, 0.845024, 0.846827],
            'R^2': [0.510433, 0.764100, 0.767875, 0.766883],
            'Ljung-Box p-value': ['1.169459e-22', '3.756088e-67', '1.306806e-63', '7.620692e-65'],
            'Jarque-Bera p-value': [0.000070, 0.219406, 0.248818, 0.241076]
        })
        
        return html.Div([
            # Título al principio
            html.H3('Modelo 1: Wind speed 100 metros (Sensor 1)', style={'textAlign': 'center', 'marginBottom': '15px'}), 
            
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in data1.columns],  # Columnas correctas
                data=data1.to_dict('records'),  # Convierte el DataFrame a un diccionario
                style_table={'width': '100%', 'overflowX': 'scroll'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '100px',
                    'maxWidth': '180px',
                    'fontSize': '14px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': '#004F6D',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '2px solid black'
                },
      
                export_format='csv',
            ),
            
            # Primera imagen
            html.Img(src='/assets/knn1.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Segunda imagen
            html.Img(src='/assets/lineal1.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Tercera imagen
            html.Img(src='/assets/ridge1.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Cuarta imagen
            html.Img(src='/assets/lasso1.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),
        ])
    
    elif tab == 'tab-modelo2':
        data2 = pd.DataFrame({
            'Modelo': ['Regresión K-NN', 'Regresión Lasso', 'Regresión Lineal', 'Regresión Ridge'],
            'MAPE': [5.832642, 4.015778, 3.996092, 3.996013],
            'RMSE': [1.204380, 0.837676, 0.830596, 0.832460],
            'R^2': [0.517706, 0.766688, 0.770615, 0.769584],
            'Ljung-Box p-value': ['8.404607e-23', '3.521004e-67', '1.214976e-63', '7.349954e-65'],
            'Jarque-Bera p-value': [0.000114, 0.173372, 0.198714, 0.191579]
        })
        
        return html.Div([
            # Título al principio
            html.H3('Modelo 2: Wind speed 100 metros (Sensor 2)', style={'textAlign': 'center', 'marginBottom': '15px'}),  

            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in data2.columns],  # Columnas correctas
                data=data2.to_dict('records'),  # Convierte el DataFrame a un diccionario
                style_table={'width': '100%', 'overflowX': 'scroll'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '100px',
                    'maxWidth': '180px',
                    'fontSize': '14px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': '#004F6D',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '2px solid black'
                },

                export_format='csv',
            ),
            
            # Primera imagen
            html.Img(src='/assets/knn2.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Segunda imagen
            html.Img(src='/assets/lineal2.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Tercera imagen
            html.Img(src='/assets/ridge2.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Cuarta imagen
            html.Img(src='/assets/lasso2.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),
        ])
        
    elif tab == 'tab-modelo3':
        data3 = pd.DataFrame({
            'Modelo': ['Regresión K-NN', 'Regresión Lasso', 'Regresión Lineal', 'Regresión Ridge'],
            'MAPE': [6.751773, 4.232456, 4.219102, 4.214576],
            'RMSE': [1.363591, 0.872926, 0.864644, 0.866600],
            'R^2': [0.369181, 0.741481, 0.746364, 0.745215],
            'Ljung-Box p-value': ['1.042822e-32', '5.546813e-63', '9.800919e-60', '8.855226e-61'],
            'Jarque-Bera p-value': [0.000104, 0.269785, 0.375339, 0.339695]
        })
        
        return html.Div([
            # Título al principio
            html.H3('Modelo 3: Wind speed 80 metros (Sensor 1)', style={'textAlign': 'center', 'marginBottom': '15px'}),  
        
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in data3.columns],  # Columnas correctas
                data=data3.to_dict('records'),  # Convierte el DataFrame a un diccionario
                style_table={'width': '100%', 'overflowX': 'scroll'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '100px',
                    'maxWidth': '180px',
                    'fontSize': '14px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': '#004F6D',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '2px solid black'
                },
                
                export_format='csv',
            ),
            
            # Primera imagen
            html.Img(src='/assets/knn3.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Segunda imagen
            html.Img(src='/assets/lineal3.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Tercera imagen
            html.Img(src='/assets/ridge3.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Cuarta imagen
            html.Img(src='/assets/lasso3.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),
        ])
    
    elif tab == 'tab-modelo4':
        data4 = pd.DataFrame({
            'Modelo': ['Regresión K-NN', 'Regresión Lasso', 'Regresión Lineal', 'Regresión Ridge'],
            'MAPE': [6.684306, 4.206317, 4.203377, 4.196624],
            'RMSE': [1.351586, 0.865937, 0.857570, 0.859552],
            'R^2': [0.377391, 0.744436, 0.749351, 0.748190],
            'Ljung-Box p-value': ['8.968552e-32', '4.300009e-63', '7.246420e-60', '6.662610e-61'],
            'Jarque-Bera p-value': [0.000067, 0.252943, 0.344181, 0.314146]
        })
        
        return html.Div([
            # Título al principio
            html.H3('Modelo 4: Wind speed 80 metros (Sensor 2)', style={'textAlign': 'center', 'marginBottom': '15px'}),  
            
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in data4.columns],  # Columnas correctas
                data=data4.to_dict('records'),  # Convierte el DataFrame a un diccionario
                style_table={'width': '100%', 'overflowX': 'scroll'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '100px',
                    'maxWidth': '180px',
                    'fontSize': '14px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': '#004F6D',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '2px solid black'
                },
    
                export_format='csv',
            ),
            
            # Primera imagen
            html.Img(src='/assets/knn4.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Segunda imagen
            html.Img(src='/assets/lineal4.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Tercera imagen
            html.Img(src='/assets/ridge4.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Cuarta imagen
            html.Img(src='/assets/lasso4.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),
            
        ])
    
    elif tab == 'tab-modelo5':
        data5 = pd.DataFrame({
            'Modelo': ['Regresión K-NN', 'Regresión Lasso', 'Regresión Lineal', 'Regresión Ridge'],
            'MAPE': [6.876112, 4.445645, 4.439774, 4.436869],
            'RMSE': [1.332056, 0.890595, 0.880800, 0.882914],
            'R^2': [0.349680, 0.709302, 0.715661, 0.714294],
            'Ljung-Box p-value': ['8.837886e-33', '8.780533e-59', '1.000130e-55', '1.275099e-56'],
            'Jarque-Bera p-value': ['1.308209e-08', '3.338686e-01', '4.692246e-01', '4.269807e-01']
        })
        
        return html.Div([
            # Título al principio
            html.H3('Modelo 5: Wind speed 60 metros', style={'textAlign': 'center', 'marginBottom': '15px'}),  

            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in data5.columns],  # Columnas correctas
                data=data5.to_dict('records'),  # Convierte el DataFrame a un diccionario
                style_table={'width': '100%', 'overflowX': 'scroll'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '100px',
                    'maxWidth': '180px',
                    'fontSize': '14px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': '#004F6D',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '2px solid black'
                },
   
                export_format='csv',
            ),
            
            # Primera imagen
            html.Img(src='/assets/knn5.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Segunda imagen
            html.Img(src='/assets/lineal5.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Tercera imagen
            html.Img(src='/assets/ridge5.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),

            # Cuarta imagen
            html.Img(src='/assets/lasso5.png', style={'width': '80%', 'display': 'block', 'margin': 'auto', 'padding': '20px'}),
        ])



# Callback para manejar los botones de colapso permitiendo solo uno abierto a la vez
@app.callback(
    [dash.dependencies.Output(f'collapse-{i}', 'is_open') for i in range(1, 4)],
    [dash.dependencies.Input(f'collapse-button-{i}', 'n_clicks') for i in range(1, 4)],
    [dash.dependencies.State(f'collapse-{i}', 'is_open') for i in range(1, 4)]
)
def toggle_collapse(n1, n2, n3, is_open1, is_open2, is_open3):
    # Permitir que solo una sección esté abierta a la vez
    ctx = dash.callback_context

    if not ctx.triggered:
        return [False, False, False]
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'collapse-button-1':
        return [not is_open1, False, False]
    elif button_id == 'collapse-button-2':
        return [False, not is_open2, False]
    elif button_id == 'collapse-button-3':
        return [False, False, not is_open3]

    return [False, False, False]


# Gráficos y funciones auxiliares
def create_wind_speed_figure():
    fig = make_subplots(rows=2, cols=2, subplot_titles=[
        'WindSpeed 100m (Sensor 1)', 'WindSpeed 100m (Sensor 2)',
        'WindSpeed 80m (Sensor 1)', 'WindSpeed 80m (Sensor 2)'
    ])
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['WindSpeed100m_1'], mode='lines', name='WindSpeed100m_1', line=dict(color='#1E90FF')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['WinSpeed100m_2'], mode='lines', name='WinSpeed100m_2', line=dict(color='#4682B4')), row=1, col=2)
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['WindSpeed80_1'], mode='lines', name='WindSpeed80_1', line=dict(color='#3CB371')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['WindSpeed80_2'], mode='lines', name='WindSpeed80_2', line=dict(color='#66CDAA')), row=2, col=2)
    fig.update_layout(height=800, width=1200)
    return fig

df_cleaned = df[['WindDirection100', 'WindSpeed100m_1', 'WindDirection80', 'WindSpeed80_1', 'WindDirection60m', 'WindSpeed60']]
def create_polar_scatter():
    fig = make_subplots(
        rows=2, cols=2, specs=[[{'type': 'polar'}, {'type': 'polar'}], [{'type': 'polar'}, {'type': 'polar'}]],
        subplot_titles=['Velocidad y Dirección a 100m', 'Velocidad y Dirección a 80m', 'Velocidad y Dirección a 60m']
    )
    fig.add_trace(go.Scatterpolar(r=df_cleaned['WindSpeed100m_1'], theta=df_cleaned['WindDirection100'], mode='markers', marker=dict(size=10, color=df_cleaned['WindSpeed100m_1'], colorscale='Blues', showscale=True), name='Velocidad a 100m'), row=1, col=1)
    fig.add_trace(go.Scatterpolar(r=df_cleaned['WindSpeed80_1'], theta=df_cleaned['WindDirection80'], mode='markers', marker=dict(size=10, color=df_cleaned['WindSpeed80_1'], colorscale='Blues', showscale=False), name='Velocidad a 80m'), row=1, col=2)
    fig.add_trace(go.Scatterpolar(r=df_cleaned['WindSpeed60'], theta=df_cleaned['WindDirection60m'], mode='markers', marker=dict(size=10, color=df_cleaned['WindSpeed60'], colorscale='Blues', showscale=False), name='Velocidad a 60m'), row=2, col=1)
    fig.update_layout(height=800, width=1000, polar=dict(radialaxis=dict(visible=True), angularaxis=dict(direction='clockwise')))
    return fig


def create_temperature_figure():
    fig = make_subplots(
        rows=2, cols=1, subplot_titles=['Temperatura AVG a 100 m', 'Temperatura AVG a 20 m']
    )
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Temperatura100m'], mode='lines', line=dict(color='#4682B4'), name='Temp 100m'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Temperatura21m'], mode='lines', line=dict(color='#3CB371'), name='Temp 20m'), row=2, col=1)
    fig.update_layout(height=800, width=1000, showlegend=False, title="Gráficos de Temperatura a Diferentes Alturas")
    return fig

def create_seasonal_decomposition_figure():
    from statsmodels.tsa.seasonal import seasonal_decompose

    # Definir las variables de velocidad del viento
    wind_variables = ['WindSpeed100m_1', 'WinSpeed100m_2', 'WindSpeed80_1', 'WindSpeed80_2', 'WindSpeed60']
    
    # Crear la figura con subgráficos para cada variable de velocidad del viento
    fig = make_subplots(
        rows=len(wind_variables) * 4, cols=1,  # 4 filas por variable (Datos Originales, Tendencia, Estacionalidad, Residuos)
        subplot_titles=[f'{var} - {component}' for var in wind_variables for component in ['Original', 'Tendencia', 'Estacionalidad', 'Residuos']]
    )

    row_index = 1  # Para controlar en qué fila colocar cada subgráfico

    for var in wind_variables:
        # Realizar la descomposición estacional para cada variable
        series = df[var].dropna()  # Elimina los valores faltantes
        
        decomposition = seasonal_decompose(series, model='additive', period=12)
        
        # Agregar los subgráficos para cada componente de la descomposición

        # Datos Originales
        fig.add_trace(go.Scatter(
            x=df['Fecha'],
            y=decomposition.observed,
            mode='lines',
            name=f'{var} - Serie Original'
        ), row=row_index, col=1)
        row_index += 1

        # Tendencia
        fig.add_trace(go.Scatter(
            x=df['Fecha'],
            y=decomposition.trend,
            mode='lines',
            name=f'{var} - Tendencia'
        ), row=row_index, col=1)
        row_index += 1

        # Estacionalidad
        fig.add_trace(go.Scatter(
            x=df['Fecha'],
            y=decomposition.seasonal,
            mode='lines',
            name=f'{var} - Estacionalidad'
        ), row=row_index, col=1)
        row_index += 1

        # Residuos
        fig.add_trace(go.Scatter(
            x=df['Fecha'],
            y=decomposition.resid,
            mode='lines',
            name=f'{var} - Residuos'
        ), row=row_index, col=1)
        row_index += 1

    # Ajustar el layout
    fig.update_layout(
        height=1000 * len(wind_variables),  # Ajustar la altura de la figura dependiendo del número de variables
        showlegend=False  # Ocultar la leyenda para mejorar la visualización
    )

    return fig



# Definir los rangos aceptados para cada variable
rango_velocidad_viento = (4, 30)  # m/s
rango_presion = (985, 1050)  # hPa
rango_humedad = (50, 100)  # %
rango_temperatura = (15, 45)  # °C
rango_direccion_viento = (0, 360)  # grados

# Aplicar las transformaciones para cada variable en el dataset
df['WindSpeed100m_1'] = df['WindSpeed100m_1'].apply(lambda x: x if pd.notna(x) and rango_velocidad_viento[0] <= x <= rango_velocidad_viento[1] else np.nan)
df['WinSpeed100m_2'] = df['WinSpeed100m_2'].apply(lambda x: x if pd.notna(x) and rango_velocidad_viento[0] <= x <= rango_velocidad_viento[1] else np.nan)
df['WindSpeed80_1'] = df['WindSpeed80_1'].apply(lambda x: x if pd.notna(x) and rango_velocidad_viento[0] <= x <= rango_velocidad_viento[1] else np.nan)
df['WindSpeed80_2'] = df['WindSpeed80_2'].apply(lambda x: x if pd.notna(x) and rango_velocidad_viento[0] <= x <= rango_velocidad_viento[1] else np.nan)
df['WindSpeed60'] = df['WindSpeed60'].apply(lambda x: x if pd.notna(x) and rango_velocidad_viento[0] <= x <= rango_velocidad_viento[1] else np.nan)
df['Presion'] = df['Presion'].apply(lambda x: x if pd.notna(x) and rango_presion[0] <= x <= rango_presion[1] else np.nan)
df['Humedad'] = df['Humedad'].apply(lambda x: x if pd.notna(x) and rango_humedad[0] <= x <= rango_humedad[1] else np.nan)
df['Temperatura100m'] = df['Temperatura100m'].apply(lambda x: x if pd.notna(x) and rango_temperatura[0] <= x <= rango_temperatura[1] else np.nan)
df['Temperatura21m'] = df['Temperatura21m'].apply(lambda x: x if pd.notna(x) and rango_temperatura[0] <= x <= rango_temperatura[1] else np.nan)
df['WindDirection100'] = df['WindDirection100'].apply(lambda x: x if pd.notna(x) and rango_direccion_viento[0] <= x <= rango_direccion_viento[1] else np.nan)
df['WindDirection80'] = df['WindDirection80'].apply(lambda x: x if pd.notna(x) and rango_direccion_viento[0] <= x <= rango_direccion_viento[1] else np.nan)
df['WindDirection60m'] = df['WindDirection60m'].apply(lambda x: x if pd.notna(x) and rango_direccion_viento[0] <= x <= rango_direccion_viento[1] else np.nan)

# Variables a analizar
variables_a_analizar = ['Temperatura100m', 'WinSpeed100m_2', 'WindSpeed80_2', 'Presion', 'Humedad', 'WindDirection100']
datos_seleccionados = df[variables_a_analizar]

# Calcular el porcentaje de valores faltantes
missing_percentages = (datos_seleccionados.isnull().mean() * 100).sort_values(ascending=False)

# Crear un DataFrame para el gráfico de barras apiladas
missing_data = pd.DataFrame({'Faltante': missing_percentages, 'No Faltante': 100 - missing_percentages})

# Función para crear el gráfico de valores faltantes en Plotly
def create_missing_data_plot():
    fig = go.Figure()

    # Agregar las barras de "Faltante"
    fig.add_trace(go.Bar(x=missing_data.index, y=missing_data['Faltante'], name='Faltante', marker=dict(color='#08306b')))

    # Agregar las barras de "No Faltante"
    fig.add_trace(go.Bar(x=missing_data.index, y=missing_data['No Faltante'], name='No Faltante', marker=dict(color='#c6dbef')))

    # Configurar el layout del gráfico
    fig.update_layout(
        barmode='stack',
        xaxis_title="Variables del Dataset",
        yaxis_title="Porcentaje de Valores",
        xaxis_tickangle=-90,
        height=600,
        showlegend=True,
        legend=dict(x=0.8, y=1)
    )

    return fig




# Callback para manejar las diferentes páginas
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return layout_pagina1
    elif pathname == '/eda':
        return layout_pagina2
    elif pathname == '/modelos':
        return layout_pagina3
    else:
        return 'Página no encontrada'


# Ejecución de la aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)

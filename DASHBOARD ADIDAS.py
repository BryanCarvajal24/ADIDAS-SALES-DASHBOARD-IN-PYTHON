from dash import html, dcc, Dash
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go  

# Cargar el dataset
dataset = pd.read_excel('G:/Mi unidad/UAO/INGENIERÍA DE DATOS E I.A/SEMESTRE 2/PROGRAMACIÓN/datasetadidas2.xlsx')

# Asegurar el formato de la fecha para graficar
dataset['Invoice Date'] = pd.to_datetime(dataset['Invoice Date'])

# Determinar el periodo del dataset
periodo = f"{dataset['Invoice Date'].min().date()} - {dataset['Invoice Date'].max().date()}"

# Agrupar datos para el gráfico de barras
aggregated_data = dataset.groupby('Product').agg({'Total Sales': 'sum'}).reset_index()

# Agrupar datos para la tendencia de ventas
sales_trend = dataset.groupby('Invoice Date').agg({'Total Sales': 'sum'}).reset_index()

# Agrupar datos para la nueva gráfica
units_by_region = dataset.groupby('Region').agg({'Units Sold': 'sum'}).reset_index()

# Variable ficticia para el gráfico coroplético
frecuencia_estados = [50, 60, 45, 30, 80, 40, 35, 20, 75, 55, 25, 15, 65, 50, 40, 30, 
                      25, 10, 5, 45, 70, 55, 40, 35, 25, 15, 10, 5, 85, 90, 75, 60, 45, 
                      30, 20, 15, 10, 5, 95, 85, 75, 65, 55, 45, 35, 25, 15, 10]

# Paleta de colores personalizada
paleta_azul_personalizada = ['#13294B', '#264D89', '#1A6DB2', '#1985C4', '#35A7FF']

# Inicializar la app
app = Dash(__name__)

# Diseño del tablero
app.layout = html.Div(style={'backgroundColor': 'black'}, children=[
    html.H1(f"DASHBOARD VENTAS DE ADIDAS ({periodo})", 
            style={'textAlign': 'center', 'color': 'white', 'fontSize': '40px', 'fontFamily': 'Courier New TUR'}),
    
    # Primera fila de gráficas
    html.Div([
        html.Div([
            dcc.Graph(
                id='histogram-graph',
                figure=px.histogram(dataset, x='Invoice Date', title='Distribución de Ventas por Fecha')
                .update_layout(width=800, height=400, plot_bgcolor='#1A6DB2', paper_bgcolor='black', font=dict(color='white'))
                .update_traces(marker=dict(color='#13294B'))
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(
                id='line-chart',
                figure=px.line(sales_trend, x='Invoice Date', y='Total Sales', title='Tendencia de Ventas Totales')
                .update_layout(width=800, height=400, plot_bgcolor='#1A6DB2', paper_bgcolor='black', font=dict(color='white'))
                .update_traces(line=dict(color='#264D89'))
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'center'}),
    
    # Segunda fila de gráficas
    html.Div([
        html.Div([
            dcc.Graph(
                id='bar-chart',
                figure=px.bar(
                    aggregated_data,  
                    x='Product',
                    y='Total Sales',
                    title='Ventas Totales por Producto',
                    color_discrete_sequence=['#13294B'] 
                ).update_layout(width=650, height=400, plot_bgcolor='#1A6DB2', paper_bgcolor='black', font=dict(color='white'))
            )
        ], style={'width': '36%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(
                id='3dplot',
                figure=px.scatter_3d(
                    dataset, x='Operating Margin', y='Operating Profit', z='Total Sales'
                ).update_layout(width=650, height=450, paper_bgcolor='black', font=dict(color='white'))
                .update_traces(marker=dict(color='#13294B'))
                .update_layout(scene=dict(
                    xaxis=dict(gridcolor='#1A6DB2'), 
                    yaxis=dict(gridcolor='#1A6DB2'), 
                    zaxis=dict(gridcolor='#1A6DB2')
                ))
            )
        ], style={'width': '31%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(
                id='pie-chart',
                figure=px.pie(
                    dataset, 
                    names='Region', 
                    values='Total Sales', 
                    title='Ventas Totales por Región', 
                    color_discrete_sequence=paleta_azul_personalizada
                ).update_traces(textposition='inside', textinfo='percent+label')
                .update_layout(paper_bgcolor='black', font=dict(color='white'))
            )
        ], style={'width': '33%', 'display': 'inline-block'})
    ]),
    
    # Tercera fila de gráficas
    html.Div([
        html.Div([
            dcc.Graph(
                id='map-chart',
                figure=go.Figure(data=go.Choropleth(
                    locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                               'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
                               'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                               'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                               'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
                    z=frecuencia_estados,
                    locationmode='USA-states',
                    colorscale='Blues',
                    marker_line_color='white'
                )).update_layout(
                    title='Mapa de Estados Unidos',
                    geo=dict(bgcolor='black', showframe=False, showcoastlines=False),
                    paper_bgcolor='black',
                    font=dict(color='white'),
                    width=1000, height=900
                )
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(
                id='units-region',
                figure=px.bar(
                    units_by_region, 
                    x='Region', 
                    y='Units Sold', 
                    title='Unidades Vendidas por Región',
                    color_discrete_sequence=['#1985C4']
                ).update_layout(width=800, height=400, plot_bgcolor='#1A6DB2', paper_bgcolor='black', font=dict(color='white'))
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'center'}),
])

# Ejecución de la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)

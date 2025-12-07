from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import plotly.io as pio
import pandas as pd


app = Dash("Video Game Sales")
server=app.server

pio.templates.default = 'plotly_white'
df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSNyYIn22Bai_3cR_oKjvFodaJw5uEESzcEjO9ZfwMjIHtEWVNts4rzPwsxug8-qLe5JYmRKdCEfcP3/pub?output=csv')
df['release_year'] = pd.DatetimeIndex(df['release_date']).year
df_sales_region = pd.melt(df, id_vars=['genre', 'title', 'total_sales', 'release_year', 'console'], value_vars=['na_sales', 'jp_sales', 'pal_sales', 'other_sales'], var_name='sales_region', value_name='sales')
df_sales_region['sales_region'] = df_sales_region['sales_region'].map({'na_sales':'North America', 
                                     'jp_sales':'Japan', 
                                     'pal_sales':'PAL Regions', 
                                     'other_sales':'Other Regions'})
df_sr_clean = df_sales_region.dropna().sort_values(by='sales', ascending=False)
fig_hm = px.density_heatmap(df_sr_clean, x='genre', y='sales_region', 
                            labels={'count':'Count', 'genre':'Genre', 'sales_region':'Sales Region'})

sr_dict = {
    'Total Sales':'total_sales',
    'North America':'na_sales',
    'Japan':'jp_sales',
    'PAL Regions':'pal_sales',
    'Other Regions':'other_sales'
}
sr_colordict = {
    'Total Sales':'red',
    'North America':'blue',
    'Japan':'green',
    'PAL Regions':'yellow',
    'Other Regions':'orange'
}


app.layout = html.Div(children=[
    html.H1(children='Video Game Sales Dashboard',
            style={'textAlign':'center'}),

    html.Div(children='''
        Seed Question: How do regional sales of video games differ between genres?
    ''',
            style={'textAlign':'center', 'margin-bottom':'20px'}),

    html.Div([
        html.Div([
            dcc.Dropdown(df['genre'].unique(),
                    'Action',
                    id='genre-filter'),
            html.Div([
                dcc.Graph(id='fig-pie')
            ])
        ], 
        style={'min-width':'400px'}), 
        html.Div([
            dcc.Graph(id='fig-scatter'),
        ],
        style={'min-width':'600px'}),
        html.Div([
            dcc.Graph(id='fig-one-game')
        ],
        style={'min-width':'400px'}),
        html.Div([
            dcc.Dropdown(['Sum', 'Mean', 'Median', 'Min', 'Max'], 
                        'Sum', 
                        id='groupby-attribute'),
            dcc.Checklist(
                ['Total Sales', 'North America', 'Japan', 'PAL Regions', 'Other Regions'], 
                ['Total Sales', 'North America'],
                inline = True, 
                id='sr-filter'
            ),
            dcc.Graph(id='fig-dot')
        ],
        style={'min-width':'600px'}),
        html.Div([
            dcc.Graph(id='fig-hm', figure=fig_hm)
        ])
    ],
    style={'display':'flex', 'flex-wrap':'wrap', 'justify-content':'space-around', 'align-content':'flex-start', 'align-items':'center', 'max-width':'1500px'}),
    
], 
style={'background-color':'#00deff'}),


# add functions here
@callback(
    Output('fig-pie', 'figure'),
    Output('fig-scatter', 'figure'),
    Output('fig-one-game', 'figure'),
    Input('genre-filter', 'value'),
    Input('fig-pie', 'clickData'),
    Input('fig-scatter', 'clickData')
)
def update_scatter(genre, pie_click_data, scatter_click_data):
    if pie_click_data is None:
        sales_region = 'North America'
        region_title = 'North America'
    else:
        sales_region = pie_click_data['points'][0]['customdata'][0]
        region_title = sales_region[0]
    
    df_genre = df[df['genre'] == genre]
    df_sr = df_sales_region[df_sales_region['genre'] == genre]

    if scatter_click_data is not None:
        game_title = scatter_click_data['points'][0]['customdata'][0]
    else:
        df_sorted_genre = df_genre.sort_values(by = sr_dict[region_title], ascending=False)
        game_title = df_sorted_genre['title'].iloc[0]

   
    df_game = df_sales_region[df_sales_region['title'] == game_title]
    fig_pie = px.pie(df_sr, values='sales', names='sales_region', title='Regional Sales by Genre', custom_data=['sales_region'], 
                     labels={'sales_region':'Sales Region', 'sales':'Sales'})
    fig_pie.update_traces({'name':'North America'}, selector={'name':'na_sales'})
    fig_scatter = px.scatter(df_genre, x=sr_dict[region_title], y='critic_score', color='release_year', hover_data=['title', 'release_year'], 
                             custom_data=['title'], title='Sales vs Critic Scores', 
                             labels={'critic_score':'Critic Score', 'title':'Title', 'release_year':'Release Year', 'na_sales':'North America Sales', 'jp_sales':'Japan Sales', 
                                     'pal_sales':'PAL Regions Sales', 'other_sales':'Other Regions Sales'})
    fig_scatter.update_layout(
        xaxis_title = region_title
    )
    fig_rad = px.bar_polar(df_game, r='sales', theta='sales_region', title=game_title, color='console', 
                           labels={'sales_region':'Sales Region', 'sales':'Sales', 'console':'Console'})



    return fig_pie, fig_scatter, fig_rad

    

@callback(
    Output('fig-dot', 'figure'),
    Input('groupby-attribute', 'value'),
    Input('sr-filter', 'value')
)
def update_dot(groupby_attribute, sr_filter):
    if groupby_attribute == 'Sum':
       df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].sum()
    elif groupby_attribute == 'Mean':
        df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].mean()
    elif groupby_attribute == 'Median':
       df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].median()
    elif groupby_attribute == 'Min':
        df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].min()
    else:
        df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].max()

    fig_dot = px.scatter(title="Average Sales in Each Genre")

    regions = sr_filter
    for region in regions:
        fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y=sr_dict[region], color_discrete_sequence=[sr_colordict[region]], 
                                     labels={'critic_score':'Critic Score', 'title':'Title', 'release_year':'Release Year', 'na_sales':'North America Sales', 'jp_sales':'Japan Sales', 
                                     'pal_sales':'PAL Regions Sales', 'other_sales':'Other Regions Sales', 'total_sales':'Total Sales', 'genre':'Genre'}).data[0])
    fig_dot.update_traces(marker=dict(size=10))

    return fig_dot

 




if __name__ == '__main__':
    app.run(debug=True)
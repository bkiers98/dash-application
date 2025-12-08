from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import plotly.io as pio
import pandas as pd


app = Dash("Video Game Sales")
server=app.server

pio.templates.default = 'plotly_white'
title_font_dict = dict(
    weight = 'bold'
)
df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSNyYIn22Bai_3cR_oKjvFodaJw5uEESzcEjO9ZfwMjIHtEWVNts4rzPwsxug8-qLe5JYmRKdCEfcP3/pub?output=csv')
df['release_year'] = pd.DatetimeIndex(df['release_date']).year
df_sales_region = pd.melt(df, id_vars=['genre', 'title', 'total_sales', 'release_year', 'console'], value_vars=['na_sales', 'jp_sales', 'pal_sales', 'other_sales'], var_name='sales_region', value_name='sales')
df_sales_region['sales_region'] = df_sales_region['sales_region'].map({'na_sales':'North America', 
                                     'jp_sales':'Japan', 
                                     'pal_sales':'PAL Regions', 
                                     'other_sales':'Other Regions'})
df_sr_clean = df_sales_region.dropna().sort_values(by='sales', ascending=False)
fig_hm = px.density_heatmap(df_sr_clean, x='genre', y='sales_region', 
                            labels={'genre':'Genre', 'sales_region':'Sales Region'}, 
                            title='Number of Games per Region/Genre')
fig_hm.update_traces(
    hovertemplate=
    'Genre: %{x}<br>' +
    'Region: %{y}<br>' +
    'Number of Games: %{z}'
)
fig_hm.update_layout(
    hoverlabel=dict(
        bgcolor='white'
    ), title_font = title_font_dict
)

sr_dict = {
    'Total Sales':'total_sales',
    'North America':'na_sales',
    'Japan':'jp_sales',
    'PAL Regions':'pal_sales',
    'Other Regions':'other_sales'
}
sr_colordict = {
    'Total Sales':'#007b4a',
    'North America':'#ff3939',
    'Japan':'#ffce29',
    'PAL Regions':'#00deff',
    'Other Regions':'#00ce00'
}


app.layout = html.Div(children=[
    html.H1(children='Video Game Sales Dashboard',
            style={'textAlign':'center'}),

    html.Div(children='''
        Examining the sales of video games in different genres throughout the regions of the world. 
    ''',
            style={'textAlign':'center', 'margin-bottom':'20px'}),

    html.Div(children=[
        html.H3(children='Important links:'),
        html.Ul([
            html.Li([html.A('Dataset source', href='https://mavenanalytics.io/data-playground/video-game-sales', target='_blank')]),
            html.Li([html.A('Stream video walkthrough', href='https://indiana-my.sharepoint.com/:v:/g/personal/benoet_iu_edu/EU7VqWjtM8pErVgz89BZJqEBl0htLkhdLXbe3eTjVOGLXA?e=lCEXo3&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D', target='_blank')]),
            html.Li([html.A('Github repository', href='https://github.com/bkiers98/dash-application.git', target='_blank')])
        ])
    ], 
    style={'textAlign':'left'}),

    html.Div(children=[
        html.H3(children='Key information/takeaways:'),
        html.Ul([
            html.Li(children='PAL Regions are Australia, Europe, and some other areas; PAL stands for "Phase Alternating Line"'),
            html.Li(children='Although North America consistently has the highest sales, more games are actually sold in unspecified regions (see heatmap)'),
            html.Li(children='Action, Action-Adventure, Sports, and Shooter genres have some of the highest sales; but the average sales within each genre are similar to other genres'),
            html.Li(children='Individual games may fare poorly on a single platform but sell well across all platforms')
        ])
    ]),

    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(df['genre'].unique(),
                        'Action',
                        id='genre-filter'),
                html.Div([
                    dcc.Graph(id='fig-pie')
                ])
            ], 
            style={'flex':'1 1 25%', 'min-width':'350px', 'padding':'10px', 'margin':'5px'}), 
            html.Div([
                dcc.Graph(id='fig-scatter'),
            ],
            style={'flex':'1 1 50%', 'min-width':'700px', 'padding':'10px', 'margin':'5px'}),
            html.Div([
                dcc.Graph(id='fig-one-game')
            ],
            style={'flex':'1 1 25%', 'min-width':'350px', 'padding':'10px', 'margin':'5px'})
        ], 
        style={'display':'flex', 'justify-content':'space-between', 'min-width':'1550px', 'background-color':'#DDDDDD'}),
        html.Div([
            html.Div([
                dcc.Checklist(
                    ['Total Sales', 'North America', 'Japan', 'PAL Regions', 'Other Regions'], 
                    ['Total Sales', 'North America'],
                    inline = True, 
                    id='sr-filter'
                ),
                dcc.Dropdown(['Sum', 'Mean', 'Median', 'Min', 'Max'], 
                            'Sum', 
                            id='groupby-attribute'),
                dcc.Graph(id='fig-dot')
            ],
            style={'flex':'1 1 50%', 'min-width':'700px', 'padding':'10px', 'margin':'5px'}),
            html.Div([
                dcc.Graph(id='fig-hm', figure=fig_hm)
            ], 
            style={'flex':'1 1 50%', 'min-width':'700px', 'padding':'15px', 'margin':'0px', 'background-color':"#9A9A9A"})
            ], 
            style={'display':'flex', 'justify-content':'space-between', 'align-items':'center', 'min-width':'1550px', 'background-color':"#BDBDBD"})
    ],
    style={'display':'flex', 'flex-direction':'column', 'justify-content':'space-around', 'min-width':'1600px', 'height':'1052px',
           'padding':'20px', 'margin':'10px', 'background-color':"#747474"}),
    
], 
style={'display':'flex', 'flex-direction':'column', 'padding':'20px', 'margin':'0px', 'align-items':'center'}),


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
    fig_pie = px.pie(df_sr, values='sales', names='sales_region', title='Regional Sales by Genre', custom_data=['sales_region', 'sales'], 
                     labels={'sales_region':'Sales Region', 'sales':'Sales'}, color_discrete_sequence = ['#ff3939', '#ffce29', '#00deff', '#00ce00'], hole=.3)
    fig_pie.update_traces(
        hovertemplate = 
        '%{customdata[0][0]}<br>'
    )
    fig_pie.update_layout(
        hoverlabel=dict(
            bgcolor='white'
        ), title_font = title_font_dict
    )
    fig_scatter = px.scatter(df_genre, x=sr_dict[region_title], y='critic_score', color='release_year', hover_data=['title', 'release_year'], 
                             custom_data=['title', 'release_year'], title='Sales vs Critic Scores', color_continuous_scale=px.colors.sequential.Turbo, 
                             labels={'critic_score':'Critic Score', 'title':'Title', 'release_year':'Release Year', 'na_sales':'North America Sales', 'jp_sales':'Japan Sales', 
                                     'pal_sales':'PAL Regions Sales', 'other_sales':'Other Regions Sales'})
    fig_scatter.update_traces(
        hovertemplate=
        '<b>%{customdata[0]}</b><br><br>' +
        'Critic Score: %{y:.1f}/10<br>' +
        'Sales: $%{x:.2f} million USD<br>' +
        'Year: %{customdata[1]}', 
        marker=dict(
            size=10, 
            opacity=.7
        )
    )
    fig_scatter.update_layout(
        xaxis_title = f'{region_title} Sales in million USD', 
        yaxis_title = 'Critic Score out of 10',
        hoverlabel=dict(
            bgcolor='white'
        ), title_font = title_font_dict
    )
    fig_rad = px.bar_polar(df_game, r='sales', theta='sales_region', title=game_title, color='console', 
                           custom_data=['console'], color_discrete_sequence=px.colors.qualitative.Light24, 
                           labels={'sales_region':'Sales Region', 'sales':'Sales', 'console':'Console'})
    fig_rad.update_traces(
        hovertemplate=
        'Console: %{customdata[0]}<br>' + 
        'Sales: $%{r:.2f} million USD<br>' +
        'Region: %{theta}'
    )
    fig_rad.update_layout(
        hoverlabel=dict(
            bgcolor='white'
        ), title_font = title_font_dict
    )



    return fig_pie, fig_scatter, fig_rad

    

@callback(
    Output('fig-dot', 'figure'),
    Input('groupby-attribute', 'value'),
    Input('sr-filter', 'value')
)
def update_dot(groupby_attribute, sr_filter):
    if groupby_attribute == 'Sum':
       df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].sum()
       graph_title = 'Sum of'
    elif groupby_attribute == 'Mean':
        df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].mean()
        graph_title = 'Mean of'
    elif groupby_attribute == 'Median':
       df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].median()
       graph_title = 'Median of'
    elif groupby_attribute == 'Min':
        df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].min()
        graph_title = 'Lowest'
    else:
        df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].max()
        graph_title = 'Highest'

    fig_dot = px.scatter(title=f"{graph_title} Sales in Each Genre", template='simple_white')

    regions = sr_filter
    for region in regions:
        fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y=sr_dict[region], color_discrete_sequence=[sr_colordict[region]], 
                                     labels={'critic_score':'Critic Score', 'title':'Title', 'release_year':'Release Year', 'na_sales':'North America Sales', 'jp_sales':'Japan Sales', 
                                     'pal_sales':'PAL Regions Sales', 'other_sales':'Other Regions Sales', 'total_sales':'Total Sales', 'genre':'Genre'}).data[0])
    fig_dot.update_traces(marker=dict(size=15), hovertemplate=
                          '<i>$%{y:.2f} million USD</i>')
    fig_dot.update_layout(hovermode='x unified', yaxis_title='Sales in Millions USD',
                        xaxis_title='Genre', title_font = title_font_dict)

    return fig_dot

 




if __name__ == '__main__':
    app.run(debug=True)
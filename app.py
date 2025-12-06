from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd


app = Dash("Video Game Sales")
server=app.server

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSNyYIn22Bai_3cR_oKjvFodaJw5uEESzcEjO9ZfwMjIHtEWVNts4rzPwsxug8-qLe5JYmRKdCEfcP3/pub?output=csv')
df['release_year'] = pd.DatetimeIndex(df['release_date']).year
df_sales_region = pd.melt(df, id_vars=['genre', 'total_sales'], value_vars=['na_sales', 'jp_sales', 'pal_sales', 'other_sales'], var_name='sales_region', value_name='sales')

sr_dict = {
    'Total Sales':'total_sales',
    'North America Sales':'na_sales',
    'Japan Sales':'jp_sales',
    'PAL Sales':'pal_sales',
    'Other Sales':'other_sales'
}
sr_colordict = {
    'Total Sales':'red',
    'North America Sales':'blue',
    'Japan Sales':'green',
    'PAL Sales':'yellow',
    'Other Sales':'orange'
}
#df_sr = df_sales_region[df_sales_region['genre'] == 'Action']
#df_genre = df[df['genre'] == 'Platform']
#df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].mean()

#fig_pie = px.pie(df_sr, values='sales', names='sales_region', title='Regional Sales by Genre')
#fig_scatter = px.scatter(df_genre, x='na_sales', y='critic_score', color='release_year', hover_data=['title', 'release_year'], title='Sales vs Critic Scores')

#fig_dot = px.scatter(title="Average Sales in Each Genre")
#fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y='total_sales', color_discrete_sequence=['red']).data[0])
#fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y='na_sales', color_discrete_sequence=['blue']).data[0])
#fig_dot.update_traces(marker=dict(size=10))

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
            dcc.Graph(id='fig-pie'), 
            dcc.Graph(id='fig-scatter'),
        ]),
        html.Div([
            dcc.Dropdown(['Sum', 'Mean', 'Median', 'Min', 'Max'], 
                         'Sum', 
                         id='groupby-attribute'),
            dcc.Checklist(
                ['Total Sales', 'North America Sales', 'Japan Sales', 'PAL Sales', 'Other Sales'], 
                ['Total Sales', 'North America Sales'],
                inline = True, 
                id='sr-filter'
            ),
            dcc.Graph(id='fig-dot')
        ])
        
    ]),
    

    
]),


# add functions here
@callback(
    Output('fig-pie', 'figure'),
    Output('fig-scatter', 'figure'),
    Input('genre-filter', 'value'),
    Input('fig-pie', 'clickData')
)
def update_scatter(genre, pie_click_data):
    if pie_click_data is None:
        sales_region = 'na_sales'
        region_title = 'na_sales'
    else:
        sales_region = pie_click_data['points'][0]['customdata'][0]
        region_title = sales_region[0]
    df_genre = df[df['genre'] == genre]
    df_sr = df_sales_region[df_sales_region['genre'] == genre]
    fig_pie = px.pie(df_sr, values='sales', names='sales_region', title='Regional Sales by Genre', custom_data=['sales_region'])
    fig_scatter = px.scatter(df_genre, x=sales_region, y='critic_score', color='release_year', hover_data=['title', 'release_year'], title='Sales vs Critic Scores')
    fig_scatter.update_layout(
        xaxis_title = region_title
    )

    return fig_pie, fig_scatter

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
        fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y=sr_dict[region], color_discrete_sequence=[sr_colordict[region]]).data[0])
    #fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y='total_sales', color_discrete_sequence=['red']).data[0])
    #fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y='na_sales', color_discrete_sequence=['blue']).data[0])
    fig_dot.update_traces(marker=dict(size=10))

    return fig_dot

 




if __name__ == '__main__':
    app.run(debug=True)
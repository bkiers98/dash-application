from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd


app = Dash()
server=app.server

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSNyYIn22Bai_3cR_oKjvFodaJw5uEESzcEjO9ZfwMjIHtEWVNts4rzPwsxug8-qLe5JYmRKdCEfcP3/pub?output=csv')
df['release_year'] = pd.DatetimeIndex(df['release_date']).year
df_sales_region = pd.melt(df, id_vars=['genre', 'total_sales'], value_vars=['na_sales', 'jp_sales', 'pal_sales', 'other_sales'], var_name='sales_region', value_name='sales')
df_sr = df_sales_region[df_sales_region['genre'] == 'Action']
df_genre = df[df['genre'] == 'Platform']
df_grouped = df.groupby('genre')[['total_sales', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales']].mean()

app = Dash("Video Game Sales")

fig_pie = px.pie(df_sr, values='sales', names='sales_region', title='Regional Sales by Genre')
fig_scatter = px.scatter(df_genre, x='na_sales', y='critic_score', color='release_year', hover_data=['title', 'release_year'], title='Sales vs Critic Scores')

fig_dot = px.scatter(title="Average Sales in Each Genre")
fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y='total_sales', color_discrete_sequence=['red']).data[0])
fig_dot.add_trace(px.scatter(df_grouped, x=df_grouped.index, y='na_sales', color_discrete_sequence=['blue']).data[0])
fig_dot.update_traces(marker=dict(size=10))


app.layout = html.Div(children=[
    html.H1(children='Video Game Sales Dashboard',
            style={'textAlign':'center'}),

    html.Div(children='''
        Seed Question: How do regional sales of video games differ between genres?
    ''',
             style={'textAlign':'center', 'margin-bottom':'20px'}),
    dcc.Graph(id='fig-pie', figure=fig_pie), 
    dcc.Graph(id='fig-scatter', figure=fig_scatter),
    dcc.Graph(id='fig-dog', figure=fig_dot)

    
]),


# add functions here

# DO NOT EDIT BELOW THIS LINE (except to change `jupyter_height`)

if __name__ == '__main__':
    app.run(debug=True)
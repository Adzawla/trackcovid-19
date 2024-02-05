
from logging import PlaceHolder
import dash
from dash_bootstrap_components._components import Navbar
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components import Div
from dash_html_components.Option import Option
from numpy import number
from pandas.core.indexes import base
import plotly.graph_objs as go
import pandas as pd
from functools import reduce 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_extensions import Lottie



# These are the links to the datasets. Whenever these datasets get updated, it will replicate automatically in our application.

confirmed_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"


confirmed_cases = pd.read_csv(confirmed_link)
deaths_cases = pd.read_csv(deaths_link)
recovered_cases = pd.read_csv(recovered_link)

#Let's unpivot the data
confirmed_data = confirmed_cases.melt(id_vars=["Province/State","Country/Region","Lat", "Long"],value_vars= confirmed_cases.columns[4:],var_name='Date',value_name='Total_Confirmed')
deaths_data = deaths_cases.melt(id_vars=["Province/State","Country/Region","Lat","Long"], value_vars=deaths_cases.columns[4:], var_name="Date" ,value_name="Total_deaths")
recovered_data = recovered_cases.melt(id_vars=["Province/State","Country/Region","Lat","Long"], value_vars=recovered_cases.columns[4:], var_name="Date", value_name="Total_recovered")

# Let's merge all the 3 datasets
all_data = [confirmed_data,deaths_data ,recovered_data]
all_data = reduce(lambda left, right:pd.merge(left, right, on=["Province/State","Country/Region","Date","Lat","Long"], how="left"),all_data)

#Converting date to it proper format
all_data["Date"]=pd.to_datetime(all_data["Date"])

# Checking the missing values and Replacing all the NA with zero
all_data.isna().sum()
all_data["Total_recovered"] = all_data["Total_recovered"].fillna(0)

# Creating a new variable Active
all_data["Active"] = all_data["Total_Confirmed"] - all_data["Total_deaths"]- all_data["Total_recovered"]

# 
all_data_grouped = all_data.groupby(['Date'])[['Total_Confirmed','Total_deaths','Total_recovered', 'Active']].sum().reset_index()

# Dictionary of list

all_data_list = all_data[['Country/Region','Lat','Long' ]]
dic_of_location = all_data_list.set_index(['Country/Region'])[['Lat', 'Long']].T.to_dict('dict')

# Some links
url1="https://assets2.lottiefiles.com/packages/lf20_0djafiny.json"  
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_coonections = "https://assets9.lottiefiles.com/private_files/lf30_5ttqPi.json"
url_companies = "https://assets9.lottiefiles.com/packages/lf20_EzPrWM.json"
url_msg_in = "https://assets9.lottiefiles.com/packages/lf20_8wREpI.json"
url_msg_out = "https://assets2.lottiefiles.com/packages/lf20_Cc8Bpg.json"
url_reactions = "https://assets2.lottiefiles.com/packages/lf20_nKwET0.json"

lottie_banner = 'https://assets7.lottiefiles.com/private_files/lf30_1lysabyy.json'

lottie_cases = 'https://assets1.lottiefiles.com/packages/lf20_dkljlzky.json'
lottie_death = 'https://assets7.lottiefiles.com/temp/lf20_euwjhc.json'
lottie_recovered = 'https://assets4.lottiefiles.com/packages/lf20_rvqq1X.json'
lottie_active = 'https://assets8.lottiefiles.com/packages/lf20_trqlqcx6.json'


# Setting the app

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server=app.server

#app= dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

colors = {
    'background': '#192444',
    'text': '#7FDBFF'
}

#style={'backgroundColor': colors['background']}, children=
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dbc.Navbar(style={'backgroundColor':'#0e1035'},children=[ 

        html.Div(
            children=[
                html.P(Lottie(options=options, width="12%", height="12%", url=url1, speed=4)),
                html.H1(
                    children="COVID-19 TRACKER", className="header-title", style={'textAlign':'center', 'color':'white'}
                ),

                html.Blockquote([ 
                  html.P("For those who lost their loved ones, may the Almighty comforter comfort you."),
                  html.P(
                    (html.Small("Designed by : KUDZO VENUNYE ADZAWLA",style={'textAlign':'center', 'color':'white'})))
                ], className="header-description", style={'color':'yellow'}),

            ])
    ],className="header"),

    html.Div( 
        dbc.Row(html.Marquee('Last updated : ' + str(all_data['Date'].iloc[-1].strftime('%B %d, %Y') + ' 00:00 (GMT)'), style={'color':'orange', 'fontSize':'20px', 'fontFamily':'Times new roman', 'align':'center'}, className='mb-2 mt-2')),
    ),
dbc.Row([ 
    dbc.Row([

        # col1 of R2    
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=lottie_active, speed=3)),
                dbc.CardBody([
                    html.H6('GLOBAL CASES',style={'textAlign':'center','color':'white'}, className='font-weight-bolder'),
                    html.P(f"{all_data_grouped['Total_Confirmed'].iloc[-1]:,.0f}", style={"textAlign":"center","color":"orange",'fontSize':20}),
                    html.P("New cases:" + f"{all_data_grouped['Total_Confirmed'].iloc[-1] - all_data_grouped['Total_Confirmed'].iloc[-2]: ,.0f}", style={'color':'white'}),
                    html.P('(' + str(round(((all_data_grouped['Total_Confirmed'].iloc[-1] - all_data_grouped['Total_Confirmed'].iloc[-2])/all_data_grouped['Total_Confirmed'].iloc[-1])*100,2)) + '%)', style={'color':'#f2aa4cff'})
                ], className='font-weight-bolder', style={'textAlign':'center'})
            ], color='#34495E'), #color="#34495E" #E59866
        ], width={'size':3, 'offset':3}, className='card_container three columns'),

        # col2 of R2 

        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="27%", height="27%", url=lottie_death)),
                dbc.CardBody([
                    html.H6('GLOBAL DEATH',style={'textAlign':'center','color':'white'}, className='font-weight-bolder'),
                    html.P(f"{all_data_grouped['Total_deaths'].iloc[-1]:,.0f}", style={"textAlign":"center","color":"orange",'fontSize':20}),                           
                    html.P('New cases : ' + f"{all_data_grouped['Total_deaths'].iloc[-1] - all_data_grouped['Total_deaths'].iloc[-2]: ,.0f}", style={'color':'white'}),
                            html.P('(' + str(round(((all_data_grouped['Total_deaths'].iloc[-1] - all_data_grouped['Total_deaths'].iloc[-2])/all_data_grouped['Total_deaths'].iloc[-1])*100,2)) + '%)', style={'color':'#f2aa4cff'})
                ],className='font-weight-bolder', style={'textAlign':'center'})
            ], color='#990000'),
        ], width=3, className='card_container three columns'),

        # col3 of R2 

        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="27%", height="27%", url=lottie_cases)),
                dbc.CardBody([
                    html.H6('RECOVERED',style={'textAlign':'center','color':'white'}, className='font-weight-bolder'),
                    html.P(f"{all_data_grouped['Total_recovered'].iloc[-1]:,.0f}", style={"textAlign":"center","color":"orange",'fontSize':20}),
                    html.P('New cases : ' + f"{all_data_grouped['Total_recovered'].iloc[-1] - all_data_grouped['Total_recovered'].iloc[-2]: ,.0f}", style={'color':'white'}),
                    html.P('(' + str(round(((all_data_grouped['Total_recovered'].iloc[-1] - all_data_grouped['Total_recovered'].iloc[-2])/all_data_grouped['Total_recovered'].iloc[-1])*100,2)) + '%)', style={'color':'#f2aa4cff'})
                ], className='font-weight-bolder', style={'textAlign': 'center'})
            ], color='#008080'),
        ], width=3, className='card_container three columns'),

        # col4 of R2

        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="27%", height="27%", url=lottie_recovered)),
                dbc.CardBody([
                    html.H6(children='TOTAL ACTIVE', style={'textAlign':'center','color':'white'}, className='font-weight-bolder'),
                    html.P(f"{all_data_grouped['Active'].iloc[-1]:,.0f}", style={"textAlign":"center","color":'orange','fontSize':20}),
                    html.P('New cases : ' + f"{all_data_grouped['Active'].iloc[-1] - all_data_grouped['Active'].iloc[-2]: ,.0f}", style={'color':'white'}),
                    html.P('(' + str(round(((all_data_grouped['Active'].iloc[-1] - all_data_grouped['Active'].iloc[-2])/all_data_grouped['Active'].iloc[-1])*100,2)) + '%)', style={'color':'#f2aa4cff'})
                ], className='font-weight-bolder', style={'textAlign':'center'})
            ], color="#34495E"),
        ], width=3, className='card_container three columns'),    
], no_gutters=True, justify='center'),



html.Div([
      html.P('Select country:', className='fix-label', style={'color':'white'}),
      dcc.Dropdown(id='w_countries',
      multi=False,
      searchable=True,
      value='Senegal',
      placeholder="Select country",
      options=[{'label': c, 'value': c}
      for c in (all_data["Country/Region"].unique())], className='dcc_compon'),

    html.P('New Cases : ' +  ' ' + str(all_data['Date'].iloc[-1].strftime('%B %d, %Y')),
    className='fix_label', style={'text-align':'center', 'color':'white'}),
    dcc.Graph(id='confirmed', config={'displayModeBar':False}, className='dcc_compon'),

    dcc.Graph(id='death', config={'displayModeBar':False}, className='dcc_compon'),

    dcc.Graph(id='recovered', config={'displayModeBar':False}, className='dcc_compon'),

    dcc.Graph(id='active', config={'displayModeBar':False}, className='dcc_compon'),
    ], className='create_container three columns'),
   
   # The pie graph

    html.Div([
    dcc.Graph(id='pie_chart', config={'displayModeBar':'hover'})
  ], className='create_container four columns'),

  # This where the line graph lies
  html.Div([
    dcc.Graph(id='line_chart', config={'displayModeBar':'hover'})
    ], className='create_container five columns'),

      # This where the map graph lies
  html.Div([
    dcc.Graph(id='map_chart', config={'displayModeBar':'hover'})
              ], className='create_container1 twelves columns')

    ], className='mb-2'),

    ])


@app.callback(Output('confirmed', 'figure'),
              [Input('w_countries', 'value')])

def update_confirmed(w_countries):
  all_data_grouped02 = all_data.groupby(['Date', 'Country/Region'])[['Total_Confirmed','Total_deaths','Total_recovered', 'Active']].sum().reset_index()
  conf_cases = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_Confirmed'].iloc[-1] - all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_Confirmed'].iloc[-2]
  conf_delta = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_Confirmed'].iloc[-2] - all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_Confirmed'].iloc[-3]

  return {
    'data':[go.Indicator(
      mode='number+delta',
      value=conf_cases,
      delta={'reference': conf_delta,
        'position':'right',
        'valueformat':' ,g',
        'relative':False,
        'font':{'size':15}},
      number={'valueformat':' ',
              'font':{'size':20}},
              
      domain={'y': [0, 1], 'x': [0, 1]}
    )],
    'layout':go.Layout(
      title={'text': 'New Confirmeds',
      'y':1,
      'x':0.5,
      'xanchor':'center',
      'yanchor':'top'},
      font=dict(color = 'orange'),
      paper_bgcolor='#1f2c56',
      plot_bgcolor='#1f2c56',
      height = 85,
    ) 

 }

 
@app.callback(Output('death', 'figure'),
              [Input('w_countries', 'value')])

def update_confirmed(w_countries):
  all_data_grouped02 = all_data.groupby(['Date', 'Country/Region'])[['Total_Confirmed','Total_deaths','Total_recovered', 'Active']].sum().reset_index()
  death_cases = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_deaths'].iloc[-1] - all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_deaths'].iloc[-2]
  death_delta = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_deaths'].iloc[-2] - all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_deaths'].iloc[-3]

  return {
    'data':[go.Indicator(
      mode='number+delta',
      value=death_cases,
      delta={'reference': death_delta,
        'position':'right',
        'valueformat':' ,g',
        'relative':False,
        'font':{'size':15}},
      number={'valueformat':' ',
              'font':{'size':20}},
              
      domain={'y': [0, 1], 'x': [0, 1]}
    )],
    'layout':go.Layout(
      title={'text': 'New Deaths',
      'y':1,
      'x':0.5,
      'xanchor':'center',
      'yanchor':'top'},
      font=dict(color = 'orange'),
      paper_bgcolor='#1f2c56',
      plot_bgcolor='#1f2c56',
      height = 85,
    ) 

 }
 
@app.callback(Output('recovered', 'figure'),
              [Input('w_countries', 'value')])

def update_confirmed(w_countries):
  all_data_grouped02 = all_data.groupby(['Date', 'Country/Region'])[['Total_Confirmed','Total_deaths','Total_recovered', 'Active']].sum().reset_index()
  recovered_cases = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_recovered'].iloc[-1] - all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_recovered'].iloc[-2]
  recovered_delta = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_recovered'].iloc[-2] - all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_recovered'].iloc[-3]

  return {
    'data':[go.Indicator(
      mode='number+delta',
      value=recovered_cases,
      delta={'reference': recovered_delta,
        'position':'right',
        'valueformat':' ,g',
        'relative':False,
        'font':{'size':15}},
      number={'valueformat':' ',
              'font':{'size':20}},
              
      domain={'y': [0, 1], 'x': [0, 1]}
    )],
    'layout':go.Layout(
      title={'text': 'New Recovered',
      'y':1,
      'x':0.5,
      'xanchor':'center',
      'yanchor':'top'},
      font=dict(color = 'orange'),
      paper_bgcolor='#1f2c56',
      plot_bgcolor='#1f2c56',
      height = 85,
    ) 

 }

@app.callback(Output('active', 'figure'),
              [Input('w_countries', 'value')])

def update_confirmed(w_countries):
  all_data_grouped02 = all_data.groupby(['Date', 'Country/Region'])[['Total_Confirmed','Total_deaths','Total_recovered', 'Active']].sum().reset_index()
  active_cases = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Active'].iloc[-1] - all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Active'].iloc[-2]
  active_delta = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Active'].iloc[-2] - all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Active'].iloc[-3]

  return {
    'data':[go.Indicator(
      mode='number+delta',
      value=active_cases,
      delta={'reference': active_delta,
        'position':'right',
        'valueformat':' ,g',
        'relative':False,
        'font':{'size':15}},
      number={'valueformat':' ',
              'font':{'size':20}},
              
      domain={'y': [0, 1], 'x': [0, 1]}
    )],
    'layout':go.Layout(
      title={'text': 'New Active',
      'y':1,
      'x':0.5,
      'xanchor':'center',
      'yanchor':'top'},
      font=dict(color = 'orange'),
      paper_bgcolor='#1f2c56',
      plot_bgcolor='#1f2c56',
      height = 85,
    ) 

 }      

# Pie Graph
@app.callback(Output('pie_chart', 'figure'),
              [Input('w_countries', 'value')])

def update_pie(w_countries):
  all_data_grouped02 = all_data.groupby(['Date', 'Country/Region'])[['Total_Confirmed','Total_deaths','Total_recovered', 'Active']].sum().reset_index()
  confirmed_value = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_Confirmed'].iloc[-1]
  death_value= all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_deaths'].iloc[-1]
  recorvered_value = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Total_recovered'].iloc[-1]
  active_value = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries]['Active'].iloc[-1]
  colors=["orange", "pink", "red", "purple"]

  return {
    'data': [go.Pie(
      labels=['Confirmed', 'Death', 'Recovered', 'Active'],
      values=[confirmed_value, death_value, recorvered_value, active_value],
      marker=dict(colors=colors),
      hoverinfo='label+value+percent',
      textinfo='label+value',
      hole=.7,
      rotation=45,
      insidetextorientation='radial'

    )],
    'layout':go.Layout(
      title={'text': 'Total cases - ' + (w_countries),
      'y':0.9,
      'x':0.5, #0.1
      'xanchor':'center',
      'yanchor':'top'},
      titlefont={"color":"white",
              "size":20},
      font=dict(family='sans-serif',
                color='white',
                size=12),
      hovermode='closest',
      paper_bgcolor='#1f2c56',
      plot_bgcolor='#1f2c56',
      legend={'orientation':'h',
      'bgcolor':'#1f2c56',
      'xanchor':'center', 'x':0.5, 'y': -0.2}
    ) 

 }

# Here lies the callback for the line graph

@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries', 'value')])

def update_line_chart(w_countries):
    all_data_grouped02 = all_data.groupby(['Date', 'Country/Region'])[['Total_Confirmed','Total_deaths','Total_recovered', 'Active']].sum().reset_index()
    all_data_grouped03 = all_data_grouped02[all_data_grouped02['Country/Region']==w_countries][['Country/Region', 'Date', 'Total_Confirmed']].reset_index()
    all_data_grouped03["Daily_confirmed"] = all_data_grouped03['Total_Confirmed'] - all_data_grouped03['Total_Confirmed'].shift(1)
    all_data_grouped03['Rolling Ave.'] = all_data_grouped03['Daily_confirmed'].rolling(window=7).mean()
    
    return{
    'data': [go.Bar(
      x=all_data_grouped03["Date"].tail(30),
      y=all_data_grouped03["Rolling Ave."].tail(30),
      name='Daily Confirmed Cases',
      marker=dict(color="orange"),
      hoverinfo='text',
      hovertext=
    '<b>Date</b>: ' + all_data_grouped03["Date"].tail(30).astype(str) + '<br>' +  
    '<b>Daily Confirmed Cases </b>: ' + [f'{x:,.0f}' for x in all_data_grouped03["Rolling Ave."].tail(30)] + '<br>' +
    '<b>Country</b>: ' + all_data_grouped03["Country/Region"].tail(30).astype(str) + '<br>'

    ),
    go.Bar(
      x=all_data_grouped03["Date"].tail(30),
      y=all_data_grouped03["Rolling Ave."].tail(30),
      #mode='lines',
      name='Rolling average of the last 7 days - Daily confirmed cases',
      #line=dict(width=3, color="#FF00FF"),
      hoverinfo='text',
      hovertext=
    '<b>Date</b>: ' + all_data_grouped03["Date"].tail(30).astype(str) + '<br>' +  
    '<b>Daily Confirmed Cases </b>: ' + [f'{x:,.0f}' for x in all_data_grouped03["Rolling Ave."].tail(30)] + '<br>'

    )],
    'layout': go.Layout(
            title={'text': 'Last 30 Days Daily Confirmed Cases: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.5},
            #margin=dict(r=0),
            xaxis=dict(title='<b>Date</b>',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Daily Confirmed Cases</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )
            ))
    }

@app.callback(Output('map_chart', 'figure'),
              [Input('w_countries', 'value')])

def update_map_chart(w_countries):
  all_data_map = all_data.groupby(['Lat', 'Long', 'Country/Region'])[['Total_Confirmed','Total_deaths','Total_recovered', 'Active']].sum().reset_index()
  all_data_map_04 = all_data_map[all_data_map['Country/Region']==w_countries]


  if w_countries:
    zoom=2
    zoom_lat = dic_of_location[w_countries]['Lat']
    zoom_long = dic_of_location[w_countries]['Long']

  return{
      'data': [go.Scattermapbox(
        lon=all_data_map_04['Long'],
        lat=all_data_map_04['Lat'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=all_data_map_04['Total_Confirmed'],
                                       colorscale='HSV',
                                       showscale=False,
                                       sizemode='area',
                                       opacity=0.3),
        hoverinfo='text',
        hovertext=
        '<b>Country</b>: ' + all_data_map_04["Country/Region"].astype(str) + '<br>' + 
        '<b>Longitude</b>: ' + all_data_map_04["Long"].astype(str) + '<br>' + 
        '<b>Confirmed Cases </b>: ' + [f'{x:,.0f}' for x in all_data_map_04["Total_Confirmed"]] + '<br>' +
        '<b>Death Cases </b>: ' + [f'{x:,.0f}' for x in all_data_map_04["Total_deaths"]] + '<br>' +
        '<b>Recovered Cases </b>: ' + [f'{x:,.0f}' for x in all_data_map_04["Total_recovered"]] + '<br>' +
        '<b>Active Cases </b>: ' + [f'{x:,.0f}' for x in all_data_map_04["Active"]] + '<br>'
      )],
      'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            #margin=dict(r=0),
            margin=dict(r=0, l =0, b = 0, t = 0),
            mapbox=dict(
              accesstoken='pk.eyJ1Ijoia3Vkem8iLCJhIjoiY2t0MDJpY2wyMDR5MjJ1cDlzb29yYzY4aCJ9.oP8LBW2pdaRvHWe_pepZjg',
              center = go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
              style='dark',
              zoom=zoom,
            ),
            autosize=True
      )
} 



if __name__ == '__main__':
  app.run_server(debug=True)
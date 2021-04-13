import requests
from pandas import DataFrame as df
import plotly.graph_objs as go

r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations')

r = df(r.json()['locations'])

lon = []

lat = []
for x in r['coordinates']:
    lon.append(x['longitude'])
    lat.append(x['latitude'])

r['lat'] = df(lat)
r['lon'] = df(lon)

confirmed = []
confirmed_size = []
deaths = []
deaths_size = []
recovered = []
recovered_size = []

for x in r['latest']:
    confirmed.append(x['confirmed'])
    confirmed_size.append(int(x['confirmed']) / 500)
    deaths.append(x['deaths'])
    deaths_size.append(int(x['deaths']) / 500)
    recovered.append(x['recovered'])
    recovered_size.append(int(x['recovered']) / 500)

r['confirmed'] = df(confirmed)
r['confirmed_size'] = df(confirmed_size)
r['deaths'] = df(deaths)
r['deaths_size'] = df(deaths_size)
r['recovered'] = df(recovered)
r['recovered_size'] = df(recovered_size)

""" PLOTLY GRAPHS """

map_confirmed = go.Scattermapbox(
    customdata=r.loc[:, ['confirmed', 'deaths', 'recovered']],
    name='Confirmed Cases',
    lon=r['lon'],
    lat=r['lat'],
    text=r['country'],
    hovertemplate="<b>%{text}</b><br><br>" +
    "Confirmed: %{customdata[0]}<br" +
    "<extra></extra>",
    mode='markers',
    showlegend=True,
    marker=go.scattermapbox.marker(
        size=r['confirmed_size']
        color='yellow',
        opacity=0.7

    )
)

map_deaths = go.Scattermapbox(
    name='Deaths',
    customdata=r.loc[:, ['confirmed', 'deaths', 'recovered']],
    lon=r['lon'],
    lat=r['lat'],
    text=r['country'],
    hovertemplate="<b>%{text}</b><br><br>" +
    "Confirmed: %{customdata[1]}<br" +
    "<extra></extra>",
    mode='markers',
    showlegend=True,
    marker=go.scattermapbox.marker(
        size=r['deaths_size']
        color='black',
        opacity=0.7
)

map_recovered=go.Scattermapbox(
    name='Recovered Cases',
    customdata=r.loc[:, ['confirmed', 'deaths', 'recovered']],
    lon=r['lon'],
    lat=r['lat'],
    text=r['country'],
    hovertemplate="<b>%{text}</b><br><br>" +
    "Confirmed: %{customdata[2]}<br" +
    "<extra></extra>",
    mode='markers',
    showlegend=True,
    marker=go.scattermapbox.marker(
        size=r['recovered_size']
        color='green',
        opacity=0.7
)

layout=go.Layout(
    mapbox_style='white-bg',
    autosize=True,
    mapbox_layers=[
        {
            'below': 'traces',
            'sourcetype': 'raster',
            'source': [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
    ]
)

data=[map_confirmed, map_deaths, map_recovered]
fig=go.Figure(data=data, layout=layout)
fig.show()

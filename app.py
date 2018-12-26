#!/usr/bin/env python

"""This python file provides a web-based interface. Using the functions in
analysis.py file, it presents graphics of the data analyzed for you on the web.
It allows you to dynamically update your charts by making several different choices.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import analysis as anlys
import plotly.graph_objs as go

__author__ = "Fatih Celik"

__license__ = "ALv2"
__version__ = "1.0.2"
__maintainer__ = "Fatih Celik"
__status__ = "Prototype"

app = dash.Dash(__name__)

# import files
file0 = "oddautodata/MODELDOKUMUARALIK2004.xls"
file1 = "oddautodata/MODELDOKUMUARALIK2005.xls"
file2 = "oddautodata/Model Dökümü, Aralık 2006.xls"
file3 = "oddautodata/MODELDOKUMARALIK2007.xls"
file4 = "oddautodata/MODELDOKUMUARALIK2008.xls"
file5 = "oddautodata/MODELDOKUMUARALIK2009.xls"
file6 = "oddautodata/MODELDOKUMUARALIK2010.xls"
file7 = "oddautodata/MODELDOKUMUARALIK2011.xls"
file8 = "oddautodata/MODELDOKUMARALIK2012.xls"
file9 = "oddautodata/MODELDOKUMUARALIK2013.xls"
file10 = "oddautodata/MODELDOKUMUARALIK2014.xls"
file11 = "oddautodata/MODELDOKUMARALIK2015.xls"
file12 = "oddautodata/Model Dokumu Aralık'2016.xls"
file13 = "oddautodata/Model Dokumu Aralık 2017.xlsx"
file14 = "oddautodata/Model Dokumu Kasım'2018.xlsx"

# read files
data04, dataAll = anlys.readFiles(file0, file1, file2, file3, file4, file5,
                                  file6, file7, file8, file9, file10, file11,
                                  file12, file13, file14)

editDataList = []

#  editing dataframe
editDataList.append(anlys.editingExcel(data04))

for i in range(0, len(dataAll)):
    editDataList.append(anlys.editingExcel(dataAll[i]))

# total sales by brand
totalSalesBrands = anlys.totalSalesByBrand(editDataList[0], editDataList[1], editDataList[2], editDataList[3],
                                           editDataList[4],
                                           editDataList[5], editDataList[6], editDataList[7], editDataList[8],
                                           editDataList[9],
                                           editDataList[10], editDataList[11], editDataList[12], editDataList[13],
                                           editDataList[14])

# appended data
appendData = anlys.appendDataByYear(totalSalesBrands)

# date index range
appendData = anlys.dateRange(appendData, len(appendData))

pieData = anlys.drawPieChart(appendData)

total = anlys.drawTableForTotalSales(appendData)


#  draw scatter & pie chart with dataframe
#  @return a value that creates a scatter & pie chart using data for the web interface
def drawChart():
    return html.Div(
        children=[

            # scatter-chart div
            html.Div(
                dcc.Graph(
                    id='scatter-chart',

                    figure={
                        "data": [
                            go.Scatter(x=appendData.index, y=appendData.alfaromeo, name='alfaromeo')
                        ],

                        'layout': {
                            'title': 'alfaromeo SALES'
                        }
                    },
                ),

                #  scatter-chart style
                style={
                    'float': 'left',
                    'display': 'inline-block'
                }
            ),

            #  pie chart div
            html.Div(
                dcc.Graph(
                    id='pie-chart',

                    figure={
                        "data": [
                            #  go.Pie(labels=appendData.index, values=appendData.alfaromeo)
                        ],

                        'layout': {
                        }
                    },
                ),

                # pie chart style
                style={
                    'float': 'left',
                    'display': 'inline-block'
                }
            ),

        ],
    )


# main Layout
app.layout = html.Div([
    # title
    html.Div([
        html.H2('Automobile Explorer (ODD - Market / Model Documents)',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '1.65em',
                       'margin-left': '20',
                       'font-weight': 'bolder',
                       'font-family': 'Courier New',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '26',
                       'margin-bottom': '0'
                       }),
        #  company Logo
        html.Img(src="https://s3.eu-central-1.amazonaws.com/b2metric.com/B2M_logo_vertical.png",
                 style={
                     'margin-top': '15px',
                     'margin-right': '20',
                     'height': '60px',
                     'float': 'right'
                 },
                 ),
    ]),

    # select fields
    dcc.Dropdown(
        id='selectBrand',
        options=[
            {'label': name.upper(), 'value': name}
            for name in appendData.columns],
        value='volkswagen',
        placeholder='Select Brand',
        style={
            'marginLeft': '185',
            'marginTop': '50',
            'float': 'left',
            'width': '200px',
        }
    ),

    dcc.Dropdown(
        id='selectStartDate',
        options=[
            {'label': name, 'value': name}
            for name in appendData.index],
        value='2017-11-01',
        placeholder='Select Start Date',
        style={
            'marginTop': '50',
            'width': '200px',
            'float': 'left',
            'marginLeft': '105'
        }
    ),

    dcc.Dropdown(
        id='selectEndDate',
        options=[
            {'label': name, 'value': name}
            for name in appendData.index],
        value='2018-11-01',
        placeholder='Select End Date',
        style={
            'marginTop': '50',
            'float': 'left',
            'width': '200px',
            'marginLeft': '70'
        }
    ),

    # web interface chart div
    html.Div(
        drawChart()
    ),
], className="container")

# callback excepitons
app.config.supress_callback_exceptions = True


# callback functions for selected values in dropdowns
@app.callback(
    dash.dependencies.Output(component_id='scatter-chart', component_property='figure'),
    [dash.dependencies.Input(component_id='selectBrand', component_property='value'),
     dash.dependencies.Input(component_id='selectStartDate', component_property='value'),
     dash.dependencies.Input(component_id='selectEndDate', component_property='value')])
# update scatter-chart with start date, end date and selected brand
def updateScatterChart(brand, startDate, endDate):
    for b in appendData.columns:

        if brand == b:

            # sales within the desired range of the brand if there is a start and end date
            if startDate != None and endDate != None:

                total = anlys.drawTableForTotalSales(appendData, brand, startDate, endDate)
                data = anlys.specificRangeSalesByBrand(appendData, startDate, endDate, brand)
                pieData = anlys.drawPieChart(appendData, startDate, endDate)
                return {
                    "data": [
                        go.Scatter(x=data.index, y=data[brand], name=brand)
                    ],

                    'layout': {
                        'title': brand[0].upper() + brand[1:] + ' Sales (Total Sales: ' + str(total) + ')'
                    }
                }

            # all sales of the brand if there is no start and end date
            else:

                total = anlys.drawTableForTotalSales(appendData, brand)
                return {
                    "data": [
                        go.Scatter(x=appendData.index, y=appendData[brand], name=brand)
                    ],

                    'layout': {
                        'title': brand[0].upper() + brand[1:] + ' Sales (Total Sales: ' + str(total) + ')',
                    }
                }


@app.callback(
    dash.dependencies.Output(component_id='pie-chart', component_property='figure'),
    [dash.dependencies.Input(component_id='selectStartDate', component_property='value'),
     dash.dependencies.Input(component_id='selectEndDate', component_property='value')])
# update scatter-chart with start date and end date
def updatePieChart(startDate, endDate):
    # sales in the selected date range
    if startDate != None and endDate != None:
        pieData = anlys.drawPieChart(appendData, startDate, endDate)
        return {
            "data": [
                pieData
            ],

            'layout': {
                'title': 'Sales shares of brands between ' + startDate + ' & ' + endDate
            }
        }

    # if there is no start and end date, all sales
    else:
        pieData = anlys.drawPieChart(appendData)
        return {
            "data": [
                pieData
            ],
            'layout': {
                'title': 'Sales shares of brands between 10-1-2017 & 10-1-2018'
            },

        }


# main
if __name__ == '__main__':
    app.run_server(debug=True)

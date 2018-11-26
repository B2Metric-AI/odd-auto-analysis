#!/usr/bin/env python

"""analysis.py: This python file allows you to read some excel based files,
edit different types, analyze different data and visualize these data.
"""

import pandas as pd
import numpy as np
import plotly.graph_objs as go

__author__ = "Fatih Celik"

__license__ = "ALv2"
__version__ = "1.0.1"
__maintainer__ = "Fatih Celik"
__status__ = "Prototype"


def main():
    print()


# read excel data files
# @param file or more file
# @return one dataframe or more dataframe
def readFiles(file, *files):

    # read data
    data = pd.read_excel(file)

    # check *args
    if files is None:
        return data

    else:

        dataList = []

        for path in files:
            dataList.append(pd.read_excel(path))

        return data, dataList

# to be use editing dataframe
# @param dataframe
# @return edited dataframe
def editingExcel(dataFrame):

    # 2018 data does not include the whole year
    if len(dataFrame.columns) == 15:

        # new column names list
        replaceColumnList = ['Brand', 'Category', 'Model', 'Segment', 'January', 'February', 'March',
                         'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Total']

        # replace column names
        dataFrame.columns = replaceColumnList

        # drop unnecessary row
        dataFrame.drop(dataFrame.index[:2], inplace=True)

        # transactions to keep only total sales of brands in dataframe
        df = dataFrame.loc[:, : 'Brand']

        indexNumber = 0

        for value, row in df.iterrows():
            if row.Brand == 'TOPLAM':
                indexNumber = value
            elif row.Brand == 'Toplam/Total Pazar/Total Market':
                indexNumber = value
            elif row.Brand == 'Toplam Pazar/Total Market':
                indexNumber = value
            elif row.Brand == 'Toplam PazarTotal Market':
                indexNumber = value

        # drop unnecessary row
        indexNumber = np.asscalar(np.int16(indexNumber))
        newDataFrame = dataFrame.loc[:(indexNumber - 1)]

    # for all years except 2018
    else:

        if len(dataFrame.columns) > 17:
            dataFrame.drop(['Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19'], axis = 1, inplace = True)
        # replace to column names
        replaceColumnList = ['Brand', 'Category', 'Model', 'Segment', 'January', 'February', 'March',
                             'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
                             'December', 'Total']

        dataFrame.columns = replaceColumnList

        # drop unnecessary row
        dataFrame.drop(dataFrame.index[:2], inplace=True)

        # transactions to keep only total sales of brands in dataframe
        df = dataFrame.loc[:, : 'Brand']

        indexNumber = 0

        for value, row in df.iterrows():
            if row.Brand == 'TOPLAM':
                indexNumber = value
            elif row.Brand == 'Toplam/Total Pazar/Total Market':
                indexNumber = value
            elif row.Brand == 'Toplam Pazar/Total Market':
                indexNumber = value
            elif row.Brand == 'Toplam PazarTotal Market':
                indexNumber = value
            # convert type int from int64
            indexNumber = np.asscalar(np.int16(indexNumber))
            newDataFrame = dataFrame.loc[:(indexNumber - 1)]

    return newDataFrame

# yearly data analysis by brand with pie chart
# @param dataframe
# @return dataframe showing yearly sales by brands
def yearlyAnalysisByBrands(dataFrame):

    # correction according to different typing shapes in columns in the category section
    df = dataFrame.loc[:, : 'Category']
    check = 0
    for value, row in df.iterrows():
        if row.Category == 'Toplam/Total':
            check = 1

    if check == 0:
        yearlyData = pd.concat([dataFrame[dataFrame.Category == 'TOPLAM'].Total,
                                dataFrame[dataFrame.Category == 'TOPLAM'].Brand],
                                axis=1)
    else:
        yearlyData = pd.concat([dataFrame[dataFrame.Category == 'Toplam/Total'].Total,
                                dataFrame[dataFrame.Category == 'Toplam/Total'].Brand],
                                axis=1)

    # trace0 = go.Pie(labels = yearlyData.Brand, values = yearlyData.Total,
                        # title='Markaların Yıl İçerisindeki Satışlara Göre Payları')

    # plot([trace0], filename=fileName)
    return yearlyData

# editing data, total sales by month, brands
# @param one or more dataframe
# @return edited dataframeList
def totalSalesByBrand(*dataFrame):

    dataFrameList = []
    for df in dataFrame:

        # only Category column
        df2 = df.loc[:, : 'Category']
        check = 0
        for value, row in df2.iterrows():
            if row.Category == 'Toplam/Total':
                check = 1

        if check == 0:
            df = df[df.Category == 'TOPLAM']
        else:
            df = df[df.Category == 'Toplam/Total']

        df = df.drop(df.columns[[1, 2, 3]], axis=1)

        # get dataframe transpoze
        transpoze = df.T
        # transpoze set columns
        transpoze.columns = df.Brand.values.tolist()

        # drop columns
        transpoze = transpoze.drop(['Brand', 'Total'])

        # edit dataframe columns
        transpoze.columns = transpoze.columns.str.replace(' ', '')
        transpoze.columns = transpoze.columns.str.lower()
        transpoze.columns = transpoze.columns.str.replace('-', '')

        # add transpoze to the list
        dataFrameList.append(transpoze)

    return dataFrameList

# different year data append a dataframe
# @param dataframe list
# @return a appended dataframe
def appendDataByYear(dataFrame):

    # if the size of the dataframe list is 2
    if len(dataFrame) == 2:
        result = dataFrame[0].append(dataFrame[1])

    # if the size of the dataframe list is greater than two
    elif len(dataFrame) > 2:
        result = dataFrame[0].append(dataFrame[1])

        for i in range(2, len(dataFrame)):
            result = result.append(dataFrame[i])

    return result

# dataFrame index set date_range
# @param changing dataFrame
# @param range for index
# @return changed dataFrame
def dateRange(dataFrame, range):

    # date range according to the size of the dataframe
    dateRange = pd.date_range(start='1/1/2004', periods=range, freq='MS')

    # new column ['Date']
    dataFrame['Date'] = dateRange

    # set index
    dataFrame.set_index('Date', inplace=True)
    return dataFrame

# specific range sales by brand,start & endDate
# @param dataframe
# @param startdate
# @param enddate
# @param brand
# @return specific dataframe
def specificRangeSalesByBrand(dataFrame, startDate, endDate, *brand):

    # brand is not none
    if len(brand) > 0:
        x = dataFrame.loc[startDate:endDate, brand]

    # brand is none
    else:
        x = dataFrame.loc[startDate:endDate]

    # draw scatter chart
    drawScatterChart(x)

    return x


# draw scatter chart given dataFrame
# @param dataframe
# @param save chart filename
# @return scatter chart tracelist
def drawScatterChart(dataFrame):

    traceList = []
    columnList = dataFrame.columns

    # a scatter for each column
    for column in columnList:
        traceList.append(go.Scatter(x = dataFrame.index, y=dataFrame[column], name = column))

    # plot(traceList, filename=filename)
    return traceList

# given dataframe with startdate & end date draw pie chart
# @param dataframe
# @param startdate
# @param enddate
# @return pie chart trace
def drawPieChart(dataFrame, startDate = '10/1/2017', endDate = '10/1/2018'):

    # specific dataframe with startdate & enddate
    pieData = dataFrame.loc[(dataFrame.index >= startDate) & (dataFrame.index <= endDate)]

    valueList = []

    # sum of all sales by month for each brand
    for t in pieData.columns:
        valueList.append(pieData[t].sum())

    # new row for total
    pieData = pieData.append(pd.Series(valueList, index=pieData.columns), ignore_index=True)

    # limit for those who remain below one percent of the sum of sales
    belowOnePercent = pieData.T[len(pieData.T.columns)-1].sum() / 100

    valuesList = []
    indexList = []

    # only index & total sales(pandas series)
    newDF = pieData.T.loc[:, len(pieData.T.columns)-1]

    otherValue = 0

    # to be found below one percent of the total sales and added to the 'others' part
    for key,value in newDF.iteritems():
        if value > belowOnePercent:
            indexList.append(key)
            valuesList.append(value)
        else:
            otherValue = otherValue + value

    # add 'others'
    indexList.append('other brands')
    valuesList.append(otherValue)

    trace0 = go.Pie(labels=indexList, values=valuesList)
    # plot([trace0], filename='xxx.html')
    return trace0

def drawTableForTotalSales(dataFrame, brand='volkswagen', startDate = '10/1/2017', endDate = '10/1/2018'):
    #  specific dataframe with startdate & enddate
    pieData = dataFrame.loc[(dataFrame.index >= startDate) & (dataFrame.index <= endDate)]

    valueList = []

    # sum of all sales by month for each brand
    for t in pieData.columns:
        valueList.append(pieData[t].sum())

    #  new row for total
    pieData = pieData.append(pd.Series(valueList, index=pieData.columns), ignore_index=True)

    #  only index & total sales(pandas series)
    totalSeries = pieData.T.loc[:, len(pieData.T.columns) - 1]

    brandTotalSales = 0

    for key, value in totalSeries.iteritems():
        if key == brand:
            brandTotalSales = value

    return brandTotalSales

# main
if __name__ == '__main__':
    main()
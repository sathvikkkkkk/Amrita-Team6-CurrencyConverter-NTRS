# Importing all required packages
from streamlit_option_menu import option_menu
from PIL import Image
from os import listdir
from os.path import isfile, join
import pandas as pd
from itertools import chain
import streamlit as st
from datetime import datetime
import datetime
from statsmodels.tsa.arima.model import ARIMA


# Reading all the files from the given input directory
dirPath = r"/Currency_Conversion_Test_Data"
fileNames = listdir(dirPath)

filePaths = []
for fileName in fileNames:
    if isfile(join(dirPath, fileName)):
        filePaths.append(join(dirPath, fileName))

newDir = r"/New Data"
newFilePaths = []
for file in filePaths:
    newFilePaths.append(join(newDir, file.split("//")[-1]))
    print(file.split("/")[-1])


# Function for obtaining Monthly Report
def obtainMonthlyReport(year, month, currencyCode):
    for file in newFilePaths:
        if str(year) in file:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            df.columns = df.columns.str.replace('   ', ' ')
            df = df[df['Date'].str.contains(month)]
            currencyArray = df[currencyCode].values
            dateArray = df['Date'].values
            dateArray = dateArray.flatten()
            currencyArray = currencyArray.flatten()
            currencyArray = currencyArray.tolist()
            dateArray = dateArray.tolist()
            maxRate = max(currencyArray)
            maxDate = dateArray[currencyArray.index(maxRate)]
            minRate = min(currencyArray)
            minDate = dateArray[currencyArray.index(minRate)]
    return currencyArray, dateArray, minRate, minDate, maxRate, maxDate


# Function for obtaining Quarterly Report
def obtainQuarterlyReport(year, month, currencyCode):
    endMonths = ['Nov', 'Dec']
    if month in endMonths:
        yearInc = int(year) + 1
        print(yearInc)
        if month == 'Nov':
            return obtainRangeReport(year, yearInc, 'Nov', 'Feb', currencyCode)
        elif month == 'Dec':
            return obtainRangeReport(year, yearInc, 'Dec', 'Mar', currencyCode)
    else:
        for file in newFilePaths:
            if str(year) in file:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip()
                df.columns = df.columns.str.replace('   ', ' ')
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                for mon in months:
                    if mon == month:
                        i = months.index(mon)
                        break
                requMonths = [months[i], months[i + 1], months[i + 2]]
                currencyArray = []
                dateArray = []
                for month in requMonths:
                    dfNew = df[df['Date'].str.contains(month)]
                    cArray = dfNew[currencyCode].values
                    dArray = dfNew['Date'].values
                    dArray = dArray.flatten()
                    cArray = cArray.flatten()
                    currencyArray.append(cArray.tolist())
                    dateArray.append(dArray.tolist())
                currencyArray = list(chain.from_iterable(currencyArray))
                dateArray = list(chain.from_iterable(dateArray))
                maxRate = max(currencyArray)
                maxDate = dateArray[currencyArray.index(maxRate)]
                minRate = min(currencyArray)
                minDate = dateArray[currencyArray.index(minRate)]
    return currencyArray, dateArray, minRate, minDate, maxRate, maxDate


# Function for obtaining Half Yearly Report
def obtainHalfYearlyReport(year, month, currencyCode):
    endMonths = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if month in endMonths:
        yearInc = int(year) + 1
        print(yearInc)
        if month == 'Aug':
            return obtainRangeReport(year, yearInc, 'Aug', 'Feb', currencyCode)
        elif month == 'Sep':
            return obtainRangeReport(year, yearInc, 'Sep', 'Mar', currencyCode)
        elif month == 'Oct':
            return obtainRangeReport(year, yearInc, 'Oct', 'Apr', currencyCode)
        elif month == 'Nov':
            return obtainRangeReport(year, yearInc, 'Nov', 'May', currencyCode)
        elif month == 'Dec':
            return obtainRangeReport(year, yearInc, 'Dec', 'Jun', currencyCode)
    else:
        for file in newFilePaths:
            if str(year) in file:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip()
                df.columns = df.columns.str.replace('   ', ' ')
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                for mon in months:
                    if mon == month:
                        i = months.index(mon)
                        break
                requMonths = [months[i], months[i + 1], months[i + 2], months[i + 3], months[i + 4], months[i + 5]]
                currencyArray = []
                dateArray = []
                for month in requMonths:
                    dfNew = df[df['Date'].str.contains(month)]
                    cArray = dfNew[currencyCode].values
                    dArray = dfNew['Date'].values
                    dArray = dArray.flatten()
                    cArray = cArray.flatten()
                    currencyArray.append(cArray.tolist())
                    dateArray.append(dArray.tolist())
                currencyArray = list(chain.from_iterable(currencyArray))
                dateArray = list(chain.from_iterable(dateArray))
                maxRate = max(currencyArray)
                maxDate = dateArray[currencyArray.index(maxRate)]
                minRate = min(currencyArray)
                minDate = dateArray[currencyArray.index(minRate)]
    return currencyArray, dateArray, minRate, minDate, maxRate, maxDate


# Function for obtaining Yearly Report
def obtainAnnualReport(year, currencyCode):
    for file in newFilePaths:
        if str(year) in file:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            df.columns = df.columns.str.replace('   ', ' ')
            currencyArray = df[currencyCode].values
            dateArray = df['Date'].values
            dateArray = dateArray.flatten()
            currencyArray = currencyArray.flatten()
            currencyArray = currencyArray.tolist()
            dateArray = dateArray.tolist()
            maxRate = max(currencyArray)
            maxDate = dateArray[currencyArray.index(maxRate)]
            minRate = min(currencyArray)
            minDate = dateArray[currencyArray.index(minRate)]
    return currencyArray, dateArray, minRate, minDate, maxRate, maxDate


# Function for Report between particular range of time
def obtainRangeReport(yearFrom, yearTo, monthFrom, monthTo, currencyCode):
    currencyArray = []
    dateArray = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for file in newFilePaths:
        if str(yearFrom) in file:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            df.columns = df.columns.str.replace('   ', ' ')
            for mon in months:
                if mon == monthFrom:
                    ind1 = months.index(mon)
                    break
            ind2 = months.index('Dec')
            for i in range(ind1, ind2):
                month = months[i]
                dfNew = df[df['Date'].str.contains(month)]
                cArray = dfNew[currencyCode].values
                dArray = dfNew['Date'].values
                dArray = dArray.flatten()
                cArray = cArray.flatten()
                currencyArray.append(cArray.tolist())
                dateArray.append(dArray.tolist())
    if (yearTo - yearFrom) > 1:
        for year in range(yearFrom, yearTo):
            cArray, dArray, minRate, minDate, maxRate, maxDate = obtainAnnualReport(year, currencyCode)
            currencyArray.append(cArray)
            dateArray.append(dArray)
    for file in newFilePaths:
        if str(yearTo) in file:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            df.columns = df.columns.str.replace('   ', ' ')
            for mon in months:
                if mon == monthTo:
                    ind2 = months.index(mon)
                    break
            ind1 = months.index('Jan')
            for i in range(ind1, ind2):
                month = months[i]
                dfNew = df[df['Date'].str.contains(month)]
                cArray = dfNew[currencyCode].values
                dArray = dfNew['Date'].values
                dArray = dArray.flatten()
                cArray = cArray.flatten()
                currencyArray.append(cArray.tolist())
                dateArray.append(dArray.tolist())
    currencyArray = list(chain.from_iterable(currencyArray))
    dateArray = list(chain.from_iterable(dateArray))
    maxRate = max(currencyArray)
    maxDate = dateArray[currencyArray.index(maxRate)]
    minRate = min(currencyArray)
    minDate = dateArray[currencyArray.index(minRate)]
    return currencyArray, dateArray, minRate, minDate, maxRate, maxDate


# Function for next day prediction
def followingDayPrediction(currencyCode):
    dictionary = {}
    year = 2022
    for file in newFilePaths:
        if str(year) in file:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            df.columns = df.columns.str.replace('   ', ' ')
            for i in range(2, len(df.columns[2:]) + 2):
                model = ARIMA(df.iloc[:, i].values)
                model_fit = model.fit()
                dictionary[df.columns[i]] = model_fit.forecast(1).tolist()[0]
    return dictionary[currencyCode]


# FUNCTIONS
def convertUSD(usd, currencyCode):
    today = datetime.date.today()
    year = today.year
    for file in newFilePaths:
        if str(year) in file:
            exchangeRate = obtainExchangeRateWithYear(file, currencyCode)
            return usd * float(exchangeRate)


def obtainExchangeRateWithYear(file, currencyCode):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('   ', ' ')
    rate = df[currencyCode].mean()
    return rate


def obtainExchangeRateWithMonth(file, currencyCode, month):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('   ', ' ')
    df = df[df['Date'].str.contains(month)]
    rate = df[currencyCode].mean()
    return rate


def obtainExchangeRateWithDate(file, date, currencyCode):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('   ', ' ')
    dfRow = df[df.Date == date]
    value = float(dfRow[currencyCode])
    return value


def convertCurrency(currency, currencyCode1, currencyCode2):
    today = datetime.date.today()
    year = today.year
    for file in newFilePaths:
        if str(year) in file:
            exchangeRate1 = float(obtainExchangeRateWithYear(file, currencyCode1))
            exchangeRate2 = float(obtainExchangeRateWithYear(file, currencyCode2))
    return currency * exchangeRate2 / exchangeRate1


with st.sidebar:
    choose = option_menu("Currency Converter",
                         ["Present Date", "Monthly", "Quarterly", "Half Yearly", "Annual", "Custom Timeline",
                          "Next Day Prediction"],
                         # icons=['calender', 'half', 'kanban', 'book', 'person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#54B1E7"},
                             "icon": {"color": "white", "font-size": "20px"},
                             "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#A59895"},
                             "nav-link-selected": {"background-color": "#000000"},
                         }
                         )

if choose == "Monthly":
    st.title("Monthly Report of a Currency")
    option1 = 'U.S. dollar (USD)'
    option1Array = option1.split(" ")
    optionStr = ""
    for option in option1Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]
    url = "https://www.google.com/search?q=" + optionStr
    st.write('Base Currency : ' + option1)
    st.write(" [Know more](%s) " % url)

    option2 = st.selectbox(

        'Currency To be Compared into',
        ('Indian rupee (INR)', 'Algerian dinar (DZD)', 'Australian dollar (AUD)',
         'Bahrain dinar (BHD)', 'Bolivar Fuerte (VEF)', 'Botswana pula (BWP)',
         'Brazilian real (BRL)', 'Brunei dollar (BND)', 'Canadian dollar (CAD)',
         'Chilean peso (CLP)', 'Chinese yuan (CNY)', 'Colombian peso (COP)',
         'Czech koruna (CZK)', 'Danish krone (DKK)', 'Euro (EUR)',
         'Hungarian forint (HUF)', 'Icelandic krona (ISK)',
         'Indonesian rupiah (IDR)', 'Iranian rial (IRR)',
         'Israeli New Shekel (ILS)', 'Japanese yen (JPY)',
         'Kazakhstani tenge (KZT)', 'Korean won (KRW)', 'Kuwaiti dinar (KWD)',
         'Libyan dinar (LYD)', 'Malaysian ringgit (MYR)',
         'Mauritian rupee (MUR)', 'Mexican peso (MXN)', 'Nepalese rupee (NPR)',
         'New Zealand dollar (NZD)', 'Norwegian krone (NOK)', 'Omani rial (OMR)',
         'Pakistani rupee (PKR)', 'Peruvian sol (PEN)', 'Philippine peso (PHP)',
         'Polish zloty (PLN)', 'Qatari riyal (QAR)', 'Russian ruble (RUB)',
         'Saudi Arabian riyal (SAR)', 'Singapore dollar (SGD)',
         'South African rand (ZAR)', 'Sri Lankan rupee (LKR)',
         'Swedish krona (SEK)', 'Swiss franc (CHF)', 'Thai baht (THB)',
         'Trinidadian dollar (TTD)', 'Tunisian dinar (TND)',
         'U.A.E. dirham (AED)', 'U.K. pound (GBP)', 'U.S. dollar (USD)',
         'Uruguayan peso (UYU)'))

    option2Array = option2.split(" ")
    optionStr = ""
    for option in option2Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]

    url = "https://www.google.com/search?q=" + optionStr
    st.write('You selected : ' + option2)
    st.write(" [Know more](%s) " % url)
    col1, col2 = st.columns([0.9, 0.1])
    with col1:  # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #54B1E7;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Select the Month and Year for Monthly Report</p>', unsafe_allow_html=True)
        month = st.selectbox('Select Month',
                             ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        year = st.selectbox('Select Year', range(2012, 2023))

        currencyArray, dateArray, minRate, minDate, maxRate, maxDate = obtainMonthlyReport(year, month, option2)

        for date in dateArray:
            day = date.split('-')
            if len(day[0]) == 1:
                dateArray[dateArray.index(date)] = "0" + date
        chart_data = pd.DataFrame(
            list(zip(currencyArray, dateArray)), columns=['currency', 'date']
        )
        st.line_chart(chart_data, x='date', y='currency')
        st.write("Minimum exchange rate", str(minRate), " on ", str(minDate))
        st.write("Maximum exchange rate", str(maxRate), " on ", str(maxDate))


elif choose == "Quarterly":
    st.title("Quarterly Report of a Currency")
    option1 = 'U.S. dollar (USD)'
    option1Array = option1.split(" ")
    optionStr = ""
    for option in option1Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]
    url = "https://www.google.com/search?q=" + optionStr
    st.write('Base Currency : ' + option1)
    st.write(" [Know more](%s) " % url)
    option2 = st.selectbox(

        'Currency To be Compared into',
        ('Indian rupee (INR)', 'Algerian dinar (DZD)', 'Australian dollar (AUD)',
         'Bahrain dinar (BHD)', 'Bolivar Fuerte (VEF)', 'Botswana pula (BWP)',
         'Brazilian real (BRL)', 'Brunei dollar (BND)', 'Canadian dollar (CAD)',
         'Chilean peso (CLP)', 'Chinese yuan (CNY)', 'Colombian peso (COP)',
         'Czech koruna (CZK)', 'Danish krone (DKK)', 'Euro (EUR)',
         'Hungarian forint (HUF)', 'Icelandic krona (ISK)',
         'Indonesian rupiah (IDR)', 'Iranian rial (IRR)',
         'Israeli New Shekel (ILS)', 'Japanese yen (JPY)',
         'Kazakhstani tenge (KZT)', 'Korean won (KRW)', 'Kuwaiti dinar (KWD)',
         'Libyan dinar (LYD)', 'Malaysian ringgit (MYR)',
         'Mauritian rupee (MUR)', 'Mexican peso (MXN)', 'Nepalese rupee (NPR)',
         'New Zealand dollar (NZD)', 'Norwegian krone (NOK)', 'Omani rial (OMR)',
         'Pakistani rupee (PKR)', 'Peruvian sol (PEN)', 'Philippine peso (PHP)',
         'Polish zloty (PLN)', 'Qatari riyal (QAR)', 'Russian ruble (RUB)',
         'Saudi Arabian riyal (SAR)', 'Singapore dollar (SGD)',
         'South African rand (ZAR)', 'Sri Lankan rupee (LKR)',
         'Swedish krona (SEK)', 'Swiss franc (CHF)', 'Thai baht (THB)',
         'Trinidadian dollar (TTD)', 'Tunisian dinar (TND)',
         'U.A.E. dirham (AED)', 'U.K. pound (GBP)', 'U.S. dollar (USD)',
         'Uruguayan peso (UYU)'))

    option2Array = option2.split(" ")
    optionStr = ""
    for option in option2Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]

    url = "https://www.google.com/search?q=" + optionStr
    st.write('You selected : ' + option2)
    st.write(" [Know more](%s) " % url)
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #54B1E7;} 
            </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Select the Month and Year for Quarterly Report</p>', unsafe_allow_html=True)
        month = st.selectbox('Select Month',
                             ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        year = st.selectbox('Select Year', range(2012, 2023))

        currencyArray, dateArray, minRate, minDate, maxRate, maxDate = obtainQuarterlyReport(year, month, option2)

        for date in dateArray:
            day = date.split('-')
            if len(day[0]) == 1:
                dateArray[dateArray.index(date)] = "0" + date
        chart_data = pd.DataFrame(
            list(zip(currencyArray, dateArray)), columns=['currency', 'date']
        )
        chart_data['date'] = pd.to_datetime(chart_data['date'])
        st.line_chart(chart_data, x='date', y='currency')
        st.write("Minimum exchange rate", str(minRate), " on ", str(minDate))
        st.write("Maximum exchange rate", str(maxRate), " on ", str(maxDate))

elif choose == "Half Yearly":
    st.title("Half Yearly Report of a Currency")
    option1 = 'U.S. dollar (USD)'
    option1Array = option1.split(" ")
    optionStr = ""
    for option in option1Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]
    url = "https://www.google.com/search?q=" + optionStr
    st.write('Base Currency : ' + option1)
    st.write(" [Know more](%s) " % url)

    option2 = st.selectbox(

        'Currency To be Compared into',
        ('Indian rupee (INR)', 'Algerian dinar (DZD)', 'Australian dollar (AUD)',
         'Bahrain dinar (BHD)', 'Bolivar Fuerte (VEF)', 'Botswana pula (BWP)',
         'Brazilian real (BRL)', 'Brunei dollar (BND)', 'Canadian dollar (CAD)',
         'Chilean peso (CLP)', 'Chinese yuan (CNY)', 'Colombian peso (COP)',
         'Czech koruna (CZK)', 'Danish krone (DKK)', 'Euro (EUR)',
         'Hungarian forint (HUF)', 'Icelandic krona (ISK)',
         'Indonesian rupiah (IDR)', 'Iranian rial (IRR)',
         'Israeli New Shekel (ILS)', 'Japanese yen (JPY)',
         'Kazakhstani tenge (KZT)', 'Korean won (KRW)', 'Kuwaiti dinar (KWD)',
         'Libyan dinar (LYD)', 'Malaysian ringgit (MYR)',
         'Mauritian rupee (MUR)', 'Mexican peso (MXN)', 'Nepalese rupee (NPR)',
         'New Zealand dollar (NZD)', 'Norwegian krone (NOK)', 'Omani rial (OMR)',
         'Pakistani rupee (PKR)', 'Peruvian sol (PEN)', 'Philippine peso (PHP)',
         'Polish zloty (PLN)', 'Qatari riyal (QAR)', 'Russian ruble (RUB)',
         'Saudi Arabian riyal (SAR)', 'Singapore dollar (SGD)',
         'South African rand (ZAR)', 'Sri Lankan rupee (LKR)',
         'Swedish krona (SEK)', 'Swiss franc (CHF)', 'Thai baht (THB)',
         'Trinidadian dollar (TTD)', 'Tunisian dinar (TND)',
         'U.A.E. dirham (AED)', 'U.K. pound (GBP)', 'U.S. dollar (USD)',
         'Uruguayan peso (UYU)'))

    option2Array = option2.split(" ")
    optionStr = ""
    for option in option2Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]

    url = "https://www.google.com/search?q=" + optionStr
    st.write('You selected : ' + option2)
    st.write(" [Know more](%s) " % url)
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #54B1E7;} 
            </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Select the Month and Year for Half Yearly Report</p>', unsafe_allow_html=True)
        month = st.selectbox('Select Month',
                             ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        year = st.selectbox('Select Year', range(2012, 2023))

        currencyArray, dateArray, minRate, minDate, maxRate, maxDate = obtainHalfYearlyReport(year, month, option2)

        for date in dateArray:
            day = date.split('-')
            if len(day[0]) == 1:
                dateArray[dateArray.index(date)] = "0" + date
        chart_data = pd.DataFrame(
            list(zip(currencyArray, dateArray)), columns=['currency', 'date']
        )
        chart_data['date'] = pd.to_datetime(chart_data['date'])
        st.line_chart(chart_data, x='date', y='currency')
        st.write("Minimum exchange rate", str(minRate), " on ", str(minDate))
        st.write("Maximum exchange rate", str(maxRate), " on ", str(maxDate))

elif choose == "Annual":
    st.title("Annual Report of a Currency")
    option1 = 'U.S. dollar (USD)'
    option1Array = option1.split(" ")
    optionStr = ""
    for option in option1Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]
    url = "https://www.google.com/search?q=" + optionStr
    st.write('Base Currency : ' + option1)
    st.write(" [Know more](%s) " % url)

    option2 = st.selectbox(

        'Currency To be Compared into',
        ('Indian rupee (INR)', 'Algerian dinar (DZD)', 'Australian dollar (AUD)',
         'Bahrain dinar (BHD)', 'Bolivar Fuerte (VEF)', 'Botswana pula (BWP)',
         'Brazilian real (BRL)', 'Brunei dollar (BND)', 'Canadian dollar (CAD)',
         'Chilean peso (CLP)', 'Chinese yuan (CNY)', 'Colombian peso (COP)',
         'Czech koruna (CZK)', 'Danish krone (DKK)', 'Euro (EUR)',
         'Hungarian forint (HUF)', 'Icelandic krona (ISK)',
         'Indonesian rupiah (IDR)', 'Iranian rial (IRR)',
         'Israeli New Shekel (ILS)', 'Japanese yen (JPY)',
         'Kazakhstani tenge (KZT)', 'Korean won (KRW)', 'Kuwaiti dinar (KWD)',
         'Libyan dinar (LYD)', 'Malaysian ringgit (MYR)',
         'Mauritian rupee (MUR)', 'Mexican peso (MXN)', 'Nepalese rupee (NPR)',
         'New Zealand dollar (NZD)', 'Norwegian krone (NOK)', 'Omani rial (OMR)',
         'Pakistani rupee (PKR)', 'Peruvian sol (PEN)', 'Philippine peso (PHP)',
         'Polish zloty (PLN)', 'Qatari riyal (QAR)', 'Russian ruble (RUB)',
         'Saudi Arabian riyal (SAR)', 'Singapore dollar (SGD)',
         'South African rand (ZAR)', 'Sri Lankan rupee (LKR)',
         'Swedish krona (SEK)', 'Swiss franc (CHF)', 'Thai baht (THB)',
         'Trinidadian dollar (TTD)', 'Tunisian dinar (TND)',
         'U.A.E. dirham (AED)', 'U.K. pound (GBP)', 'U.S. dollar (USD)',
         'Uruguayan peso (UYU)'))

    option2Array = option2.split(" ")
    optionStr = ""
    for option in option2Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]

    url = "https://www.google.com/search?q=" + optionStr
    st.write('You selected : ' + option2)
    st.write(" [Know more](%s) " % url)
    col1, col2 = st.columns([0.8, 0.2])
    with col1:  # To display the header text using css style
        st.markdown(""" <style> .font {
                font-size:35px ; font-family: 'Cooper Black'; color: #54B1E7;} 
                </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Select the Year</p>', unsafe_allow_html=True)

        year = st.selectbox('Select Year', range(2012, 2023))

        currencyArray, dateArray, minRate, minDate, maxRate, maxDate = obtainAnnualReport(year, option2)

        for date in dateArray:
            day = date.split('-')
            if len(day[0]) == 1:
                dateArray[dateArray.index(date)] = "0" + date
        chart_data = pd.DataFrame(
            list(zip(currencyArray, dateArray)), columns=['currency', 'date']
        )
        chart_data['date'] = pd.to_datetime(chart_data['date'])
        st.line_chart(chart_data.rename(columns={'date': 'index'}).set_index('index'))
        st.write("Minimum exchange rate", str(minRate), " on ", str(minDate))
        st.write("Maximum exchange rate", str(maxRate), " on ", str(maxDate))

elif choose == "Custom Timeline":
    st.title("Customized Report on Time Interval")
    option1 = 'U.S. dollar (USD)'
    option1Array = option1.split(" ")
    optionStr = ""
    for option in option1Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]
    url = "https://www.google.com/search?q=" + optionStr
    st.write('Base Currency : ' + option1)
    st.write(" [Know more](%s) " % url)

    option2 = st.selectbox(

        'Currency To be Compared into',
        ('Indian rupee (INR)', 'Algerian dinar (DZD)', 'Australian dollar (AUD)',
         'Bahrain dinar (BHD)', 'Bolivar Fuerte (VEF)', 'Botswana pula (BWP)',
         'Brazilian real (BRL)', 'Brunei dollar (BND)', 'Canadian dollar (CAD)',
         'Chilean peso (CLP)', 'Chinese yuan (CNY)', 'Colombian peso (COP)',
         'Czech koruna (CZK)', 'Danish krone (DKK)', 'Euro (EUR)',
         'Hungarian forint (HUF)', 'Icelandic krona (ISK)',
         'Indonesian rupiah (IDR)', 'Iranian rial (IRR)',
         'Israeli New Shekel (ILS)', 'Japanese yen (JPY)',
         'Kazakhstani tenge (KZT)', 'Korean won (KRW)', 'Kuwaiti dinar (KWD)',
         'Libyan dinar (LYD)', 'Malaysian ringgit (MYR)',
         'Mauritian rupee (MUR)', 'Mexican peso (MXN)', 'Nepalese rupee (NPR)',
         'New Zealand dollar (NZD)', 'Norwegian krone (NOK)', 'Omani rial (OMR)',
         'Pakistani rupee (PKR)', 'Peruvian sol (PEN)', 'Philippine peso (PHP)',
         'Polish zloty (PLN)', 'Qatari riyal (QAR)', 'Russian ruble (RUB)',
         'Saudi Arabian riyal (SAR)', 'Singapore dollar (SGD)',
         'South African rand (ZAR)', 'Sri Lankan rupee (LKR)',
         'Swedish krona (SEK)', 'Swiss franc (CHF)', 'Thai baht (THB)',
         'Trinidadian dollar (TTD)', 'Tunisian dinar (TND)',
         'U.A.E. dirham (AED)', 'U.K. pound (GBP)', 'U.S. dollar (USD)',
         'Uruguayan peso (UYU)'))

    option2Array = option2.split(" ")
    optionStr = ""
    for option in option2Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]

    url = "https://www.google.com/search?q=" + optionStr
    st.write('You selected : ' + option2)
    st.write(" [Know more](%s) " % url)
    st.markdown(""" <style> .font {
                            font-size:35px ; font-family: 'Cooper Black'; color: #54B1E7;} 
                            </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Select the Month and Year</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([0.5, 0.5])

    with col1:

        frommonth = st.selectbox('From Month',
                                 ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        fromyear = st.selectbox('From Year', range(2012, 2023))
    with col2:
        tomonth = st.selectbox('To  Month',
                               ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        toyear = st.selectbox('To Year', range(2012, 2023))

    currencyArray, dateArray, minRate, minDate, maxRate, maxDate = obtainRangeReport(fromyear, toyear, frommonth,
                                                                                     tomonth, option2)

    for date in dateArray:
        day = date.split('-')
        if len(day[0]) == 1:
            dateArray[dateArray.index(date)] = "0" + date
    chart_data = pd.DataFrame(
        list(zip(currencyArray, dateArray)), columns=['currency', 'date']
    )
    chart_data['date'] = pd.to_datetime(chart_data['date'])
    st.line_chart(chart_data.rename(columns={'date': 'index'}).set_index('index'))
    st.write("Minimum exchange rate", str(minRate), " on ", str(minDate))
    st.write("Maximum exchange rate", str(maxRate), " on ", str(maxDate))

elif choose == "Next Day Prediction":
    st.title("Prediction of Currency on Next Day")
    option2 = st.selectbox(

        'Currency To be Predicted',
        ('Indian rupee (INR)', 'Algerian dinar (DZD)', 'Australian dollar (AUD)',
         'Bahrain dinar (BHD)', 'Bolivar Fuerte (VEF)', 'Botswana pula (BWP)',
         'Brazilian real (BRL)', 'Brunei dollar (BND)', 'Canadian dollar (CAD)',
         'Chilean peso (CLP)', 'Chinese yuan (CNY)', 'Colombian peso (COP)',
         'Czech koruna (CZK)', 'Danish krone (DKK)', 'Euro (EUR)',
         'Hungarian forint (HUF)', 'Icelandic krona (ISK)',
         'Indonesian rupiah (IDR)', 'Iranian rial (IRR)',
         'Israeli New Shekel (ILS)', 'Japanese yen (JPY)',
         'Kazakhstani tenge (KZT)', 'Korean won (KRW)', 'Kuwaiti dinar (KWD)',
         'Libyan dinar (LYD)', 'Malaysian ringgit (MYR)',
         'Mauritian rupee (MUR)', 'Mexican peso (MXN)', 'Nepalese rupee (NPR)',
         'New Zealand dollar (NZD)', 'Norwegian krone (NOK)', 'Omani rial (OMR)',
         'Pakistani rupee (PKR)', 'Peruvian sol (PEN)', 'Philippine peso (PHP)',
         'Polish zloty (PLN)', 'Qatari riyal (QAR)', 'Russian ruble (RUB)',
         'Saudi Arabian riyal (SAR)', 'Singapore dollar (SGD)',
         'South African rand (ZAR)', 'Sri Lankan rupee (LKR)',
         'Swedish krona (SEK)', 'Swiss franc (CHF)', 'Thai baht (THB)',
         'Trinidadian dollar (TTD)', 'Tunisian dinar (TND)',
         'U.A.E. dirham (AED)', 'U.K. pound (GBP)', 'U.S. dollar (USD)',
         'Uruguayan peso (UYU)'))

    option2Array = option2.split(" ")
    optionStr = ""
    for option in option2Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]
    url = "https://www.google.com/search?q=" + optionStr
    st.write('You selected : ' + option2 + " [Know more](%s) " % url)
    convVal = followingDayPrediction(option2)
    convVal = str(convVal)
    st.write("Predicted Value of ", option2, " in USD ", convVal)

# For Present Date
else:
    st.title('FOREX - Present Day Currency Converter')
    option1 = st.selectbox(

        'Select Currency',
        ('U.S. dollar (USD)', 'Algerian dinar (DZD)', 'Australian dollar (AUD)',
         'Bahrain dinar (BHD)', 'Bolivar Fuerte (VEF)', 'Botswana pula (BWP)',
         'Brazilian real (BRL)', 'Brunei dollar (BND)', 'Canadian dollar (CAD)',
         'Chilean peso (CLP)', 'Chinese yuan (CNY)', 'Colombian peso (COP)',
         'Czech koruna (CZK)', 'Danish krone (DKK)', 'Euro (EUR)',
         'Hungarian forint (HUF)', 'Icelandic krona (ISK)', 'Indian rupee (INR)',
         'Indonesian rupiah (IDR)', 'Iranian rial (IRR)',
         'Israeli New Shekel (ILS)', 'Japanese yen (JPY)',
         'Kazakhstani tenge (KZT)', 'Korean won (KRW)', 'Kuwaiti dinar (KWD)',
         'Libyan dinar (LYD)', 'Malaysian ringgit (MYR)',
         'Mauritian rupee (MUR)', 'Mexican peso (MXN)', 'Nepalese rupee (NPR)',
         'New Zealand dollar (NZD)', 'Norwegian krone (NOK)', 'Omani rial (OMR)',
         'Pakistani rupee (PKR)', 'Peruvian sol (PEN)', 'Philippine peso (PHP)',
         'Polish zloty (PLN)', 'Qatari riyal (QAR)', 'Russian ruble (RUB)',
         'Saudi Arabian riyal (SAR)', 'Singapore dollar (SGD)',
         'South African rand (ZAR)', 'Sri Lankan rupee (LKR)',
         'Swedish krona (SEK)', 'Swiss franc (CHF)', 'Thai baht (THB)',
         'Trinidadian dollar (TTD)', 'Tunisian dinar (TND)',
         'U.A.E. dirham (AED)', 'U.K. pound (GBP)',
         'Uruguayan peso (UYU)'))

    option1Array = option1.split(" ")
    optionStr = ""
    for option in option1Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]
    url = "https://www.google.com/search?q=" + optionStr
    st.write('You selected : ' + option1 + " [Know more](%s) " % url)

    option2 = st.selectbox(

        'Currency To be Compared into',
        ('Indian rupee (INR)', 'Algerian dinar (DZD)', 'Australian dollar (AUD)',
         'Bahrain dinar (BHD)', 'Bolivar Fuerte (VEF)', 'Botswana pula (BWP)',
         'Brazilian real (BRL)', 'Brunei dollar (BND)', 'Canadian dollar (CAD)',
         'Chilean peso (CLP)', 'Chinese yuan (CNY)', 'Colombian peso (COP)',
         'Czech koruna (CZK)', 'Danish krone (DKK)', 'Euro (EUR)',
         'Hungarian forint (HUF)', 'Icelandic krona (ISK)',
         'Indonesian rupiah (IDR)', 'Iranian rial (IRR)',
         'Israeli New Shekel (ILS)', 'Japanese yen (JPY)',
         'Kazakhstani tenge (KZT)', 'Korean won (KRW)', 'Kuwaiti dinar (KWD)',
         'Libyan dinar (LYD)', 'Malaysian ringgit (MYR)',
         'Mauritian rupee (MUR)', 'Mexican peso (MXN)', 'Nepalese rupee (NPR)',
         'New Zealand dollar (NZD)', 'Norwegian krone (NOK)', 'Omani rial (OMR)',
         'Pakistani rupee (PKR)', 'Peruvian sol (PEN)', 'Philippine peso (PHP)',
         'Polish zloty (PLN)', 'Qatari riyal (QAR)', 'Russian ruble (RUB)',
         'Saudi Arabian riyal (SAR)', 'Singapore dollar (SGD)',
         'South African rand (ZAR)', 'Sri Lankan rupee (LKR)',
         'Swedish krona (SEK)', 'Swiss franc (CHF)', 'Thai baht (THB)',
         'Trinidadian dollar (TTD)', 'Tunisian dinar (TND)',
         'U.A.E. dirham (AED)', 'U.K. pound (GBP)', 'U.S. dollar (USD)',
         'Uruguayan peso (UYU)'))

    option2Array = option2.split(" ")
    optionStr = ""
    for option in option2Array:
        optionStr = optionStr + option + "+"
    optionStr = optionStr[0:len(optionStr) - 1]

    url = "https://www.google.com/search?q=" + optionStr
    st.write('You selected : ' + option2 + " [Know more](%s) " % url)

    st.write("Enter value to be converted from ", option1)
    value1 = st.text_input(option1, 1)
    value1int = int(float(value1))
    convVal = convertCurrency(value1int, option1, option2)
    conValStr = str(convVal)

    st.markdown("""
    <style>
    .big-font {
        font-size:100px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.write("The Converted Value from ", value1, " ", option1, " to ", option2, " is ", conValStr)
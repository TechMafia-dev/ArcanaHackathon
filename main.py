import json
import os
# import cohere
# import ast
# import time
# from urllib.request import urlopen, Request
# from datetime import date, timedelta
#
# import requests
# from bs4 import BeautifulSoup
# from textblob import TextBlob
from flask import Flask, render_template, jsonify
# import pandas as pd
import requests
from tradingview_ta import TA_Handler, Interval, Exchange

# create the app
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/portfolio")
def portfolio():
    portfolio = [
        {'sno' : 1, 'name': 'BBYL', 'buy_date' : '2021-05-04 14:30:00', 'buy_price' : 321, 'qty' : 14},
        {'sno' : 2, 'name': 'CGSL', 'buy_date' : '2020-02-18 14:30:00', 'buy_price' : 438, 'qty' : 27},
        {'sno' : 3, 'name': 'CTOL', 'buy_date' : '2019-02-01 14:30:00', 'buy_price' : 98, 'qty' : 32},
        {'sno' : 4, 'name': 'EATL', 'buy_date' : '2017-12-11 14:30:00', 'buy_price' : 128, 'qty' : 41},
        {'sno' : 5, 'name': 'GRIL', 'buy_date' : '2016-03-15 14:30:00', 'buy_price' : 199, 'qty' : 11},
        {'sno' : 6, 'name': 'FDBKL', 'buy_date' : '2013-02-21 14:30:00', 'buy_price' : 99, 'qty' : 98},
        {'sno' : 7, 'name': 'SDRL', 'buy_date' : '2012-02-13 14:30:00', 'buy_price' : 275, 'qty' : 16},
        {'sno' : 8, 'name': 'PINL', 'buy_date' : '2011-01-12 14:30:00', 'buy_price' : 63, 'qty' : 12},
        {'sno' : 9, 'name': 'YNGAL', 'buy_date' : '2010-11-22 14:30:00', 'buy_price' : 545, 'qty' : 32},
    ]
    history = [
        {'sno' : 1, 'name': 'ABDL', 'buy_date' : '2021-05-04 14:30:00', 'buy_price' : 322.5, 'qty' : 48, 'sell_date' : "2023-03-20 14:30:00", 'sell_price' : 263},
        {'sno' : 2, 'name': 'ANTOL', 'buy_date' : '2021-02-18 14:30:00', 'buy_price' : 1765, 'qty' : 61, 'sell_date' : "2022-09-21 14:30:00", 'sell_price' : 1109},
        {'sno' : 3, 'name': 'CGTL', 'buy_date' : '2021-02-03 14:30:00', 'buy_price' : 4412, 'qty' : 12, 'sell_date' : "2023-03-20 14:30:00", 'sell_price' : 4740},
        {'sno' : 4, 'name': 'HMSOL', 'buy_date' : '2016-12-09 14:30:00', 'buy_price' : 252.5, 'qty' : 230, 'sell_date' : "2018-12-13 14:30:00", 'sell_price' : 166.5},
        {'sno' : 5, 'name': 'JCHL', 'buy_date' : '2012-03-15 14:30:00', 'buy_price' : 436, 'qty' : 47, 'sell_date' : "2016-07-08 14:30:00", 'sell_price' : 547},
        {'sno' : 6, 'name': 'JHDL', 'buy_date' : '2012-02-21 14:30:00', 'buy_price' : 125.6, 'qty' : 60, 'sell_date' : "2015-06-29 14:30:00", 'sell_price' : 198.9},
        {'sno' : 7, 'name': 'RRL', 'buy_date' : '2012-02-11 14:30:00', 'buy_price' : 273, 'qty' : 22, 'sell_date' : "2013-06-03 14:30:00", 'sell_price' : 409},
        {'sno' : 8, 'name': 'VCPL', 'buy_date' : '2010-01-12 14:30:00', 'buy_price' : 40, 'qty' : 38, 'sell_date' : "2016-02-19 14:30:00", 'sell_price' : 245},
        {'sno' : 9, 'name': 'VLXL', 'buy_date' : '2009-11-20 14:30:00', 'buy_price' : 93.5, 'qty' : 105, 'sell_date' : "2015-08-03 14:30:00", 'sell_price' : 87},
    ]
    return render_template('portfolio.html', portfolio=portfolio, history=history)

@app.route("/m_trends")
def m_trends():
    return render_template('market_trends.html')

@app.route("/my_space")
def my_space():
    return render_template('my_space.html')

@app.route("/experiment")
def charting_test():
    return render_template("test.html")

@app.route('/get_quote/<param>')
def get_latest_quote(param):
    # Path to the Excel file in the static folder
    excel_file_path = 'static/data/Stocks/'+param+'.csv'

    # Read the Excel file using pandas
    df = pd.read_csv(excel_file_path)

    # Retrieve data from database or other source
    data = {'foo': param, 'value' : df.iloc[-1,3]}
    return jsonify(data)

@app.route('/get_filtered_time_series/<param>')
def get_filtered_time_series(param):
    data = json.loads(param)
    stock = param.stock
    filter = param.filter
    # Path to the Excel file in the static folder
    excel_file_path = 'static/data/Stocks/'+stock+'.csv'

    # Read the Excel file using pandas
    df = pd.read_csv(excel_file_path)
    df = pd.concat([df.iloc[:,1],df.iloc[:,3]],axis=1)
    print(df)
    # Convert DataFrame to JSON format
    json_data = df.to_json(orient='records')
    print(json_data)

    # Retrieve data from database or other source
    # data = {'foo': param, 'value' : 'namaste'}
    data = {'foo': param, 'value' : json_data}
    return jsonify(data)

@app.route('/get_time_series/<param>')
def get_time_series(param):
    # Path to the Excel file in the static folder
    excel_file_path = 'static/data/Stocks/'+param+'.csv'

    # Read the Excel file using pandas
    df = pd.read_csv(excel_file_path)
    df = pd.concat([df.iloc[:,1],df.iloc[:,3]],axis=1)
    print(df)
    # Convert DataFrame to JSON format
    json_data = df.to_json(orient='records')
    print(json_data)

    # Retrieve data from database or other source
    # data = {'foo': param, 'value' : 'namaste'}
    data = {'foo': param, 'value' : json_data}
    return jsonify(data)


@app.route('/tickers')
def get_tickers():
    data = {'foo':'Hi', 'value':["AUD", "MFPA", "AVL", "SDRL", "RRL", "HGTL", "BAL", "PZCL", "JET2L", "PINL", "SMTL", "ATSTL", "LGENL", "JAML", "WTANL", "RCPL", "EDINL", "GPEL", "ICGTL", "MYIL", "BGFDL", "VSVSL", "BRSCL", "SAINL", "FGTL", "CGTL", "SYNTL", "TWL", "ATRL", "MRCL", "TEML", "SGROL", "BOOTL", "VIDL", "JMFL", "PMPL", "DGNL", "MGNSL", "GHEL", "GRIL", "ADIGL", "PNLL", "JHDL", "EWIL", "CMLL", "MPACL", "YNGAL", "CKNL", "DNEL", "TIGTL", "JEGIL", "BGCGL", "SHRSL", "THRGL", "CGSL", "BAGL", "ARBBL", "ABDL", "HMSOL", "FDBKL", "ANTOL", "VCPL", "BWNGL", "ELML", "PDGL", "SHIL", "JGGIL", "LWDBL", "CNEL", "HRNL", "PRVL", "EATL", "ALUL", "GRGL", "MWYL", "MTOL", "SDYL", "MACFL", "DLNL", "CHGL", "KPCL", "RSWL", "NICLL", "HLCLL", "GLEL", "VLXL", "MPEL", "SVSL", "CPIL", "SXSL", "DSCVL", "FCITL", "JCHL", "REDDL", "CTOL", "SNWSL", "DIGL", "RNWHL", "FSJL", "BBYL", "FMCC", "COKE", "AMWD", "CP", "BRID", "PTSI", "MITK", "WSM", "GL", "SXI", "PEBK", "NSC", "DXYN", "COP", "TDW", "GFF", "MVF", "JHI", "LNC", "OSUR", "BCV", "JPM", "TKOMY", "SFE", "GWW", "DSGR", "CRMT", "IP", "BF-B", "SEE", "RRX", "DLHC", "WSO", "KAMN", "MNST", "SYK", "TEX", "MLAB", "HWKN", "THO", "DGII", "CDNS", "AAME", "ATRI", "LZB", "JEF", "IBM", "BMI", "WEYS", "ASYS", "ODC", "MDC", "MAS", "CUZ", "UTL", "ABM", "DE", "IEP", "NEU", "WOR", "BKH", "UMBF", "LYTS", "PHI", "ALOT", "BMY", "GAB", "MMC", "PPL", "HD", "PH", "MUR", "BAX", "NVO", "KBH", "MCR", "TMO", "UVV", "HON", "FSTR", "TRMK", "AMD", "CNA", "BIO", "OTTR", "CMU", "SHEL", "AFG", "NMI", "SNA", "PEO", "UFCS", "PTC", "SIGI", "NL", "KLAC", "EHC", "LUV", "TYL", "BXMT", "PW", "CMCSA", "WEC", "TSI", "RMCF", "SGC", "RGEN", "HIFS", "RELL", "LMT", "TELL", "KTCC", "UMH", "PNM", "IDCC", "BKTI", "AOS", "USAU", "CATO", "MATX", "ARW", "T", "VALU", "FISV", "TG", "CSPI", "WRB", "HALL", "GRC", "MTR", "EVRG", "PLAB", "IMO", "RES", "SBCF", "ROL", "ES", "IAF", "WAFD", "CTBI", "ESCA", "IPG", "LRCX", "WSBC", "NABZY", "AVY", "JNJ", "CBU", "DDS", "PEP", "WASH", "HEI", "ORI", "NI", "UNH", "TFX", "AVNW", "IEX", "AXP", "ABEO", "HAL", "CINF", "FRBK", "THMO", "SFNC", "TGT", "BBVA", "HTLD", "ICAGY", "MIDD", "TR", "GPS", "HELE", "ADI", "VIRC", "PMM", "VHI", "CIA", "CTO", "ARGO", "SNFCA", "FARM", "CNP", "GHC", "BBY", "GTY", "HUBB", "VNO", "EBIX", "OLP", "VOD", "GLW", "VSEC", "LAKE", "EAT", "MYE", "WTM", "ADSK", "MTB", "OXY"]}
    print(jsonify(data))
    return jsonify(data)

@app.route('/get_moving_average/<param>')
def get_moving_average_data(param):
    # Path to the Excel file in the static folder
    excel_file_path = 'static/data/Stocks/'+param+'.csv'

    # Read the Excel file using pandas
    df = pd.read_csv(excel_file_path)
    target_variable = 'close'
    df['ma_20'] = df[target_variable].shift(1).rolling(window=20).mean()
    df['ma_50'] = df[target_variable].shift(1).rolling(window=50).mean()
    df['ma_100'] = df[target_variable].shift(1).rolling(window=100).mean()

    df['std_20'] = df[target_variable].shift(1).rolling(window=20).std()
    df['std_50'] = df[target_variable].shift(1).rolling(window=50).std()
    df['std_100'] = df[target_variable].shift(1).rolling(window=100).std()

    df = df.dropna()
    df = df.drop_duplicates(subset='ds')

    # Convert DataFrame to JSON format
    json_data = df.to_json(orient='records')
    print(json_data)

    # Retrieve data from database or other source
    # data = {'foo': param, 'value' : 'namaste'}
    data = {'foo': param, 'value' : json_data}
    return jsonify(data)


@app.route('/stock_matrices/<param>')
def get_stock_matrices(param):
    with open('static/assets/json/stock_info.json') as json_file:
        data1 = json.load(json_file)
        if param in data1:
            return jsonify(data1[param])
    with open('static/assets/json/stock_info2.json') as json_file:
        data2 = json.load(json_file)
        if param in data2:
            return jsonify(data2[param])

@app.route('/transcripts/<param>')
def get_transcript_data(param):
    api_key = 'ib5eEMPo4jvF0pgo8icHt6hxZmC0287yGZNblWVv'
    co = cohere.Client(api_key)

    # static_path = os.path.join(app.root_path, 'static')
    # folders = [name for name in os.listdir(static_path) if os.path.isdir(os.path.join(static_path, name))]

    transcript = []
    summary_list = []
    sentiment_list = []
    main_folder_path = os.path.join(app.root_path, 'static/data/fmp-transcripts/FMP/'+param)
    for year_folder in os.listdir(main_folder_path)[:1]:
        year_folder_path = os.path.join(main_folder_path, year_folder)
        for trans_file in os.listdir(year_folder_path):
            final_path = year_folder_path + '/' + trans_file
            print(final_path)
            with open(final_path, 'r') as file:
                file_contents = file.read()
                d = ast.literal_eval(file_contents)
                text = d['content']
                response = co.summarize(text,
                                        model='summarize-xlarge',
                                        length='medium',
                                        extractiveness='medium'
                                        )
                time.sleep(5)
                summary = response.summary
                print(summary)

                blob = TextBlob(summary)
                sentiment = blob.sentiment.polarity
                print(sentiment)

                transcript.append(file_contents)
                summary_list.append(summary)
                sentiment_list.append(sentiment)
                print(file_contents)

    # Retrieve data from database or other source
    # data = {'foo': param, 'value' : 'namaste'}
    data = {'foo': param, 'transcript' : transcript, 'summary' : summary_list, 'sentiment' : sentiment_list}
    return jsonify(data)

@app.route('/stock_news/<param>')
def get_stock_news(param):

    stock = param
    news = {}

    # copy the finviz url
    # (it may change over time so make sure url ending is correct)
    url = f'https://finviz.com/quote.ashx?t={stock}&p=d'
    request = Request(url=url, headers={'user-agent': 'news_scraper'})
    response = urlopen(request)

    # parse the data
    html = BeautifulSoup(response, features='html.parser')
    finviz_news_table = html.find(id='news-table')
    news[stock] = finviz_news_table

    # filter and store neede in news_parsed
    news_parsed = []
    news_list = []
    count = 1
    for stock, news_item in news.items():  # extract only top 5 news
        for row in news_item.findAll('tr'):
            try:
                headline = row.a.getText()
                source = row.span.getText()
                news_list.append(headline)
                news_parsed.append([stock, headline])
            except:
                pass
            if count == 5:
                break
            count += 1

            # convert to a dataframe for data analysis
    # news_df = pd.DataFrame(news_parsed, columns=['Stock', 'Headline'])
    news_string = news_list[0] + news_list[1] + news_list[2] + news_list[3] + news_list[4]
    blob = TextBlob(news_string)
    sentiment = blob.sentiment.polarity
    print(sentiment)

    # Retrieve data from database or other source
    # data = {'foo': param, 'value' : 'namaste'}
    data = {'foo': param, 'value' : news_list, 'sentiment' : sentiment}
    return jsonify(data)

def predict_risk(dff):
    dff['30_dev_20']=(dff['std_20']-0.3*dff['ma_20'])/(0.3*dff['ma_20'])    # % change
    dff['10_dev_20']=(dff['std_20']-0.1*dff['ma_20'])/(0.1*dff['ma_20'])

    dff['30_dev_50']=(dff['std_50']-0.3*dff['ma_50'])/(0.3*dff['ma_50'])
    dff['10_dev_50']=(dff['std_50']-0.1*dff['ma_50'])/(0.1*dff['ma_50'])

    dff['30_dev_100']=(dff['std_100']-0.3*dff['ma_100'])/(0.3*dff['ma_100'])
    dff['10_dev_100']=(dff['std_100']-0.1*dff['ma_100'])/(0.1*dff['ma_100'])

    val30_20=dff['30_dev_20'].mean()
    val10_20=dff['10_dev_20'].mean()

    val30_50=dff['30_dev_50'].mean()
    val10_50=dff['10_dev_50'].mean()

    val30_100=dff['30_dev_100'].mean()
    val10_100=dff['10_dev_100'].mean()

    def check(val_30,val_10):
        if val_30<=0 and val_10<=0:
            return 'Low Risk Stock'
        elif val_30<=0 and val_10>0:
            return 'Moderate Risk Stock'
        else:
            return 'High Risk Stock'

    result_20=check(val30_20,val10_20)
    result_50=check(val30_50,val10_50)
    result_100=check(val30_100,val10_100)
    print(f' Taking Moving Avg of 20 , Stock = {result_20}')
    print(f' Taking Moving Avg of 50 , Stock = {result_50}')
    print(f' Taking Moving Avg of 100 , Stock = {result_100}')
    return result_20,result_50,result_100

@app.route('/risk_info/<param>')
def get_risk_analysis_info(param):
    # Path to the Excel file in the static folder
    excel_file_path = 'static/data/Stocks/'+param+'.csv'

    # Read the Excel file using pandas
    df = pd.read_csv(excel_file_path)
    target_variable = 'close'
    df['ma_20'] = df[target_variable].shift(1).rolling(window=20).mean()
    df['ma_50'] = df[target_variable].shift(1).rolling(window=50).mean()
    df['ma_100'] = df[target_variable].shift(1).rolling(window=100).mean()

    df['std_20'] = df[target_variable].shift(1).rolling(window=20).std()
    df['std_50'] = df[target_variable].shift(1).rolling(window=50).std()
    df['std_100'] = df[target_variable].shift(1).rolling(window=100).std()

    df = df.dropna()
    df = df.drop_duplicates(subset='ds')

    risk = predict_risk(df)

    # Retrieve data from database or other source
    # data = {'foo': param, 'value' : 'namaste'}
    data = {'foo': param, 'value' : risk}
    return jsonify(data)


@app.route('/get_index_series/<param>')
def get_index_series(param):
    # Path to the Excel file in the static folder
    excel_file_path = 'static/data/Indexes/'+param+'.csv'

    # Read the Excel file using pandas
    df = pd.read_csv(excel_file_path)
    df = df.dropna()
    df = df.iloc[:,:5]
    print(df)
    # Convert DataFrame to JSON format
    json_data = df.to_json(orient='records')
    print(json_data)

    # Retrieve data from database or other source
    # data = {'foo': param, 'value' : 'namaste'}
    data = {'foo': param, 'value' : json_data}
    return jsonify(data)

app.run(debug=True)

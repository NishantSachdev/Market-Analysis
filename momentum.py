from email.message import EmailMessage
from nsepy import get_history
from datetime import date , timedelta
import pandas as pd
import smtplib
from email.mime.text import MIMEText

today = str(date.today())
historical = str((date.today()-timedelta(days=350)).isoformat())
list_today = today.split('-')
list_historical = historical.split('-')

stock_list = ['RELIANCE', 'TCS', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'BHARTIARTL', 'SBIN', 
'BAJFINANCE', 'HDFC', 'ITC', 'LICI', 'ADANIENT', 'ATGL', 'ADANITRANS', 'KOTAKBANK', 'ADANIGREEN', 'ASIANPAINT', 
'DMART', 'BAJAJFINSV', 'MARUTI', 'LTI', 'HCLTECH', 'SUNPHARMA', 'TITAN', 'AXISBANK', 'WIPRO', 'NESTLEIND', 
'ULTRACEMCO', 'ADANIPORTS', 'ONGC', 'NTPC', 'M&M', 'JSWSTEEL', 'POWERGRID', 'PIDILITIND', 'COALINDIA', 
'TATAMOTORS', 'SBILIFE', 'TATASTEEL', 'HDFCLIFE', 'GRASIM', 'AMBUJACEM', 'DIVISLAB', 'DABUR', 'VEDL', 
'BAJAJ-AUTO', 'EICHERMOT', 'TECHM', 'SIEMENS', 'IOC', 'GODREJCP', 'CIPLA', 'BRITANNIA', 'INDUSINDBK', 'DLF', 
'HINDALCO', 'SBICARD', 'HAVELLS', 'HAL', 'LTI', 'SHREECEM', 'ICICIPRULI', 'SRF', 'BEL', 'DRREDDY', 'BAJAJHLDNG', 
'TATACONSUM', 'INDIGO', 'MARICO', 'TATAPOWER', 'BANKBARODA', 'BPCL', 'NYKAA', 'APOLLOHOSP', 'MCDOWELL-N', 
'BERGEPAINT', 'CHOLAFIN', 'IRCTC', 'ICICIGI', 'GAIL', 'TORNTPHARM', 'INDUSTOWER', 'ZOMATO', 'MINDTREE', 
'HEROMOTOCO', 'UPL', 'NAUKRI', 'MOTHERSON', 'BOSCHLTD', 'PIIND', 'PGHH', 'ACC', 'COLPAL', 'BANDHANBNK', 'PAYTM', 
'MUTHOOTFIN', 'JUBLFOOD', 'ZYDUSLIFE', 'PNB', 'HDFCAMC', 'MPHASIS', 'NMDC', 'BIOCON', 'GLAND', 'LUPIN', 'SAIL', 
'PEL']

def returns(close_price_list,no_of_days):
    try:
        return str(round(((close_price_list[-1]-close_price_list[-no_of_days])/close_price_list[-no_of_days])*100,2))+' %'
    except:
        pass

def volatility(close_price_list,no_of_days):
    try:
        price_list = close_price_list[-no_of_days:]
        average = sum(price_list)/len(price_list)
        deviation_list = []
        for x in price_list:
            deviation_list.append((average-x)**2)
        std_deviation =  (sum(deviation_list)/len(deviation_list))**0.5
        stock_specific_std_deviation = (std_deviation/average)*100
        return round(stock_specific_std_deviation,2)
    except:
        pass

column_names = ['Stock','3_day', '5_day','7_day','10_day','15_day','30_day','45_day','60_day','90_day','150_day','250_day','30day_vol','60day_vol','90day_vol']
full_df = pd.DataFrame(columns = column_names)
for stock in stock_list:
    print(f'Collecting data for {stock}...')
    try:
        stock_df = get_history(symbol=stock,start=date(int(list_historical[0]),int(list_historical[1]),int(list_historical[2])),end=date(int(list_today[0]),int(list_today[1]),int(list_today[2])))
    except AttributeError:
        continue
    close_price_list = stock_df['Close'].tolist()
    day_3 = returns(close_price_list,3)
    day_5 = returns(close_price_list,5)
    day_7 = returns(close_price_list,7)
    day_10 = returns(close_price_list,10)
    day_15 = returns(close_price_list,15)
    day_30 = returns(close_price_list,30)
    day_45 = returns(close_price_list,45)
    day_60 = returns(close_price_list,60)
    day_90 = returns(close_price_list,90)
    day_150 = returns(close_price_list,150)
    day_250 = returns(close_price_list,250)
    day_30_volatility = volatility(close_price_list,30)
    day_60_volatility = volatility(close_price_list,60)
    day_90_volatility = volatility(close_price_list,90)
    list_stock_momentum_detials = [stock,day_3,day_5,day_7,day_10,day_15,day_30,day_45,day_60,day_90,day_150,day_250,day_30_volatility,day_60_volatility,day_90_volatility]
    full_df.loc[len(full_df)] = list_stock_momentum_detials

# report name 
print('Preparing excel...')
date_excel = date.today()
date_excel = date_excel.strftime("%d/%m/%Y")
list_date_excel = date_excel.split("/")
date_excel = list_date_excel[0] + '_' + list_date_excel[1] + '_' + list_date_excel[2]

full_df.to_excel(date_excel+'.xlsx')

# email 
print('Preparing email message...')
html = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(full_df.to_html())

msg = EmailMessage()
msg['subject'] = "momentum"
msg['to'] = "nishant26sachdev@gmail.com"
msg['from'] = "Momentum Research"
part1 = MIMEText(html, 'html')
msg.set_content(part1)

with open(f"{date_excel}.xlsx","rb") as excel:
    data = excel.read()
    msg.add_attachment(data,maintype='application',subtype='xlsx',filename=excel.name)

print('Sending email...')
server = smtplib.SMTP("smtp.gmail.com",587) 
server.starttls()
server.login("krishnakaka4141@gmail.com","hifzuyqbgonxjtcx")
server.send_message(msg)
server.quit()
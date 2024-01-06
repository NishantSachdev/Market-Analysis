import logging
import json
import pandas as pd
import statistics
import yfinance as yf
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    # Read/Set all input/hardcoded data using config file
    config_file = "input/config.json"
    config_obj = read_config_file(config_file)
    
    df_valuation_metrics = pd.read_csv(config_obj["valuation_metrics_file"])
    list_periods = config_obj["periods"]
    index_ticker = config_obj["index_ticker"]
    time_period_market = config_obj["mkt_perf_time_period"]
    time_period_stock = config_obj["momentum_time_period"]
    output_fig_file = config_obj["output_fig_file"]
    output_excel_file = config_obj["output_excel_file"]

    # Get the list of stock tickers
    stock_list = get_nasdaq100_tickers()   # or get_sp500_tickers()

    # Calculate market valuation metrics
    df_market_valuation = market_valuation(df_valuation_metrics, list_periods)

    # Calculate market performance metrics
    df_market_performance = market_performance(index_ticker, time_period_market, list_periods, output_fig_file)

    # Calculate stock momentum metrics
    df_stock_momentum = stock_momentum(stock_list, list_periods, time_period_stock)

    # Create Excel file and add dataframes to different sheets
    with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
        df_market_valuation.to_excel(writer, sheet_name='Market Valuation Data', index=False)
        df_market_performance.to_excel(writer, sheet_name='Market Performance Data', index=False)
        df_stock_momentum.to_excel(writer, sheet_name='Stock Momentum Data', index=False)

    # Send email with excel file as attachment
    send_email(config_obj)


################################ Sub Main Functions ################################
        

# ---- Calculate the average P/E and P/B ratios for given number of days ----
def market_valuation(df_valuation_metrics, list_periods):
    try:
        logging.info("--- Begin: market_valuation ---")
        
        # Calculate P/E and P/B ratio averages and percentage changes
        logging.info("Calculating P/E and P/B ratio averages and percentage changes...")
        latest_value = df_valuation_metrics[["P/E", "P/B"]].tail(1).values.tolist()[0]
        avg_pe_values, avg_pb_values  = calculate_pe_pb_ratio_avgs(df_valuation_metrics, list_periods)
        pe_changes, pb_changes = calculate_pe_pb_ratio_changes(avg_pe_values, avg_pb_values, latest_value)

        # Create dataframe for market valuation data
        logging.info("Creating dataframe for market valuation data...")
        df_market_valuation = pd.DataFrame(
        {"No of Days" : list_periods,
        "Avg P/E" : avg_pe_values, 
        "Percentage change in P/E" : pe_changes,
        "Avg P/B" : avg_pb_values,
        "Percentage change in P/B" : pb_changes}
        )

        # Add Current P/E and P/B values to dataframe
        df_market_valuation["No of Days"] = df_market_valuation["No of Days"].astype(str) + " Days"
        df_market_valuation.loc[len(df_market_valuation)] = ""
        df_market_valuation.loc[len(df_market_valuation)] = ["", "Current P/E", "", "Current P/B", ""]
        df_market_valuation.loc[len(df_market_valuation)] = ["", latest_value[0], "", latest_value[1], ""]

        # Round all float values in df to 2 decimal places
        df_market_valuation = df_market_valuation.round(2)

        logging.info("--- End: market_valuation ---")

        return df_market_valuation
    
    except Exception as e:
        logging.error(f"An error occurred in market_valuation(): {str(e)}")


# ---- Calculate the latest percentage increase and historical average percentage increase for each period ----
def market_performance(index_ticker, time_period, list_periods, fig_filename):
    try:
        logging.info("--- Begin: market_performance ---")
        
        # Get the market data
        ticker = yf.Ticker(index_ticker)
        market_data = ticker.history(period=time_period)
        df_index_data = pd.DataFrame({"Period in Days": list_periods})

        logging.info("Calculate average price/level and percentage change for that period...")
        # Calculate average price/level for each period using list comprehension
        list_period_averages = [round(market_data["Close"].tail(days).mean(), 2) for days in list_periods]
        df_index_data["Average"] = list_period_averages

        # Calculate percentage change for each period between the latest price/level and average price/level for that period
        latest = round(market_data["Close"].tail(1).values[0], 2)
        percentage_change = ((latest - df_index_data["Average"]) / df_index_data["Average"] * 100).round(2)
        df_index_data["Latest Percentage Change"] = percentage_change

        # Calculate historical average percentage change for each period
        logging.info("Calculate historical average percentage change for each period...")
        len_full_data = len(market_data)
        list_avg_price_change = []
        for days in list_periods:
            list_price_change = []
            max_len = len_full_data // days
            for iter in range(1, max_len + 1):
                low = (iter * days) - (days - 1)
                high = iter * days
                df_subset = market_data.iloc[-high:-low, :]
                last_value = df_subset["Close"].tail(1).values[0]
                avg_value = round(df_subset["Close"].mean(), 2)
                pct_change = ((last_value - avg_value) / avg_value * 100).round(2)
                list_price_change.append(pct_change)

            list_avg_price_change.append(round(statistics.mean(list_price_change), 2))

        df_index_data[f"Historical Average Percentage Change for period - {time_period}"] = list_avg_price_change

        # Plot a bar graph between the latest percentage increase and historical average percentage increase for each period
        logging.info("Plot a bar graph between the latest percentage increase and historical average percentage increase for each period...")
        x_column = "Period in Days"
        y_columns = ["Latest Percentage Change", f"Historical Average Percentage Change for period - {time_period}"]
        title = f"Index: {index_ticker} - Latest Percentage Change vs Historical Average Percentage Change for period - {time_period}"
        plot_percentage_increase(df_index_data, x_column, y_columns, title, fig_filename)
        logging.info(f"Bar Graph saved to {fig_filename}")

        df_index_data.drop(columns=["Average"], inplace=True)
        logging.info("--- End: market_performance ---")
        return df_index_data
    
    except Exception as e:
        logging.error(f"An error occurred in market_performance(): {str(e)}")


# ---- Calculate the latest percentage increase and volatility for each period ----
def stock_momentum(stock_list, list_periods, time_period_stock):
    try:
        logging.info("--- Begin: stock_momentum ---")
        
        stock_list = get_nasdaq100_tickers()    # or get_sp500_tickers()
        time_period = time_period_stock

        full_df = pd.DataFrame(index=stock_list)
        for days in list_periods:
            full_df[f"{days} Day Returns"] = ""
        for days in list_periods:
            full_df[f"{days} Day Volatility"] = ""

        logging.info("Collecting data for all stocks...")
        data = yf.download(stock_list, period=time_period)["Close"]

        logging.info("Calculating returns and volatility for all stocks...")
        for stock in stock_list:
            close_price_list = data[stock].tolist()
            returns_list = [returns(close_price_list, days) for days in list_periods]
            volatility_list = [volatility(close_price_list, days) for days in list_periods]
            list_stock_momentum_details = returns_list + volatility_list
            full_df.loc[stock] = list_stock_momentum_details

        logging.info("--- End: stock_momentum ---")

        return full_df
    
    except Exception as e:
        logging.error(f"An error occurred in stock_momentum(): {str(e)}")


################################ Calculation Functions ################################


# Calculate average P/E and P/B ratios for given number of days
def calculate_pe_pb_ratio_avgs(avg, avg_days):
    avg_pe_values = []
    avg_pb_values = []
    for days in avg_days:
        avg_value = avg["P/E"].tail(days).mean().tolist()
        avg_pe_values.append(avg_value)
        avg_value = avg["P/B"].tail(days).mean().tolist()
        avg_pb_values.append(avg_value)
    return avg_pe_values, avg_pb_values


# Calculate percentage change in P/E and P/B ratio compared to the average
def calculate_pe_pb_ratio_changes(avg_pe_values, avg_pb_values, latest_value):
    pe_changes = []
    pb_changes = []
    for i in range(len(avg_pe_values)):
        pe_change = (avg_pe_values[i] - latest_value[0]) / avg_pe_values[i] * 100
        pe_changes.append(pe_change)
        pb_change = (avg_pb_values[i] - latest_value[1]) / avg_pb_values[i] * 100
        pb_changes.append(pb_change)
    return pe_changes, pb_changes


# Calculate the latest percentage change for given number of days
def returns(close_price_list, days):
    try:
        current_price = close_price_list[-1]
        previous_price = close_price_list[-days]
        percentage_change = ((current_price - previous_price) / previous_price) * 100
        return str(round(percentage_change, 2)) + " %"
    except:
        pass


# Calculate the volatility for given number of days
def volatility(close_price_list, days):
    try:
        price_list = close_price_list[-days:]
        average = sum(price_list) / len(price_list)
        deviation_list = []
        for x in price_list:
            deviation_list.append((average - x) ** 2)
        std_deviation = (sum(deviation_list) / len(deviation_list)) ** 0.5
        stock_specific_std_deviation = (std_deviation / average) * 100
        return round(stock_specific_std_deviation, 2)
    except:
        pass


################################ Visualization Functions ################################
        

# Plot a bar graph between the latest percentage increase and historical average percentage increase for each period
def plot_percentage_increase(df_index_data, x_column, y_columns, title, filename):
    try:
        figsize = (10, 5)
        df_index_data.plot(x=x_column, y=y_columns, kind="bar", figsize=figsize, title=title)
        plt.savefig(filename)
    except Exception as e:
        logging.error(f"An error occurred in plot_percentage_increase(): {str(e)}")


############################# Market Data Functions ###############################


# Retrieves the list of tickers for all S&P500 stocks.
def get_sp500_tickers():
    sp500_tickers = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )[0]
    if len(sp500_tickers["Symbol"]) > 500:
        return sp500_tickers["Symbol"].head(500).tolist()
    
    return sp500_tickers["Symbol"].tolist()


# Retrieve the list of tickers for all Nasdaq 100 stocks
def get_nasdaq100_tickers():
    nasdaq100_tickers = pd.read_html(
        "https://en.wikipedia.org/wiki/Nasdaq-100"
    )[4]
    if len(nasdaq100_tickers["Ticker"]) > 100:
        return nasdaq100_tickers["Ticker"].head(100).tolist()
    
    return nasdaq100_tickers["Ticker"].tolist()


################################## Utility Functions ##################################


# Send email with excel file as attachment
def send_email(config_obj):
    logging.info("Preparing email message...")

    msg = EmailMessage()
    msg["subject"] = config_obj["email_subject"]
    msg["to"] = config_obj["email_to"]
    msg["from"] = "Market Research"

    msg.set_content("Please find the attached excel file for the Valuation, Performance & Momentum Report.")
    with open(config_obj["output_excel_file"], "rb") as excel:
        data = excel.read()
        msg.add_attachment(
            data, maintype="application", subtype="xlsx", filename=excel.name
        )
    
    with open(config_obj["output_fig_file"], "rb") as image:
        data = image.read()
        msg.add_attachment(
            data, maintype="image", subtype="png", filename=image.name
        )

    logging.info("Sending email...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(config_obj["email_from"], config_obj["email_password"])
    server.send_message(msg)
    server.quit()

    logging.info("Email sent successfully!")


# Read the config file
def read_config_file(config_file):
    try:
        with open(config_file) as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        logging.error(f"An error occurred in read_config_file(): {str(e)}")
        return None


########################################################################################
        

if __name__ == "__main__":
    main()

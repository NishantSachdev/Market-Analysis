### VALUATION, PERFORMANCE & MOMENTUM ANALYSIS
--------------------------------------------------------------------------

### What is the Project all about?

This project is a Python application that does valuation, performance & momentum analysis. The script starts by reading a configuration file `input/config.json` that is used as an editable input file for the project.

**_The script then_**
- calculates market **valuation** metrics using the P/E and P/B ratio data in `input/index_valuation_metrics.json`. 
- calculates market **performance** using the real time historical price/level of a broad market index and compares it to average performance older periods.
- calculates return and volatility for stocks of a broad market index that can be viewed to judge the **momentum** in the market.

**_The output can be found in output folder or sent over email which contains_**
- An excel file containing three sheets for Valuation, Performance and Momentum Analysis
- A png file plotting the market performance data.

--------------------------------------------------------------------------

### Use Case

The script is designed to be run periodically (e.g., daily or weekly) to provide updated market analysis. It can be used by financial analysts, stock market traders, and anyone interested in understanding market trends and making informed trading or investment decisions by analyzing market valuation, performance, and momentum based on real-time data. 

--------------------------------------------------------------------------

### How to Use?

1. Set inputs according to your use case and email credentials in `input/config.json`.
2. Download the latest data for the file `input/index_valuation_metrics.json` from the link - 
"https://www1.nseindia.com/products/content/equities/indices/historical_pepb.htm"
3. To run the application, execute the `mkt_valuation_perf_momentum.py` script.
3. Check the output folder or your email for `market_performance.png` to analyze market performance.
4. Check the output folder or your email for `valuation_perf_momentum.xlsx` file for the entire output.

--------------------------------------------------------------------------

### Future Scope

- Support for more financial indicators.
- Integration with more data sources.
- Advanced data visualization features.

--------------------------------------------------------------------------

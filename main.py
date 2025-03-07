from neuralintents import BasicAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf
import pickle
import sys
import datetime as dt
import yfinance as yf

portfolio={'AAPL': 20,'TSLA': 5, 'GS': 10}
with open('portfolio.pkl','rb') as f:
    portfolio=pickle.load(f)
def save_portfolio():
    with open('portfolio.pkl','wb') as f:
        pickle.dump(portfolio,f)
        
def add_portfolio():
    ticker=input("Which stock do you want to add:")
    amount= input("How many shares do you want to add:")
    
    if ticker in portfolio.keys():
        portfolio[ticker]+=amount
    else:
        portfolio[ticker]=amount
    
    save_portfolio()
    
def remove_portfolio():
    ticker=input("Which stock do you want to sell:")
    amount= input("How amny shares do you want to sell:")
    
    if ticker in portfolio.keys():
        if amount<=portfolio[ticker]:
            portfolio[ticker]-=amount
            save_portfolio()
        else:
            print("You don't have enough shares!")   
    else:
         print(f"You don't own any shares of{ticker}")

def show_portfolio():
    print("Your portfolio:")
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}")
def portfolio_worth():
    total_value = 0  
    try:
        for ticker, shares in portfolio.items():
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")  
            
            if data.empty:
                print(f"Warning: No recent data found for {ticker}. Skipping...")
                continue
            
            price = data['Close'].iloc[-1]
            total_value += price * shares  # Multiply by quantity owned
        
        print(f"Your portfolio is worth ${total_value:.2f}")
    
    except Exception as e:
        print(f"Error fetching portfolio worth: {e}")
    
def portfolio_gains():
    starting_date = input("Enter a date for comparison (YYYY-MM-DD): ")
    sum_now = 0
    sum_then = 0

    try:
        
        starting_date = pd.Timestamp(starting_date).tz_localize(None)

        for ticker, shares in portfolio.items():
            stock = yf.Ticker(ticker)

            # Fetch historical data
            data = stock.history(period="max")

            # Ensure data index is also timezone-naive for comparison
            data.index = data.index.tz_localize(None)

            # Get latest closing price
            price_now = data['Close'].iloc[-1]

            # Get closing price on the starting date or closest available trading day
            price_then = data['Close'].asof(starting_date)

            if pd.isna(price_then):  # If no close price found
                print(f"Warning: No trading data found for {ticker} on {starting_date}. Skipping...")
                continue

            # Calculate total portfolio value at both times
            sum_now += price_now * shares
            sum_then += price_then * shares

        if sum_then == 0:
            print("Error: Could not retrieve historical prices for any stocks in the portfolio.")
            return

        # Calculate gains
        relative_gains = ((sum_now - sum_then) / sum_then) * 100
        absolute_gains = sum_now - sum_then

        print(f"Relative Gains: {relative_gains:.2f}%")
        print(f"Absolute Gains: ${absolute_gains:.2f}")

    except Exception as e:
        print(f"Error: {e}")


# ... previous code remains unchanged ...
def plot_chart():
    try:
        # Get stock ticker
        ticker = input("Choose a ticker symbol (e.g., AAPL, TSLA): ").strip().upper()
        if not ticker.isalpha():
            print("Error: Invalid ticker symbol. Please enter a valid stock ticker (e.g., AAPL).")
            return

        # Get and validate date
        starting_string = input("Choose a starting date (DD/MM/YYYY): ").strip()
        try:
            start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
        except ValueError:
            print("Error: Invalid date format. Please enter the date as DD/MM/YYYY.")
            return

        end = dt.datetime.now()

        # Fetch data using yfinance
        print(f"Fetching stock data for {ticker} from {start.date()} to {end.date()}...")
        df = yf.download(ticker, start=start, end=end)

        if df.empty:
            print(f"Error: No stock data found for {ticker}. Please check the symbol and date range.")
            return

        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['Close'], label='Close Price')
        
        # Customize the plot
        plt.title(f'{ticker} Stock Price')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        plt.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Adjust layout and display
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Unexpected error: {e}")
        
def plot_pie_chart():
    try:
        total_value = 0
        values = {}
        
        # Calculate current value of each holding
        for ticker, shares in portfolio.items():
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            
            if data.empty:
                print(f"Warning: No recent data found for {ticker}. Skipping...")
                continue
            
            price = data['Close'].iloc[-1]
            value = price * shares
            values[ticker] = value
            total_value += value

        if not values:
            print("No data available to create pie chart.")
            return

        # Create pie chart
        plt.figure(figsize=(10, 8))
        plt.pie(values.values(), labels=values.keys(), autopct='%1.1f%%')
        plt.title('Portfolio Distribution')
        plt.axis('equal')
        plt.show()

    except Exception as e:
        print(f"Error creating pie chart: {e}")
                
def bye():
    print("Good Bye!")
    sys.exit(0)
   
mappings = {
    'plot_chart': plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains': portfolio_gains,
    'plot_pie_chart': plot_pie_chart,
    'bye': bye
}

assistant = BasicAssistant('intents.json', mappings, None, "finance_assistant_model")
assistant.fit_model()
assistant.save_model()
assistant.load_model()

# Single main loop
while True:
    message = input("")
    if any(x in message.lower() for x in ['plot chart', 'plot', 'show chart', 'chart']):
        plot_chart()
    elif any(x in message.lower() for x in ['pie chart', 'distribution', 'portfolio breakdown']):
        plot_pie_chart()
    else:
        response = assistant.ask(message)
        print(response)
           
    
        
              
             
         
                
        
    
              
            
    

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def fetch_stock_data(ticker, start_date, end_date):
  data=yf.download(ticker,start=start_date, end=end_date)
  name=ticker_to_name.get(ticker)
  return data,name

def calc_metric(data,moving_avg_period):
  data['Daily Return']=data['Close'].pct_change()  #daily return is the % change in a stocks CLOSING price from one day to the next, this will give you the %change od consecutive rows of the column 'close'
  data['Volatility']=data['Daily Return'].rolling(window=moving_avg_period).std() #volatility is the standard dev of daily return over a period.
  data['Moving Average']=data['Close'].rolling(window=moving_avg_period).mean() #moving avg is the mean of daily returns over a period.

  return data

ticker_to_name = { 
  "AAPL": "Apple",
 "GOOGL": "Alphabet", 
 "MSFT": "Microsoft", 
 "AMZN": "Amazon",
  "TSLA": "Tesla" } 
tickers = list(ticker_to_name.keys())
ticker_real_names = list(ticker_to_name.values())
features=["volatility","closing price","moving average","daily return"]


def plot_data(ticker,data,feature,name):
  plt.figure(figsize=(12,6))
  if feature=="closing price":
    plt.plot(data['Close'],label="close price", color='blue')

  elif feature=="moving average"  :
   plt.plot(data['Moving Average'], label='moving avg', color='red')
  elif feature=="volatility":
   plt.plot(data['Volatility'],label="volatility",color='green')
  elif feature=="daily return" :
    plt.plot(data['Daily Return'],label='daily returns',color='red')
  else:
    plt.plot(data['Close'],label="close price", color='blue')    

  plt.xlabel('Date')
  plt.ylabel('Price')
  plt.title(f'{name} - {feature}')
  plt.legend()
  plt.show()

import tkinter as tk 
from tkinter import ttk 
from tkcalendar import DateEntry

class StockScreenerApp:
  def __init__(self,root):
    self.root=root
    self.root.title("stock screener")
    self.root.geometry("300x500")

    self.ticker_label=tk.Label(root,text="Ticker:")
    self.ticker_label.grid(row=0,column=0, padx=10,pady=10)
    self.ticker_dropdown=ttk.Combobox(root,value=list(ticker_to_name.values()),width=30,height=30)
    self.ticker_dropdown.grid(row=0,column=1,padx=10,pady=10)
    self.ticker_dropdown.set(ticker_real_names[0])

    self.features_label=tk.Label(root,text="features:")
    self.features_label.grid(row=3,column=0,padx=10,pady=10)
    self.features_dropdown=ttk.Combobox(root,value=features,width=30,height=30)
    self.features_dropdown.grid(row=3,column=1,padx=10,pady=10)

    self.start_label=tk.Label(root,text="Start date:")
    self.start_label.grid(row=1,column=0,padx=10,pady=10)
    self.start_entry=DateEntry(root,date_pattern='yyyy-mm-dd', width=30,height=30)
    self.start_entry.grid(row=1,column=1,padx=10,pady=10)

    self.end_label=tk.Label(root,text="End date:")
    self.end_label.grid(row=2,column=0,padx=10,pady=10)
    self.end_entry=DateEntry(root,date_pattern='yyyy-mm-dd',width=30,height=30)
    self.end_entry.grid(row=2,column=1,padx=10,pady=10)

    self.analyze_button=tk.Button(root,text="ANALYZE",command=self.analyze,font=("arial",8))
    self.analyze_button.grid(row=4,columnspan=2,padx=10,pady=10)
    self.metrics_label=tk.Label(root,text="Calculated Metrics")
    self.metrics_label.grid(row=5,column=0,columnspan=2,padx=10,pady=10)

    self.daily_return_label=tk.Label(root,text="")
    self.daily_return_label.grid(row=6,column=0,columnspan=2)

    self.volatility_label=tk.Label(root,text="")
    self.volatility_label.grid(row=7,column=0,columnspan=2)

    self.moving_avg_label=tk.Label(root,text="")
    self.moving_avg_label.grid(row=8,column=0,columnspan=2)
    

  def analyze(self):
   company_name=self.ticker_dropdown.get()
   ticker = [key for key, value in ticker_to_name.items() if value == company_name][0]
   end_date=self.end_entry.get()
   start_date=self.start_entry.get()
   feature=self.features_dropdown.get()


   data, name = fetch_stock_data(ticker, start_date, end_date)
   

   data=calc_metric(data,50)
   plot_data(ticker,data,feature,name)

   avg_daily_return = data['Daily Return'].mean() 
   avg_volatility = data['Volatility'].mean()
   latest_moving_average=data['Moving Average'].iloc[-1]

   self.daily_return_label.config(text=f"Average Daily Return: : {avg_daily_return:.4f}") 
   self.volatility_label.config(text=f"Average Volatility:{avg_volatility:.4f} ")
   self.moving_avg_label.config(text=f"Latest Moving Average:{latest_moving_average:.4f} ")

if __name__=="__main__":
  root=tk.Tk()
  app=StockScreenerApp(root)
  root.mainloop()  

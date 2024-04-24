import streamlit as st
import pandas as pd
from utils import *
import altair as alt
import datetime
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

# Command to run streamlit:
# streamlit run C:/Users/Patrick/Documents/projects/intraday-financial-dashboard/code/main.py

# Remove the issue of overwriting dataframes:https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
pd.options.mode.chained_assignment = None

# # Set up AWS credentials

#  Personal PC
# secrets = toml.load(".gitignore\secrets.toml")
# print(secrets)
# ACCESS_KEY = secrets['ACCESS_KEY']
# SECRET_KEY = secrets['SECRET_KEY']

#  Streamlit
ACCESS_KEY = st.secrets["ACCESS_KEY"]
SECRET_KEY = st.secrets["SECRET_KEY"]

################################


st.title('Intraday Financial Dashboard')
st.text_area(
    "By: Patrick Labadie",
    "This dashboard shows one day of equity and derivative quotes for every company listed in the S&P 500. The quotes are pulled every 5 minutes using Questrade's API, with "
    "the data stored on AWS cloud servers. "  
    "This idea to build my own historical financial database with intraday quotes came from my Master's thesis. Considering how expensive "
    "financial data became, a free alternative resource to conduct your own analysis comes in handy.",
    )
st.divider()
dropdown_ticker = st.selectbox('Type the ticker or select any stock from the S&P 500!', list_of_tickers)

filtered_df = get_dataframe_eq(dropdown_ticker)


open = filtered_df['lastTradePrice'].iloc[0]
close = filtered_df['lastTradePrice'].iloc[-1]
high = filtered_df['lastTradePrice'].max()
low = filtered_df['lastTradePrice'].min()
lower_limit = filtered_df['lastTradePrice'].min()*.995
upper_limit = filtered_df['lastTradePrice'].max()*1.011

# Create the charts using Altair
base = alt.Chart(filtered_df).encode(x={
      "field": "timestamp",
      "timeUnit": "yearmonthdatehoursminutes",
      "axis": {"title":"Date-Time", "labelAngle": 45}
    })

line =  base.mark_line(clip=True).encode(
    x={
      "field": "timestamp",
      "timeUnit": "yearmonthdatehoursminutes",
      "axis": {"title":"Date-Time", "labelAngle": 45}
    },
    y=alt.Y('lastTradePrice', scale=alt.Scale(domain=[lower_limit, upper_limit]))
)

bar = base.mark_bar(color='#1f77b4',size=1).encode(y='vol:Q')
chart = (bar + line).resolve_scale(y='independent').properties(width=600)
st.altair_chart(chart, use_container_width=True)

# Display Date
datedisplay = filtered_df['timestamp'].iloc[0][0:10]
st.subheader(f"Date: :blue[{datedisplay}]")


# Use columns to display the prices side-by-side
col1, col2 = st.columns(2)
# Configure the page layout
with col1:
    st.header("High:")
    st.header(high)

with col2:
    st.header("Low:")
    st.header(low)

####################################################
# GET INPUTS FOR OPTIONS CHART
#####################################################

st.title('Derivative Prices')

full_option_df = get_dataframe_opt(dropdown_ticker)


# Get the necessary values to search for the specific option 

# expiration_dates
friday = datetime.date.today() + datetime.timedelta( (4-datetime.date.today().weekday()) % 7 )
next_friday =  friday + datetime.timedelta(days=7)
two_fridays = next_friday + datetime.timedelta(days=14)
fr1 = friday.strftime("%d%b%y").lstrip("0")
fr2 = next_friday.strftime("%d%b%y").lstrip("0")
fr3 = two_fridays.strftime("%d%b%y").lstrip("0")
exp_dates = [str(fr1),str(fr2),str(fr3)]

# Strike Price
strike_prices = pd.unique(full_option_df['strike_price'])
strike_prices = sorted(strike_prices)
# strike_elements = int(len(strike_prices) * 0.1)
# start_index = (len(strike_prices) - strike_elements) //2
displayed_strikes = strike_prices_to_display(strike_prices,close)


# Display dropdowns 
drop_exp = st.selectbox('Select the expiration date:', exp_dates)
drop_strike_raw = st.selectbox('Select the strike price:', displayed_strikes)
drop_type = st.selectbox('Select the option type:', ["CALL","PUT"])

drop_strike = str(drop_strike_raw)
option_type = "C"
if drop_type == "PUT":
  option_type = "P"


df_opt_symbol = str(dropdown_ticker+drop_exp+option_type+drop_strike+'0')
print(df_opt_symbol)

#####################################################
# OPTIONS CHART - SHOWS lastTradePrice & Vol
#####################################################


try:
  options_df = full_option_df.loc[full_option_df['symbol']==df_opt_symbol]
  
  if options_df['bidPrice'].iloc[0] =="NaN":
     options_df['bidPrice'].iloc[0] = options_df['bidPrice'].iloc[1]
  if options_df['askPrice'].iloc[0] =="NaN":
     options_df['askPrice'].iloc[0] = options_df['askPrice'].iloc[1]

  print(options_df)
  # Create min/max to zoom in on graph
  lower_limit_opt = options_df['lastTradePrice'].min()*.995
  upper_limit_opt = options_df['lastTradePrice'].max()*1.011


  base = alt.Chart(options_df).encode(x={
        "field": "timestamp",
        "timeUnit": "yearmonthdatehoursminutes",
        "axis": {"title":"Date-Time", "labelAngle": 45}
      })

  line =  base.mark_line(clip=True).encode(
      x={
        "field": "timestamp",
        "timeUnit": "yearmonthdatehoursminutes",
        "axis": {"title":"Date-Time", "labelAngle": 45}
      },
      y=alt.Y('lastTradePrice', scale=alt.Scale(domain=[lower_limit_opt, upper_limit_opt]))
  )

  bar = base.mark_bar(color='#1f77b4',size=1).encode(y='vol:Q')
  chart = (bar + line).resolve_scale(y='independent').properties(width=600)
  st.altair_chart(chart, use_container_width=True)
except:
   st.header("No luck with this option chain, try another!")
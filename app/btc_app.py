from datetime import datetime

import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
from pytz import timezone

from inference import pred, get_current_close_price, get_df

st.title('Bitcoin Closing Price Prediction')
st.header('Using Bi-Directional LSTM')
st.markdown('created by: **MoonShots**')

feature_df, pred = pred()
pred = round(pred, 1)
actual = get_current_close_price()

st.markdown(
    f'<p style="background-color:#d1eeea;color:#000000;font-size:24px;border-radius:2%;"><b> Prediction for date {datetime.now().strftime("%d-%m-%Y")} <b></p>',
    unsafe_allow_html=True)
st.markdown("""<style>div.stButton > button:first-child {background-color: #d1eeea;}</style>""", unsafe_allow_html=True)
submit = st.button('Refresh to get latest price')
if submit:
    actual = get_current_close_price()
    st.text(f'last refreshed on {datetime.now(timezone("Europe/Berlin")).strftime("%Y-%m-%d %I:%M:%S %p")}')

close_price_df = get_df()

heat_map = ff.create_annotated_heatmap([[pred, actual]], annotation_text=[
    [f'Predicted Price <br> <b>${round(pred, 1)}<b>', f'Latest Price <br> <b>${actual}<b>']], colorscale='Teal',
                                       hoverinfo='none')
for i in range(len(heat_map.layout.annotations)):
    heat_map.layout.annotations[i].font.size = 25
st.plotly_chart(heat_map)
#st.markdown(f'Absolute Error: **${round(abs(pred - actual), 2)}**')
#st.markdown(f'Percentage Error: **{round((abs(pred - actual) / actual) * 100, 2)}%**')
st.markdown(
    f'<p style="background-color:#d1eeea;color:#000000;font-size:24px;border-radius:2%;"><b> BTC Closing Prices Data<b></p>',
    unsafe_allow_html=True)
bar_plot = go.Figure()
bar_plot.add_trace(go.Bar(x=close_price_df['Date'], y=close_price_df['Close'],
                          marker=dict(color=close_price_df['Close'], colorscale='Teal')))
bar_plot.update_layout(title="Bitcoin Actual Closing Price", xaxis_title="Date", yaxis_title="BTC Price(USD)")
bar_plot.update_traces(dict(marker_line_width=0))
st.plotly_chart(bar_plot)

st.markdown('<p style="background-color:#d1eeea;color:#000000;font-size:24px;border-radius:2%;"><b> Features<b></p>',
            unsafe_allow_html=True)
st.dataframe(data=feature_df.reset_index(drop=True).tail(10))

st.markdown(
    '<p style="background-color:#d1eeea;color:#000000;font-size:24px;border-radius:2%;"><b> Data Resource & Reference<b></p>',
    unsafe_allow_html=True)
st.write('1. [Investpy](https://investpy.readthedocs.io/_api/crypto.html)')
st.write('2. [Quandl](https://www.quandl.com/data/BCHAIN)')
st.write('3. [bitinfocharts](https://bitinfocharts.com/comparison/bitcoin-price.html#3y)')
st.write('4. [Investing](https://www.investing.com/)')

st.markdown('<p style="background-color:#d1eeea;color:#000000;font-size:24px;border-radius:2%;"><b> Contact Us<b></p>',
            unsafe_allow_html=True)
st.write('1. [Linkedin](https://www.linkedin.com/in/parth-modi-5587a1148/)')
st.write('2. [GitHub](https://github.com/Parth527)')
st.write('3. Email-modiparth527@gmail.com')

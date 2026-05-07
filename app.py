# app.py

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Stock Market Trend Analyzer",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #020617 0%,
        #081120 30%,
        #0B1120 60%,
        #111827 100%
    );
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(3, 7, 18, 0.96);
    border-right: 1px solid rgba(0,229,255,0.15);
}

/* Title */
.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #00E5FF;
    margin-top: 10px;
    letter-spacing: 1px;
}

/* Subtitle */
.sub-title {
    color: #94A3B8;
    font-size: 17px;
    margin-top: -10px;
}

/* Metric Cards */
.metric-card {
    background: rgba(15, 23, 42, 0.70);
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0px 0px 25px rgba(0,229,255,0.08);
    backdrop-filter: blur(12px);
}

/* Logo Container */
.logo-container {
    background: rgba(255,255,255,0.03);
    border-radius: 24px;
    padding: 8px;
    border: 1px solid rgba(0,255,180,0.15);
    box-shadow:
        0px 0px 30px rgba(0,255,180,0.12),
        0px 0px 50px rgba(0,229,255,0.08);
}

/* Buttons */
.stButton>button,
.stDownloadButton>button {
    background: linear-gradient(
        90deg,
        #00E5FF,
        #2563EB
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 22px;
    font-weight: 700;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

/* Input Fields */
.stTextInput input,
.stDateInput input {
    background-color: rgba(255,255,255,0.05);
    color: white;
    border-radius: 10px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #00E5FF;
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([1.4, 6])

with col1:

    st.markdown('<div class="logo-container">', unsafe_allow_html=True)

    # USE ONLINE BULL IMAGE
    st.image(
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop",
        width=220
    )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown(
        """
        <div class='main-title'>
            STOCK MARKET TREND ANALYZER
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='sub-title'>
            Real-Time Financial Analysis • Smart Insights • Market Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    current_time = datetime.now().strftime("%d %B %Y | %I:%M:%S %p")

    st.markdown(
        f"""
        <span style='color:#00E5FF;'>📅 {current_time}</span>
        &nbsp;&nbsp;&nbsp;
        <span style='color:#00FF99;'>🟢 Market Open</span>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 Analysis Settings")

ticker = st.sidebar.text_input(
    "Enter Stock Symbol",
    value="NVDA"
)

start_date = st.sidebar.date_input(
    "Start Date",
    datetime(2024, 1, 1)
)

end_date = st.sidebar.date_input(
    "End Date",
    datetime.today()
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 🔥 Popular Stocks

- NVDA
- AAPL
- TSLA
- META
- MSFT
- RELIANCE.NS
- INFY.NS
""")

# =========================================================
# FETCH DATA
# =========================================================

@st.cache_data
def load_stock_data(symbol, start, end):

    stock_df = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=True
    )

    return stock_df

data = load_stock_data(
    ticker,
    start_date,
    end_date
)

if data.empty:
    st.error("❌ No stock data found.")
    st.stop()

# =========================================================
# DATA PROCESSING
# =========================================================

close_price = data['Close'].squeeze()
high_price = data['High'].squeeze()
low_price = data['Low'].squeeze()
volume_price = data['Volume'].squeeze()

# Daily Return
data['Daily Return'] = close_price.pct_change()

# Moving Averages
data['20 MA'] = close_price.rolling(window=20).mean()
data['50 MA'] = close_price.rolling(window=50).mean()

# Volatility
volatility = float(data['Daily Return'].std())

# Price Metrics
highest_price = float(high_price.max())
lowest_price = float(low_price.min())
current_price = float(close_price.iloc[-1])
starting_price = float(close_price.iloc[0])

# Growth
growth = (
    (current_price - starting_price)
    / starting_price
) * 100

trend = "Bullish 📈" if growth > 0 else "Bearish 📉"

# =========================================================
# METRIC CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <h4 style='color:#00E5FF;'>Current Price</h4>
        <h1>${current_price:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <h4 style='color:#00FF99;'>Highest Price</h4>
        <h1>${highest_price:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
        <h4 style='color:#FF4B4B;'>Lowest Price</h4>
        <h1>${lowest_price:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:

    growth_color = "#00FF99" if growth > 0 else "#FF4B4B"

    st.markdown(f"""
    <div class="metric-card">
        <h4 style='color:#00E5FF;'>Total Growth</h4>
        <h1 style='color:{growth_color};'>
            {growth:.2f}%
        </h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# STOCK TREND GRAPH
# =========================================================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=close_price,
        mode='lines',
        name='Closing Price',
        line=dict(color='#00E5FF', width=3),
        fill='tozeroy',
        fillcolor='rgba(0,229,255,0.08)'
    )
)

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data['20 MA'],
        mode='lines',
        name='20 Day MA',
        line=dict(color='#00FF99', width=2)
    )
)

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data['50 MA'],
        mode='lines',
        name='50 Day MA',
        line=dict(color='#FF4B4B', width=2)
    )
)

fig.update_layout(
    title=f"{ticker} Price Trend & Moving Averages",
    template='plotly_dark',
    height=620,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode='x unified'
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# SECOND ROW
# =========================================================

chart_col1, chart_col2 = st.columns(2)

# =========================================================
# RETURNS GRAPH
# =========================================================

with chart_col1:

    returns_fig = go.Figure()

    returns_fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Daily Return'],
            marker_color=[
                '#00FF99' if val >= 0 else '#FF4B4B'
                for val in data['Daily Return']
            ],
            name="Daily Returns"
        )
    )

    returns_fig.update_layout(
        title="Daily Returns (%)",
        template='plotly_dark',
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    st.plotly_chart(
        returns_fig,
        use_container_width=True
    )

# =========================================================
# VOLUME GRAPH
# =========================================================

with chart_col2:

    volume_fig = go.Figure()

    volume_fig.add_trace(
        go.Bar(
            x=data.index,
            y=volume_price,
            marker_color='rgba(0,229,255,0.7)',
            name='Trading Volume'
        )
    )

    volume_fig.update_layout(
        title="Trading Volume",
        template='plotly_dark',
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    st.plotly_chart(
        volume_fig,
        use_container_width=True
    )

# =========================================================
# ANALYSIS SECTION
# =========================================================

st.markdown("## 📈 Market Insights")

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:

    st.markdown(f"""
    <div class="metric-card">

    ### 📊 Technical Analysis

    - Market Trend: {trend}
    - Volatility Score: {volatility:.4f}
    - Average Return: {data['Daily Return'].mean():.4f}
    - Trading Days: {len(data)}

    </div>
    """, unsafe_allow_html=True)

with analysis_col2:

    if growth > 0:

        recommendation = """
        ✅ Strong upward momentum detected.

        ✅ Moving averages support bullish continuation.

        ✅ Trading activity indicates investor confidence.
        """

    else:

        recommendation = """
        ⚠ Bearish momentum detected.

        ⚠ Price movement indicates downward pressure.

        ⚠ Risk management strategies recommended.
        """

    st.markdown(f"""
    <div class="metric-card">

    ### 🧠 AI-Based Insight

    {recommendation}

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# DATA PREVIEW
# =========================================================

st.markdown("## 📁 Recent Market Data")

st.dataframe(
    data.tail(20),
    use_container_width=True
)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================

csv = data.to_csv().encode('utf-8')

st.download_button(
    label="⬇ Download Processed CSV",
    data=csv,
    file_name=f"{ticker}_analysis.csv",
    mime='text/csv'
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<div style='text-align:center; color:gray;'>

© 2026 Stock Market Trend Analyzer | Built with Streamlit | Data by Yahoo Finance

⚠ Educational Purpose Only — Not Financial Advice

</div>
""", unsafe_allow_html=True)
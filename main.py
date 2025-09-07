import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('https://www.dropbox.com/scl/fi/20rqvoayhfq55oi6vbkwp/NAV_-Clone.csv?rlkey=ovqiv1fwpxtauy0o5f0zrecya&dl=1')

def adjusted_NAV(df):
    df_1 = df.dropna().copy()
    df_2 = df[df.isna().any(axis = 1)].iloc[1:,:].copy()
    df_2.columns = ['Date','Settle','Amount','NA']
    df_1['ReportDate'] = pd.to_datetime(df_1['ReportDate'].astype(int), format = '%Y%m%d')
    df_2['Date'] = pd.to_datetime(df_2['Date'].astype(int), format = '%Y%m%d')
    
    s_1 = df_1.set_index('ReportDate')['Total'].astype(float)
    s_2 = df_2.set_index('Date')['Amount'].astype(float)
    x = pd.concat([s_1.rename('NAV'), s_1.diff().rename('pnl'), s_2.rename('cash')], axis = 1).fillna(0)
    x['adj_pnl'] = x['pnl'] - x['cash']
    x['adj_NAV'] = x['NAV'].iloc[0] + x['adj_pnl'].cumsum()
    return x

s = adjusted_NAV(df)['adj_NAV'].rename('adj_NAV')

nav_series = s.sort_index()
nav_pct = ((nav_series / nav_series.iloc[0] - 1) * 100).round(2)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=nav_series.index,
    y=nav_series.values,
    mode='lines+markers',
    name='NAV Absolute',
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=nav_series.index,
    y=nav_pct.values,
    mode='lines+markers',
    name='NAV % Change',
    yaxis='y2',
    line=dict(color='green')
))

fig.update_layout(
    # title='NAV Over Time',
    # xaxis_title='Date',
    yaxis=dict(
        # title='NAV Absolute',
        side='left',
        showgrid=True
    ),
    yaxis2=dict(
        title='% Change',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend=dict(x=0.01, y=0.99),
    margin=dict(l=40, r=40, t=40, b=40),  # tight margins
    autosize=True

)

fig.write_html("index.html", include_plotlyjs='cdn')
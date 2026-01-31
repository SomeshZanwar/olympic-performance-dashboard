"""
🥇 Interactive Olympic Performance Dashboard.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.data_loader import load_and_clean_data, compute_kpis
from src.config import RAW_DATA_PATH, FIGURES_DIR


# Config
st.set_page_config(
    page_title="Olympic Performance Dashboard 🥇",
    page_icon="🥇", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🥇 Interactive Olympic Performance Analytics")
st.markdown("**120+ years of Olympic history • 271k athletes • 1896-2016**")

# Load data (cached ~3s first load)
@st.cache_data
def get_data():
    return load_and_clean_data()

df = get_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
years = st.sidebar.slider("Year Range", 1896, 2016, (1896, 2016))
country = st.sidebar.selectbox("Country", ['All'] + sorted(df['NOC'].unique()))
sport = st.sidebar.selectbox("Sport", ['All'] + sorted(df['Sport'].unique())[:20])
medals = st.sidebar.multiselect("Medal Types", ['Gold', 'Silver', 'Bronze'], default=['Gold', 'Silver', 'Bronze'])

# Filter
df_filt = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])].copy()
if country != 'All': df_filt = df_filt[df_filt['NOC'] == country]
if sport != 'All': df_filt = df_filt[df_filt['Sport'] == sport]
if medals != ['Gold', 'Silver', 'Bronze']: 
    df_filt = df_filt[df_filt['Medal'].isin(medals)]

# Page tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Overview", "🥇 Medal Tally", "🇺🇸 Country Trends", "🏅 Athletes", "📈 Trends"])

with tab1:
    st.header("🏠 Games Overview")
    
    kpis = compute_kpis(df_filt)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🥇 Athletes", f"{kpis['total_athletes']:,.0f}")
    c2.metric("🏅 Countries", kpis['total_countries'])
    c3.metric("⚽ Sports", kpis['total_sports'])
    c4.metric("🥇🥈🥉 Medals", f"{kpis['total_medals']:,.0f}")
    
    # Medal pie
    medals_pie = df_filt['Medal'].value_counts()
    fig1 = px.pie(values=medals_pie.values, names=medals_pie.index, hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Top countries
    top_countries = df_filt[df_filt['Has_Medal']]['NOC'].value_counts().head(12)
    fig2 = px.bar(x=top_countries.values, y=top_countries.index, orientation='h')
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("🥇 Medal Tally")
    
    medal_df = df_filt[df_filt['Has_Medal']]
    if len(medal_df) > 0:
        tally = medal_df.groupby(['NOC', 'Medal']).size().unstack(fill_value=0)
        tally['Total'] = tally.sum(axis=1)
        tally = tally.sort_values('Total', ascending=False).head(20)
        st.dataframe(tally)
        
        fig_tally = px.bar(tally.iloc[:, :-1].iloc[::-1], 
                          orientation='h', title="Top Countries by Medal Type")
        st.plotly_chart(fig_tally, use_container_width=True)

with tab3:
    st.header("🇺🇸 Country Performance Over Time")
    
    medal_year = df_filt[df_filt['Has_Medal']].groupby(['Year', 'NOC'])['Medal'].count().reset_index(name='Medals')
    if country == 'All':
        top_nocs = medal_year['NOC'].value_counts().head(8).index
        medal_year = medal_year[medal_year['NOC'].isin(top_nocs)]
    
    fig_country = px.line(medal_year, x='Year', y='Medals', color='NOC')
    st.plotly_chart(fig_country, use_container_width=True)

with tab4:
    st.header("🏅 Athlete Insights")
    
    col1, col2 = st.columns(2)
    with col1:
        fig_age = px.histogram(df_filt, x='Age', color='Sex', nbins=40,
                              title="Age Distribution")
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        medalists = df_filt[df_filt['Has_Medal']]
        fig_hw = px.scatter(medalists, x='Height', y='Weight', 
                           color='Sex', size='Age', hover_name='Name',
                           title="Height vs Weight (Medalists)")
        st.plotly_chart(fig_hw, use_container_width=True)
    
    # Top athletes
    top_athletes = medalists.groupby(['Name', 'NOC'])['Medal'].count().sort_values(ascending=False).head(15)
    st.subheader("🥇 Top Medalists")
    st.dataframe(top_athletes)

with tab5:
    st.header("📈 Olympic Evolution")
    
    col1, col2 = st.columns(2)
    with col1:
        events_year = df_filt.groupby('Year')['Event'].nunique()
        fig_events = px.line(x=events_year.index, y=events_year.values,
                            title="Events per Olympics")
        st.plotly_chart(fig_events)
    
    with col2:
        athletes_year = df_filt.groupby('Year')['Name'].nunique()
        fig_athletes = px.line(x=athletes_year.index, y=athletes_year.values,
                              title="Athletes per Olympics")
        st.plotly_chart(fig_athletes)

st.markdown("---")
st.markdown("*Built with Streamlit + Plotly | Data: Kaggle Olympics[web:105]*")
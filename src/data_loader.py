"""
Data loading and cleaning for Olympic dashboard.
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from src.config import RAW_DATA_PATH


@st.cache_data
def load_and_clean_data(_raw_path=RAW_DATA_PATH) -> pd.DataFrame:
    """Load + preprocess Olympic data (cached)."""
    
    df = pd.read_csv(_raw_path)
    print(f"✅ Loaded {len(df):,} rows")
    
    # Clean medals
    df['Medal'] = df['Medal'].fillna('NA')
    medal_order = ['Gold', 'Silver', 'Bronze', 'NA']
    df['Medal'] = pd.Categorical(df['Medal'], categories=medal_order, ordered=True)
    
    # Clean numerics (fill median)
    for col in ['Age', 'Height', 'Weight']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())
    
    # Clean team names
    df['Team'] = df['Team'].str.strip()
    
    # Derived columns
    df['Has_Medal'] = df['Medal'] != 'NA'
    
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    """Dashboard summary metrics."""
    medal_df = df[df['Has_Medal']]
    
    return {
        'total_athletes': len(df['Name'].unique()),
        'total_countries': len(df['NOC'].unique()),
        'total_sports': len(df['Sport'].unique()),
        'total_medals': len(medal_df),
        'top_country': medal_df['NOC'].value_counts().index[0],
        'top_sport': medal_df['Sport'].value_counts().index[0],
        'years_range': (df['Year'].min(), df['Year'].max())
    }
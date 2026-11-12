from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv(Path(__file__).parent / 'zomato_clean.csv')

# cleaning
df['rate'] = df['rate'].astype(str).str.replace('/5', '').str.strip()
df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(str).str.replace(',', '').str.strip()
df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'], errors='coerce')
df = df.rename(columns={'approx_cost(for two people)': 'cost', 'listed_in(type)': 'meal_type', 'listed_in(city)': 'city'})
#df = df.drop(columns=['url', 'address', 'phone', 'dish_liked', 'reviews_list', 'menu_item'])
df = df.dropna(subset=['rate', 'location'])

# page config
st.set_page_config(page_title="Bangalore Food Dashboard", layout="wide")
st.title("🍽️ Bangalore Restaurant Analysis")
st.markdown("Exploring 40,000+ restaurants across Bangalore using Zomato data.")

#sidebar filters

st.sidebar.header("Filters")
locations = ['All'] + sorted(df['location'].unique().tolist())
selected_location = st.sidebar.selectbox("Select Location", locations)

if selected_location != 'All':
    df = df[df['location'] == selected_location]

# top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Restaurants", f"{len(df):,}")
col2.metric("Avg Rating", f"{df['rate'].mean():.1f} / 5")
col3.metric("Avg Cost for Two", f"₹{df['cost'].mean():.0f}")
col4.metric("Locations", df['location'].nunique())

st.divider()

# top locations bar chart
st.subheader("Top 15 Locations by Restaurant Count")
top_locations = df['location'].value_counts().head(15).reset_index()
top_locations.columns = ['location', 'count']
fig1 = px.bar(top_locations, x='location', y='count', color='count', color_continuous_scale='Oranges')
st.plotly_chart(fig1, use_container_width=True)

# cuisine distribution
st.subheader("Top 10 Cuisines")
top_cuisines = df['cuisines'].value_counts().head(10).reset_index()
top_cuisines.columns = ['cuisine', 'count']
fig2 = px.bar(top_cuisines, x='count', y='cuisine', orientation='h', color='count', color_continuous_scale='Blues')
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# rating distribution
st.subheader("Rating Distribution")
fig3 = px.histogram(df, x='rate', nbins=20, color_discrete_sequence=['#f97316'])
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# cost vs rating
st.subheader("Cost vs Rating")
fig4 = px.scatter(df, x='cost', y='rate', opacity=0.3, 
                  color_discrete_sequence=['#3b82f6'],
                  labels={'cost': 'Cost for Two (₹)', 'rate': 'Rating'})
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# online order vs rating
st.subheader("Online Order vs Average Rating")
online_rating = df.groupby('online_order')['rate'].mean().reset_index()
fig5 = px.bar(online_rating, x='online_order', y='rate', 
              color='online_order', color_discrete_sequence=['#f97316', '#3b82f6'],
              labels={'online_order': 'Accepts Online Orders', 'rate': 'Avg Rating'})
st.plotly_chart(fig5, use_container_width=True)


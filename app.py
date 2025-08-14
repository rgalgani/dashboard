import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import leafmap.foliumap as leafmap

# Set Streamlit page config
st.set_page_config(page_title="Ethiopia - Context & Programme Monitoring Dashboard", layout="wide")

# App title
st.title("🇪🇹 Ethiopia - Context & Programme Monitoring Dashboard")

# GitHub raw base path
GITHUB_BASE = "https://raw.githubusercontent.com/rgalgani/dashboard/main/"

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Context", "📈 M&E", "🔍 Ask the Data!"])

# ---------- TAB 1: CONTEXT ----------
with tab1:
    st.header("📊 Conflict Trends and Contextual Data")

    # Load ACLED data
    @st.cache_data
    def load_acled():
        url = GITHUB_BASE + "ACLED.csv"
        df = pd.read_csv(url, parse_dates=['event_date'])
        return df

    acled = load_acled()

    # --- Charts Section ---
    st.subheader("Violent Events Over Time")

    # Line Chart: monthly count
    acled['event_date'] = pd.to_datetime(acled['event_date'])
    timeseries = acled.groupby(acled['event_date'].dt.to_period("M")).size().reset_index(name="count")
    timeseries['event_date'] = timeseries['event_date'].dt.to_timestamp()

    fig_line = px.line(timeseries, x="event_date", y="count", labels={'event_date': 'Date', 'count': 'Number of Events'})
    st.plotly_chart(fig_line, use_container_width=True)

    # Bar Chart: events by admin1
    st.subheader("Violent Events by Region (Admin1)")
    if 'admin1' in acled.columns:
        region_counts = acled['admin1'].value_counts().reset_index()
        region_counts.columns = ['Region', 'Events']
        fig_bar = px.bar(region_counts, x='Region', y='Events', text='Events')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No 'admin1' column found in the data.")

    # --- Map Section ---
    st.subheader("🗺️ Map of Violent Events")

    # Filter for rows with valid coordinates
    acled_map = acled.dropna(subset=['latitude', 'longitude'])

    if not acled_map.empty:
        gdf = gpd.GeoDataFrame(
            acled_map,
            geometry=gpd.points_from_xy(acled_map.longitude, acled_map.latitude),
            crs="EPSG:4326"
        )

        # Initialize map
        m = leafmap.Map(center=[9.145, 40.4897], zoom=5)

        # Add events layer
        m.add_gdf(
            gdf[['geometry']], 
            layer_name="Violent Events", 
            zoom_to_layer=True
        )

        m.to_streamlit(height=600)
    else:
        st.warning("No geolocated violent events found in the dataset.")

# ---------- TAB 2: M&E ----------
with tab2:
    st.header("📈 Monitoring & Evaluation")
    st.info("This section will be developed later.")

# ---------- TAB 3: Ask the Data! ----------
with tab3:
    st.header("🔍 Explore the Data")
    st.info("This section will be developed later.")
import streamlit as st
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
import pandas as pd
import pymysql
import plotly.express as px
import os
import json


def get_connection():
    # Replace these with your actual MySQL credentials
    username = "root"
    password = "Harsha%40123"
    hostname = "localhost"
    database = "phonepe"

    engine = create_engine(f"mysql+pymysql://{'root'}:{'Harsha%40123'}@{'localhost'}/{'phonepe'}")
    return engine.raw_connection()

def show_table_columns():
    conn = get_connection()
    df = pd.read_sql("SHOW COLUMNS FROM agg_transaction", conn)
    st.write("Table Columns in agg_transaction:", df)
    conn.close()

def get_years():
    conn = get_connection()
    df = pd.read_sql("SELECT DISTINCT Years FROM agg_transaction ORDER BY Years", conn)
    conn.close()
    return df["Years"].tolist()

def get_all_states_by_year(year):
    conn = get_connection()
    query = f"""
    SELECT 
    States, 
    ROUND(AVG(lat), 4) AS Latitude, 
    ROUND(AVG(lon), 4) AS Longitude, 
    ROUND(SUM(Transaction_amount), 2) AS Total_Transaction_Value
    FROM agg_transaction
    WHERE Years = {year}
    GROUP BY States
    ORDER BY Total_Transaction_Value DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_all_districts_by_year(year):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"""
    SELECT District, lat AS Latitude, lon AS Longitude, ROUND(SUM(Metric_amount), 2) AS Total_Metric_Value
    FROM map_transaction
    WHERE Years = {year}
    GROUP BY District, lat, lon
    ORDER BY Total_Metric_Value DESC
    LIMIT 30;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(results, columns=["District", "Latitude", "Longitude", "Total_Metric_Value"])

def get_top_pincodes_by_year(year):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"""
    SELECT Pincodes, lat AS Latitude, lon AS Longitude, ROUND(SUM(Pin_amount), 2) AS Total_Pincode_Value
    FROM top_transaction
    WHERE Years = {year}
    GROUP BY Pincodes, lat, lon
    ORDER BY Total_Pincode_Value DESC
    LIMIT 30;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(results, columns=["Pincode", "Latitude", "Longitude", "Total_Pincode_Value"])

def show_growth_regions():
    conn = get_connection()
    query = """
    SELECT States, Transaction_type, COUNT(*) AS Growth_Quarters
    FROM agg_trans
    WHERE Trend = 'Growth'
    GROUP BY States, Transaction_type
    HAVING COUNT(*) >= 3;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Normalize column names to lowercase for consistency
    df.columns = df.columns.str.strip().str.lower()

    st.subheader("Consistently Growing Regions")

    # Defensive check: ensure required columns exist
    required_cols = {'growth_quarters', 'transaction_type'}
    if required_cols.issubset(df.columns):
        fig_hist_growth = px.histogram(
            df,
            x='growth_quarters',
            color='transaction_type',
            title="Distribution of Growth Quarters"
        )
        st.plotly_chart(fig_hist_growth)
    else:
        st.warning("Required columns missing in query result. Please check schema or aliases.")

def show_declining_regions():
    conn = get_connection()
    query = """
    SELECT States, Transaction_type, COUNT(*) AS Non_Growth_Quarters
    FROM agg_trans
    WHERE Trend IN ('Decline', 'Stable')
    GROUP BY States, Transaction_type
    HAVING COUNT(*) >= 3;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    st.subheader("Declining or Stagnant Regions")
    fig = px.bar(df, x='States', y='Non_Growth_Quarters', color='Transaction_type', title="Non-Growth Quarters by State")
    st.plotly_chart(fig)

def show_volatility():
    conn = get_connection()
    query = """
    WITH joined AS (SELECT curr.States, curr.Device_brand, curr.Years, curr.Quarter,
            curr.User_count - prev.User_count AS UserCount_Change,
            curr.AppOpens - prev.AppOpens AS AppOpens_Change,
            curr.Usage_percentage - prev.Usage_percentage AS UsageChange
    FROM agg_user AS curr
    JOIN agg_user AS prev ON curr.States = prev.States
                AND curr.Device_brand = prev.Device_brand
                AND curr.Years = prev.Years
                AND curr.Quarter = prev.Quarter + 1)
    SELECT States, Device_brand, Years, Quarter,
            ROUND(AVG(UserCount_Change), 2) AS Avg_UserCount_Change,
            ROUND(AVG(AppOpens_Change), 2) AS Avg_AppOpens_Change,
            ROUND(AVG(UsageChange), 2) AS Avg_UsageChange
    FROM joined
    GROUP BY States, Device_brand, Years, Quarter
    ORDER BY States, Device_brand, Years, Quarter
    LIMIT 50;
    """
    df = pd.read_sql(query, get_connection())
    df.columns = df.columns.str.strip().str.lower()

    if not all(col in df.columns for col in ['years', 'quarter']):
        st.error("Missing required columns.")
        return

    df['period'] = df['years'].astype(str) + " Q" + df['quarter'].astype(str)
    st.subheader("Device-Specific Volatility Over Time")

    brand = st.selectbox("Select Device Brand", df['device_brand'].unique())
    metric_map = {
        "User Count Change": "avg_usercount_change",
        "App Opens Change": "avg_appopens_change",
        "Usage % Change": "avg_usagechange"
    }
    metric_label = st.selectbox("Select Volatility Metric", list(metric_map.keys()))
    metric = metric_map[metric_label]

    filtered = df[df['device_brand'] == brand]
    fig = px.line(filtered, x='period', y=metric, color='states', markers=True,
              title=f"{metric_label} Trend for {brand}")
    st.plotly_chart(fig)

def show_map_snapshot(year, quarter):
    conn = get_connection()
    query = f"""
    SELECT States, Years, Quarter, Transaction_type, Transaction_amount, Trend, lat, lon
    FROM agg_trans
    WHERE Years = {year} AND Quarter = {quarter};
    """
    df = pd.read_sql(query, conn)
    conn.close()
    st.subheader(f"Map Snapshot: {year} Q{quarter}")
    fig = px.scatter_mapbox(df, lat='lat', lon='lon', color='Trend',
                            size='Transaction_amount', hover_name='States',
                            mapbox_style='carto-positron', zoom=4,
                            title=f"Transaction Trends in {year} Q{quarter}")
    st.plotly_chart(fig)

def show_trend_summary():
    conn = get_connection()
    query = """
    SELECT States,
    COUNT(CASE WHEN Trend = 'Growth' THEN 1 END) AS Growth,
    COUNT(CASE WHEN Trend = 'Decline' THEN 1 END) AS Decline,
    COUNT(CASE WHEN Trend = 'Stable' THEN 1 END) AS Stable,
    COUNT(CASE WHEN Trend = 'No Data' THEN 1 END) AS No_Data
    FROM agg_trans
    GROUP BY States;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    st.subheader("Strategic Trend Summary by State")
    selected_state = st.selectbox("Select State for Pie Chart", df['States'].unique())
    state_data = df[df['States'] == selected_state].melt(id_vars='States', 
                                                        value_vars=['Growth', 'Decline', 'Stable', 'No_Data'],
                                                        var_name='Trend', value_name='Count')

    fig_pie = px.pie(state_data, names='Trend', values='Count',
                    title=f"Trend Breakdown for {selected_state}")
    st.plotly_chart(fig_pie)

def show_pincode_engagement_map(year, quarter):
    conn = get_connection()
    
    query = f"""
    SELECT m.States, m.Years, m.Quarter, m.RegisteredUsers, m.AppOpens,
        ROUND(m.AppOpens / NULLIF(m.RegisteredUsers, 0), 2) AS Engagement_rate, t.Total_pin_amount,
        ROUND(t.Total_pin_amount / NULLIF(m.RegisteredUsers, 0), 2) AS Spend_per_user, t.lat, t.lon
    FROM map_user m
    JOIN (SELECT States, Years, Quarter, AVG(lat) AS lat, AVG(lon) AS lon, SUM(Pin_amount) AS Total_pin_amount
	  FROM top_transaction
	  GROUP BY States, Years, Quarter) t ON m.States = t.States AND m.Years = t.Years AND m.Quarter = t.Quarter;
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    df.columns = df.columns.str.strip().str.lower()

    st.subheader(f"Pincode Engagement Snapshot: {year} Q{quarter}")
    metric = st.selectbox("Select Metric", ["engagement_rate", "spend_per_user", "total_pin_amount"])

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        size=metric,
        color=metric,
        hover_name="states",
        hover_data=["registeredusers", "appopens", "total_pin_amount", "spend_per_user"],
        mapbox_style="carto-positron",
        zoom=4,
        title=f"{metric.replace('_', ' ').title()} by Location"
    )
    st.plotly_chart(fig)

def show_insurance_growth():
    st.subheader("Insurance Growth by State")

    df = pd.read_sql("""
        SELECT States, Years, Quarter, SUM(Transaction_amount) AS Total
        FROM agg_insurance
        GROUP BY States, Years, Quarter
        ORDER BY States, Years, Quarter;
    """, get_connection())

    if df.empty:
        st.warning("No insurance data found.")
        return

    df = df.sort_values(['States', 'Years', 'Quarter'])
    df['trend'] = df.groupby('States')['Total'].diff().gt(0).map({True: 'Growth', False: 'No Growth'})
    summary = df[df['trend'] == 'Growth'].groupby('States').size().reset_index(name='Growth Quarters')

    fig = px.bar(
    summary,
    x='States',
    y='Growth Quarters',
    color='Growth Quarters',  # 🌡️ Color scale based on value
    color_continuous_scale='Viridis',
    title="Insurance Growth Quarters by State"
    )
    st.plotly_chart(fig)    

st.set_page_config(layout='wide')
st.title('PhonePe Transaction Insights')

with st.sidebar:
    selected_menu = st.selectbox("Main Menu", ["Select", "Home", "Business Case Study"])

if "map_rendered" not in st.session_state:
    st.session_state.map_rendered = False
# Home Page
if selected_menu == 'Home':
    
    level = st.selectbox("Choose Level", ["Top performing States", "Top performing Districts", "Top performing Pincodes"])

    # Select the year
    years = st.selectbox('Select The Year', get_years())

    # Fetch and display based on level
    if level == "Top performing States":
        if "home_map_rendered" not in st.session_state:
            st.session_state.home_map_rendered = False

        agg_trans_df = get_all_states_by_year(years)

        if not agg_trans_df.empty:
            st.subheader(f"Top 10 States by Transaction Value in {years}")
            st.dataframe(agg_trans_df.head(10))

            if not st.session_state.home_map_rendered:
                fig = px.scatter_mapbox(
                    agg_trans_df,
                    lat='Latitude',
                    lon='Longitude',
                    size='Total_Transaction_Value',
                    color='Total_Transaction_Value',
                    hover_name='States',
                    color_continuous_scale='Rainbow',
                    size_max=40,
                    zoom=4,
                    mapbox_style='carto-positron',
                    title=f"Top Performing States in {years} (by Transaction Value)"
                )
                st.plotly_chart(fig, use_container_width=True, key=f"home_map_{years}")
                st.session_state.home_map_rendered = True
        else:
            st.warning(f"No data found for the year {years}")
            st.session_state.home_map_rendered = False

    elif level == "Top performing Districts":
        if "district_map_rendered" not in st.session_state:
            st.session_state.district_map_rendered = False

        map_trans_df = get_all_districts_by_year(years)

        if not map_trans_df.empty:
            st.subheader(f"Top 10 Districts by Metric Value in {years}")
            st.dataframe(map_trans_df.head(30))

            if not st.session_state.district_map_rendered:
                fig = px.scatter_mapbox(
                    map_trans_df,
                    lat='Latitude',
                    lon='Longitude',
                    size='Total_Metric_Value',
                    color='Total_Metric_Value',
                    hover_name='District',
                    color_continuous_scale='Rainbow',
                    size_max=40,
                    zoom=4,
                    mapbox_style='carto-positron',
                    title=f"Top Performing Districts in {years} (by Metric Value)"
                )
                st.plotly_chart(fig, use_container_width=True, key=f"district_map_{years}")
                st.session_state.district_map_rendered = True
            else:
                st.warning(f"No data found for the year {years}")
                st.session_state.district_map_rendered = False

    elif level == "Top performing Pincodes":
        key = f"map_rendered_pincodes_{years}"
        if key not in st.session_state:
            st.session_state[key] = False
        top_trans_df = get_top_pincodes_by_year(years)
       
        if not top_trans_df.empty:
            st.subheader(f"Top 10 Pincodes by Pincode Value in {years}")
            st.dataframe(top_trans_df.head(30))

        if not st.session_state[key]:
                fig = px.scatter_mapbox(
                    top_trans_df,
                    lat='Latitude',
                    lon='Longitude',
                    size='Total_Pincode_Value',
                    color='Total_Pincode_Value',
                    hover_name='Pincode',
                    color_continuous_scale='Rainbow',
                    size_max=40,
                    zoom=4,
                    mapbox_style='carto-positron',
                    title=f"Top Performing PIncodes in {years} (by PIncode Value)"
                )
                st.plotly_chart(fig, use_container_width=True, key=f"map_pincodes_{years}")
                st.session_state[key] = True
        else:
            st.warning(f"No data found for the year {years}")

if selected_menu == 'Business Case Study':
    st.subheader("Business Strategy Insights")

    scenario = st.selectbox("Select Strategic Scenario", [
        "Decoding Transaction Dynamics on PhonePe",
        "Device Dominance and User Engagement Analysis",
        "Insurance Penetration and Growth Potential Analysis",
        "Transaction Analysis for Market Expansion",
        "User Engagement and Growth Strategy"
    ])

    if scenario == "Decoding Transaction Dynamics on PhonePe":
        st.markdown("""
        **Scenario:**  
        PhonePe has identified significant variations in transaction behavior across states, quarters, and payment categories.  
        Some regions and transaction types show consistent growth, while others stagnate or decline.  
        The leadership team seeks deeper insights to drive targeted strategies.
        """)
        show_growth_regions()
        show_declining_regions()
        show_volatility()
        show_trend_summary()

    elif scenario == "Device Dominance and User Engagement Analysis":
        st.markdown("""
        **Scenario:**  
        PhonePe wants to improve app performance by analyzing user preferences across device brands.  
        Trends vary across regions, and some devices are underutilized despite high registration.  
        This insight will guide UX improvements and device-specific optimizations.
        """)
        show_volatility()
        year = st.selectbox("Select Year for Device Snapshot", get_years())
        quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])
        show_map_snapshot(year, quarter)
        show_trend_summary()

    elif scenario == "Insurance Penetration and Growth Potential Analysis":
        st.markdown("""
        **Scenario:**  
        PhonePe is expanding into insurance and wants to analyze transaction growth in this segment.  
        The goal is to identify untapped regions for marketing and insurer partnerships.
        """)
        show_insurance_growth()
        show_growth_regions()
        show_declining_regions()
        year = st.selectbox("Select Year for Insurance Snapshot", get_years())
        quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])
        show_map_snapshot(year, quarter)

    elif scenario == "Transaction Analysis for Market Expansion":
        st.markdown("""
        **Scenario:**  
        In a competitive market, PhonePe needs to understand transaction dynamics across states.  
        This analysis will uncover trends and opportunities for regional expansion.
        """)
        show_trend_summary()
        year = st.selectbox("Select Year for Expansion Snapshot", get_years())
        quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])
        show_map_snapshot(year, quarter)
        show_growth_regions()

    elif scenario == "User Engagement and Growth Strategy":
        st.markdown("""
        **Scenario:**  
        PhonePe seeks to enhance its market position by analyzing user engagement across different states and districts.  
        With a significant number of registered users and app opens, understanding user behavior can provide valuable insights for strategic decision-making and growth opportunities.
        """)
        show_volatility()
        show_growth_regions()
        show_declining_regions()
        year = st.selectbox("Select Year for Pincode Engagement", get_years())
        quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])
        show_pincode_engagement_map(year, quarter)
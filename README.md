<<<<<<< HEAD
Phonepe-Project
=======
# Phonepe-Project
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c
PhonePe Transaction Insights

First clone the data from the path using !git clone https://github.com/PhonePe/pulse

import os
import json
import pandas as pd
import numpy as np
import mysql.connector
import pymysql
from sqlalchemy import create_engine - for data cleaning and preprocessing

Created 9 tables state path and json path

agg_insurance
agg_transaction
<<<<<<< HEAD
agg_trans
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c
agg_user
map_insurance
map_transaction
map_user
top_insurance
top_transaction
top_user

Analyse and Cleaned all the data frame.

# Create the below connection to mysql to use all 9 tables in mysql
connection = pymysql.connect(

    host='localhost',        # or '127.0.0.1' or your DB server IP
    user='root',
    password='Harsha@123',
    database='phonepe',
    port=3306                # default MySQL port
)
cursor = connection.cursor()

engine = create_engine("mysql+pymysql://root:Harsha%40123@localhost:3306/phonepe")

Created query in mysql using 9 table

PhonePe Analytics Dashboard Documentation


Data Sources

agg_transaction     -	 State-level transaction data with lat/lon
<<<<<<< HEAD
                         Show_transaction_by_state_year
map_transaction	    -    District-level metrics
top_transaction	    -    Pincode-level transaction volumes
agg_trans	        -    Transaction trends (Growth, Decline, Stable)
                         Show_transaction_volatility
                         Show_transaction_type_mix
                         Show_yoy_growth
agg_user	        -    Device-level user behavior
                         Show_underutilized_devices_by_state
                         Show_state_volatility_summary
                         Show_conversion_funnel
                         Show_device_brand
map_user	        -    User engagement by region
                         Show_engagement_by_state
                         Show_district_engagement_chord        
agg_insurance	    -    Insurance-specific transaction data
                         Show_conversion_funnel
                         Show_policy_type_distribution


=======
map_transaction	    -    District-level metrics
top_transaction	    -    Pincode-level transaction volumes
agg_trans	        -    Transaction trends (Growth, Decline, Stable)
agg_user	        -    Device-level user behavior
map_user	        -    User engagement by region
agg_insurance	    -    Insurance-specific transaction data
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c

1. Top-Level Data Retrieval

    get_all_states_by_year(year)
    get_all_districts_by_year(year)
    get_top_pincodes_by_year(year)
    These functions support map visualizations and regional summaries.
<<<<<<< HEAD
    Business Insights: Helps regional teams prioritize outreach and investment by identifying high-activity states, districts, and pincodes.
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c
    
2. Insurance Growth Analysis

    Function: show_insurance_growth()
    Purpose: Highlights states with consistent quarter-over-quarter growth in insurance transactions.
    Visualization: Bar chart with color gradient based on growth quarters.
<<<<<<< HEAD
    Business Insight: Supports product expansion by pinpointing states with rising insurance adoption—ideal for launching new policy types or partnerships.
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c
    
3. Consistently Growing Regions

    Function: show_growth_regions()
    Purpose: Identifies states and transaction types with ≥3 growth quarters.
    Visualization: Histogram grouped by transaction type.
<<<<<<< HEAD
    Business Insight: Enables targeted marketing and resource allocation in regions showing sustained transaction growth across categories.
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c

4. Declining/Stagnant Regions

    Function: show_declining_regions()
    Purpose: Flags regions with ≥3 quarters of decline or stability.
    Visualization: Bar chart by state and transaction type.
<<<<<<< HEAD
    Business Insight: Flags areas needing intervention—whether through incentives, UX improvements, or localized campaigns.
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c

5. Device-Specific Volatility

    Function: show_volatility()
    Purpose: Tracks changes in user count, app opens, and usage % across device brands.
    Visualization: Line chart with brand and metric selector.
<<<<<<< HEAD
    Business Insight: Guides device-specific optimization and brand partnerships by revealing fluctuating user behavior across hardware segments.
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c

6. Map Snapshot by Quarter

    Function: show_map_snapshot(year, quarter)
    Purpose: Displays transaction trends on a map for a selected quarter.
    Visualization: Scatter mapbox colored by trend.
<<<<<<< HEAD
    Business Insight: Provides a visual pulse of regional performance, helping leadership track quarterly impact of campaigns or policy changes.
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c

7. Trend Summary by State

    Function: show_trend_summary()
    Purpose: Summarizes growth, decline, stable, and no-data trends per state.
    Visualization: Pie chart for selected state.
<<<<<<< HEAD
    Business Insight: Offers a quick strategic overview for boardroom discussions—highlighting which states are thriving, lagging, or data-deficient.
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c

8. Pincode Engagement Map

    Function: show_pincode_engagement_map(year, quarter)
    Purpose: Shows engagement rate and spend per user at pincode level.
    Visualization: Map with selectable metric (engagement, spend, volume).
<<<<<<< HEAD
    Business Insight: Enables hyperlocal targeting by revealing granular engagement and spend patterns—ideal for merchant onboarding or ad placement.

9. Yearly Transaction Trends by State

   Function: show_transaction_by_state_year()
   Purpose: Tracks how transaction volumes evolve year-over-year for each state.
   Visualizations: Line Chart - Shows transaction growth or decline over time for a selected state.
                   Heatmap: Compares transaction intensity across all states and years.
   Business Insight: Supports long-term planning by visualizing historical growth trajectories and identifying seasonal or policy-driven shifts.                  

10. Underutilized Devices by State

    Function: show_underutilized_devices_by_state()
    Purpose: Flags device brands with low app engagement despite high user registration.
    Visualization:Treemap - Hierarchical view of states and device brands.
    Business Insight: Helps optimize marketing or app performance strategies for specific device segments.

11. State-wise Volatility Summary

    Function: show_state_volatility_summary()
    Purpose: Measures quarter-over-quarter changes in user count, app opens, and usage percentage.
    Visualization: Scatter Plot - X-axis = AppOpens change, Y-axis = Usage change, Bubble size = User count change.
    Business Insight: Identifies states with unstable user behavior—ideal for targeting retention campaigns or UX improvements.

12. Engagement Rate by State

    Function: show_engagement_by_state()
    Purpose: Measures how actively users engage with the app across states in a given quarter.
    Visualization: Sunburst Chart - Outer ring = states, size = user base, color = engagement rate.
    Business Insight: Reveals high-engagement regions vs. passive user bases. Useful for regional strategy and feature rollout planning.

13. Conversion Funnel: Insurance vs Engagement

    Function: show_conversion_funnel()
    Purpose: Correlates insurance transactions with user engagement across states and quarters.
    Visualization: Line Chart: Tracks engagement rate over time per state.
    Business Insight: Reveals whether high insurance activity aligns with app usage—ideal for targeting bundled offerings or regional campaigns.

14. Policy Type Distribution

    Function: show_policy_type_distribution()
    Purpose: Breaks down insurance transactions by policy type across states.
    Visualization: Sunburst Chart - Inner ring = states, outer ring = policy types.
    Business Insight: Helps identify dominant insurance categories regionally—useful for product-market fit analysis.

15. Transaction Volatility
    
    Function: show_transaction_volatility()
    Purpose: Measures standard deviation in transaction amounts across quarters.
    Visualization: Bar Chart - Top 10 states with highest volatility.
    Business Insight: Flags regions with unstable transaction behavior—ideal for risk modeling or forecasting adjustments.

16. Transaction Type Mix

    Function: show_transaction_type_mix()
    Purpose: Shows how transaction value is distributed across types within each state.
    Visualization: Sunburst Chart - State → Transaction Type → Value.
    Business Insight: Reveals economic behavior patterns—e.g., states leaning toward bill payments vs merchant transactions.

17. Year-over-Year Growth Heatmap

    Function: show_yoy_growth_heatmap()
    Purpose: Calculates and visualizes YoY growth in transaction value.
    Visualization: Heatmap - Green = growth, Red = decline.
    Business Insight: Quickly identifies growth hotspots and declining regions—ideal for strategic planning.

18. Device Brand Distribution

    Function: show_device_brand_treemap()
    Purpose: Aggregates user count by device brand.
    Visualization: Treemap - Size = user base per brand.
    Business Insight: Useful for optimizing app performance or targeting device-specific UX improvements.

19. District-Level Engagement Flow

    Function: show_district_engagement_chord()
    Purpose: Compares registered users vs app opens at district level.
    Visualization: Sunburst Chart - Engagement type → District → Value.
    Business Insight: Highlights districts with high registration but low engagement—ideal for reactivation campaigns.    
=======
>>>>>>> 79180b3ea679336b7187e266ea61f21ef9e7319c

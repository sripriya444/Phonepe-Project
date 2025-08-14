# Phonepe-Project
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
map_transaction	    -    District-level metrics
top_transaction	    -    Pincode-level transaction volumes
agg_trans	        -    Transaction trends (Growth, Decline, Stable)
agg_user	        -    Device-level user behavior
map_user	        -    User engagement by region
agg_insurance	    -    Insurance-specific transaction data

1. Top-Level Data Retrieval

    get_all_states_by_year(year)
    get_all_districts_by_year(year)
    get_top_pincodes_by_year(year)
    These functions support map visualizations and regional summaries.
    
2. Insurance Growth Analysis

    Function: show_insurance_growth()
    Purpose: Highlights states with consistent quarter-over-quarter growth in insurance transactions.
    Visualization: Bar chart with color gradient based on growth quarters.
    
3. Consistently Growing Regions

    Function: show_growth_regions()
    Purpose: Identifies states and transaction types with ≥3 growth quarters.
    Visualization: Histogram grouped by transaction type.

4. Declining/Stagnant Regions

    Function: show_declining_regions()
    Purpose: Flags regions with ≥3 quarters of decline or stability.
    Visualization: Bar chart by state and transaction type.

5. Device-Specific Volatility

    Function: show_volatility()
    Purpose: Tracks changes in user count, app opens, and usage % across device brands.
    Visualization: Line chart with brand and metric selector.

6. Map Snapshot by Quarter

    Function: show_map_snapshot(year, quarter)
    Purpose: Displays transaction trends on a map for a selected quarter.
    Visualization: Scatter mapbox colored by trend.

7. Trend Summary by State

    Function: show_trend_summary()
    Purpose: Summarizes growth, decline, stable, and no-data trends per state.
    Visualization: Pie chart for selected state.

8. Pincode Engagement Map

    Function: show_pincode_engagement_map(year, quarter)
    Purpose: Shows engagement rate and spend per user at pincode level.
    Visualization: Map with selectable metric (engagement, spend, volume).

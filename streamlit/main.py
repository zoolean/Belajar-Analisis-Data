import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from func import DataAnalyzer, BrazilMapPlotter
from babel.numbers import format_currency
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("./dataset/all_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('./dataset/geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Judul
    st.title("Dashboard Analisis Data")

    # Logo Image
    st.image("./streamlit/gcl.png")

    # Rentang Tanggal
    start_date, end_date = st.date_input(
        label="Pilih Rentang Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )


# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)
daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

# Title
st.header("E-Commerce Dashboard :convenience_store:")

# Daily Orders
st.subheader("Daily Orders")

col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = format_currency(daily_orders_df["revenue"].sum(), "IDR", locale="id_ID")
    st.markdown(f"Total Revenue: **{total_revenue}**")

plt.figure(figsize=(12, 6))
bars = plt.bar(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    color="#FFD54F",
    edgecolor="#FFA000",
    linewidth=2,
)
plt.xlabel("Date", fontsize=15)
plt.ylabel("Order Count", fontsize=15)
plt.xticks(rotation=45)
plt.yticks(fontsize=15)
plt.title("Daily Orders", fontsize=20)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Menambahkan label di atas setiap batang
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, yval, int(yval), va="bottom", fontsize=12)

st.pyplot()



# Customer Demographic
st.subheader("Customer Demographic")
tab1 = st.sidebar.radio("Select Tab", ["Geolocation"])

if tab1 == "Geolocation":
    map_plot.plot()

    with st.expander("See Explanation"):
        st.write('Sesuai dengan grafik yang sudah dibuat, ada lebih banyak pelanggan di bagian tenggara dan selatan. Informasi lainnya, ada lebih banyak pelanggan di kota-kota yang merupakan ibu kota (São Paulo, Rio de Janeiro, Porto Alegre, dan lainnya).')

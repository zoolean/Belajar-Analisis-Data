import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib.request



# Dataset
all_df = pd.read_csv("./dataset/all_data.csv")

# Geolocation Dataset
geo_df = pd.read_csv('./dataset/geolocation.csv')

# Konversi kolom tanggal ke tipe data datetime
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])


# VISUALISASI 1
st.title("Distribusi Jumlah Order per Bulan (Jun 2017 - Mei 2018)")
filtered_orders = all_df[
    (all_df['order_purchase_timestamp'] >= '2017-06-01') &
    (all_df['order_purchase_timestamp'] <= '2018-05-31')
]
monthly_order_counts = filtered_orders.resample('M', on='order_purchase_timestamp').size()
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(x=monthly_order_counts.index.strftime('%B %Y'), y=monthly_order_counts.values, marker='o', color='#72B6A1', ax=ax1)
ax1.set(xlabel='Bulan', ylabel='Jumlah Order')
ax1.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig1)

# VISUALISASI 2
st.title("Produk dengan Pembelian Terbanyak dan Terendah")

# Jumlah semua produk terjual
purchased_products = all_df['product_category_name_english'].value_counts()

# Produk dengan jumlah pembelian paling banyak
most_purchased = purchased_products.idxmax()
most_purchased_count = purchased_products.max()

# Produk dengan jumlah pembelian paling sedikit
least_purchased = purchased_products.idxmin()
least_purchased_count = purchased_products.min()

# Data untuk plot pembelian terbanyak
top_products = purchased_products.head(6)  # Ambil 6 produk teratas untuk plot

# Data untuk plot pembelian tersedikit
least_purchased_data = all_df[all_df['product_category_name_english'].isin(purchased_products.nsmallest(6).index)]
least_purchased_data_counts = least_purchased_data['product_category_name_english'].value_counts()
# Mengurutkan data berdasarkan jumlah pembelian
least_purchased_data_counts = least_purchased_data_counts.sort_values()

# Set warna palet untuk bar plot
palette = sns.color_palette("Set2")

# Warna khusus untuk produk terbanyak dan tersedikit
special_colors = {'Produk dengan Pembelian Terbanyak': '#72B6A1', 'Produk dengan Pembelian Terendah': '#72B6A1'}

# Mendapatkan posisi produk dengan pembelian tersedikit
least_purchased_index = least_purchased_data_counts.index.get_loc(least_purchased)

# Plot produk dengan pembelian terbanyak dan terendah secara bersebelahan
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

# Bar plot untuk produk terbanyak
sns.barplot(x=top_products.index, y=top_products.values, palette=palette, ax=axes[0])
axes[0].set_title('Produk dengan Pembelian Terbanyak')
axes[0].set_xlabel('Nama Produk')
axes[0].set_ylabel('Jumlah Pembelian')

# Menambahkan warna khusus untuk produk terbanyak
for i, bar in enumerate(axes[0].patches):
    if i == 0:
        bar.set_facecolor(special_colors['Produk dengan Pembelian Terbanyak'])
    else:
        bar.set_facecolor('#cbd4d1')  # Warna abu-abu

# Bar plot untuk produk tersedikit
sns.barplot(x=least_purchased_data_counts.index, y=least_purchased_data_counts.values, palette=palette, ax=axes[1])
axes[1].set_title('Produk dengan Pembelian Terendah')
axes[1].set_xlabel('Nama Produk')
axes[1].set_ylabel('Jumlah Pembelian')

# Menambahkan warna khusus untuk produk tersedikit
for i, bar in enumerate(axes[1].patches):
    if i == least_purchased_index:
        bar.set_facecolor(special_colors['Produk dengan Pembelian Terendah'])
    else:
        bar.set_facecolor('#cbd4d1')  # Warna abu-abu

plt.tight_layout()
st.pyplot(fig)

# VISUALISASI 3
st.title("Peta Lokasi Pelanggan")
brazil_map_image = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'), 'jpg')
fig3, ax3 = plt.subplots(figsize=(10, 10))
ax3.scatter(geo_df['geolocation_lng'], geo_df['geolocation_lat'], alpha=0.3, s=0.3, c='#72B6A1')
ax3.set_title('Peta Lokasi Pelanggan')
ax3.axis('off')
ax3.imshow(brazil_map_image, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
st.pyplot(fig3)

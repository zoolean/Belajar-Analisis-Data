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

# VISUALISASI PERTAMA
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
top_products = purchased_products.head(5)  

# Data untuk plot pembelian tersedikit
least_purchased_data = all_df[all_df['product_category_name_english'].isin(purchased_products.nsmallest(6).index)]
least_purchased_data_counts = least_purchased_data['product_category_name_english'].value_counts()
# Mengurutkan data berdasarkan jumlah pembelian
least_purchased_data_counts = least_purchased_data_counts.sort_values()

# Plot produk dengan pembelian terbanyak dan terendah secara bersebelahan
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

# Line plot untuk produk terbanyak
top_products.plot(ax=axes[0], color='#00008B', marker='o', linestyle='-')
axes[0].set_title('Produk yang Terjual paling Banyak')
axes[0].set_xlabel('Produk')
axes[0].set_ylabel('Pembelian')

# Line plot untuk produk tersedikit
least_purchased_data_counts.plot(ax=axes[1], color='#00008B', marker='o', linestyle='-')
axes[1].set_title('Produk yang Terjual paling Rendah')
axes[1].set_xlabel('Produk')
axes[1].set_ylabel('Pembelian')

plt.tight_layout()
st.pyplot(fig)


# VISUALISASI KEDUA
st.title("Peta Lokasi Pelanggan")
brazil_map_image = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'), 'jpg')
fig3, ax3 = plt.subplots(figsize=(10, 10))
ax3.scatter(geo_df['geolocation_lng'], geo_df['geolocation_lat'], alpha=0.3, s=0.3, c='#00008B')
ax3.set_title('Peta Lokasi Pelanggan')
ax3.axis('off')
ax3.imshow(brazil_map_image, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
st.pyplot(fig3)
st.write('Sesuai dengan grafik yang sudah dibuat, ada lebih banyak pelanggan di bagian tenggara dan selatan. Informasi lainnya, ada lebih banyak pelanggan di kota-kota yang merupakan ibu kota (São Paulo, Rio de Janeiro, Porto Alegre, dan lainnya).')

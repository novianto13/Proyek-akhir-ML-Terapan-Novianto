# -*- coding: utf-8 -*-
"""Proyek akhir ML Terapan Novianto.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/187hrCS7CWfmt67QiaOl4JaqGz-cKn4jq

# Proyek akhir ML Terapan: Rekomendasi makanan

# Nama: Novianto

# 1. Pemahaman data
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

import re
import string

food = pd.read_csv('https://raw.githubusercontent.com/novianto13/Proyek-akhir-ML-Terapan/main/Food.csv')
food.head()

food.info()

rating = pd.read_csv('https://raw.githubusercontent.com/novianto13/Proyek-akhir-ML-Terapan/main/ratings.csv')
rating.head()

rating.info()

"""## Data food"""

sns.countplot(x='C_Type', data=food)
plt.title('Distribusi C_Type')
plt.xlabel('C_Type')
plt.ylabel('Jumlah')
plt.xticks(rotation=45, ha='right') # Rotasi label sumbu x jika diperlukan
plt.show()

sns.countplot(x='Veg_Non', data=food)
plt.title('Distribusi Veg_Non')
plt.xlabel('Veg_Non')
plt.ylabel('Jumlah')
plt.show()

c_type_counts = food['C_Type'].value_counts()
veg_non_counts = food['Veg_Non'].value_counts()

print("Jumlah data pada C_Type:\n", c_type_counts)
print("\nJumlah data pada Veg_Non:\n", veg_non_counts)

pd.crosstab(food['C_Type'], food['Veg_Non']).plot(kind='bar', stacked=True)
plt.title('Hubungan antara C_Type dan Veg_Non')
plt.xlabel('C_Type')
plt.ylabel('Jumlah')
plt.xticks(rotation=45, ha='right') # Rotasi label sumbu x jika diperlukan
plt.legend(title='Veg_Non')
plt.show()

cross_tab = pd.crosstab(food['C_Type'], food['Veg_Non'])
print(cross_tab)

"""## Data rating"""

rating.describe()

print('Jumlah user ID: ', len(rating.User_ID.unique()))
print('Jumlah food ID: ', len(rating.Food_ID.unique()))
print('Jumlah data rating: ', len(rating))

"""## Data preprocessing"""

# Menggabungkan dataset food dan rating berdasarkan Food_ID
food_rating = pd.merge(food, rating, on='Food_ID', how='left')

# Menampilkan 5 baris pertama dari dataset yang sudah digabungkan
print(food_rating.head())

# Mengelompokkan data berdasarkan 'Food_Name' dan menghitung rata-rata rating
food_ratings = food_rating.groupby('Name')['Rating'].mean().reset_index()

# Mengurutkan data berdasarkan rating rata-rata secara descending dan mengambil 10 teratas
top_10_foods = food_ratings.sort_values(by=['Rating'], ascending=False).head(10)

# Menampilkan 10 nama makanan dengan rating tertinggi
print("10 Nama Makanan dengan Rating Tertinggi:\n", top_10_foods)

# Mengelompokkan data berdasarkan 'Food_Name' dan menghitung rata-rata rating
food_ratings = food_rating.groupby('Name')['Rating'].mean().reset_index()

# Mengurutkan data berdasarkan rating rata-rata secara descending
sorted_ratings = food_ratings.sort_values(by=['Rating'], ascending=False)

# Mengambil 5 nama makanan dengan rating tertinggi
top_5_foods = sorted_ratings.head(5)

# Mengambil 5 nama makanan dengan rating terendah
bottom_5_foods = sorted_ratings.tail(5)

# Menampilkan hasil
print("5 Nama Makanan dengan Rating Tertinggi:\n", top_5_foods)
print("\n5 Nama Makanan dengan Rating Terendah:\n", bottom_5_foods)

# Menghitung jumlah data untuk setiap rating
rating_counts = food_rating['Rating'].value_counts()

# Menghitung jumlah total data
total_data = len(food_rating)

# Menampilkan hasil
print("Jumlah data berdasarkan rating:")
print(rating_counts)
print("\nJumlah total data:", total_data)

# Menghitung jumlah data untuk setiap rating
rating_counts = food_rating['Rating'].value_counts()

# Membuat grafik batang
plt.bar(rating_counts.index, rating_counts.values)

# Menambahkan label dan judul
plt.xlabel("Rating")
plt.ylabel("Jumlah Data")
plt.title("Jumlah Data Berdasarkan Rating")

# Menampilkan grafik
plt.show()

# manampilkan tabel rating dan jenis makanan

# Kelompokkan data dan hitung jumlah data
rating_food_counts = food_rating.groupby(['Rating', 'C_Type']).size().unstack(fill_value=0)

# Hitung total per kolom
total_per_column = rating_food_counts.sum()

# Buat baris baru untuk total
total_row = pd.DataFrame(data=[total_per_column.values], columns=total_per_column.index, index=['Total'])

# Gabungkan baris total dengan DataFrame asli
rating_food_counts = pd.concat([rating_food_counts, total_row])

# Hitung total per baris dan tambahkan kolom 'Jumlah'
rating_food_counts['Jumlah'] = rating_food_counts.sum(axis=1)

# Tampilkan tabel
print("Jumlah Data Berdasarkan Rating dan Jenis Makanan:")
display(rating_food_counts)

# Mengambil data dari tabel rating_food_counts
rating_food_counts = food_rating.groupby(['Rating', 'C_Type']).size().unstack(fill_value=0)

# Membuat grafik batang bertumpuk
rating_food_counts.plot(kind='bar', stacked=True, figsize=(10, 6))

# Menambahkan label dan judul
plt.xlabel("Jenis Makanan (C_Type)")
plt.ylabel("Jumlah Data")
plt.title("Jumlah Data Berdasarkan Rating dan Jenis Makanan")
plt.xticks(rotation=45, ha='right')  # Rotasi label sumbu x agar mudah dibaca
plt.legend(title='Rating')

# Menampilkan grafik
plt.show()

"""# Data Preparation

## Cleaning data
"""

food_rating.duplicated().sum()

# Pindahkan kolom 'User_ID' ke posisi paling kiri
food_rating = food_rating[['User_ID'] + [col for col in food_rating.columns if col != 'User_ID']]

# Menampilkan 5 baris pertama dari dataset yang sudah diubah
print(food_rating.head())

food_rating.info()

# Mengecek keberadaan nilai NaN di setiap kolom
print(food_rating.isna().any())

# Mengecek jumlah nilai NaN di setiap kolom
print(food_rating.isna().sum())

# Mengecek keberadaan data kosong di kolom bertipe object (string)
for col in food_rating.select_dtypes(include=['object']).columns:
    print(f"Kolom '{col}':")
    num_empty = food_rating[col].apply(lambda x: x.strip() == '').sum()
    print(f"  Jumlah data kosong: {num_empty}")

# Mengecek keberadaan nilai 0 di kolom numerik
for col in food_rating.select_dtypes(include=['number']).columns:
    print(f"Kolom '{col}':")
    num_zeros = (food_rating[col] == 0).sum()
    print(f"  Jumlah nilai 0: {num_zeros}")

# Menghitung jumlah data NaN di setiap kolom
na_counts = food_rating.isna().sum()

# Menampilkan jumlah total data NaN di seluruh dataset
total_na = na_counts.sum()

# Menampilkan hasil
print("Jumlah data NaN di setiap kolom:\n", na_counts)
print("\nTotal data NaN di seluruh dataset:", total_na)

# Menghapus baris yang mengandung nilai NaN
food_rating = food_rating.dropna()

# Menampilkan jumlah baris dan kolom setelah menghapus data NaN
print("Ukuran dataset setelah menghapus data NaN:", food_rating.shape)

# Mengubah tipe data kolom 'User_ID' dan 'Rating' menjadi int
food_rating['User_ID'] = food_rating['User_ID'].astype(int)
food_rating['Rating'] = food_rating['Rating'].astype(int)

# Menampilkan informasi tipe data dari dataset food_rating
print(food_rating.info())

# hasil gabungan data
food_rating.head(5)

"""# Model

## Content Based Filtering

### TF-IDF Vectorizer
"""

from sklearn.feature_extraction.text import TfidfVectorizer

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()

# Melakukan perhitungan idf pada data cuisine
tf.fit(food['C_Type'])

# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names_out()

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(food['C_Type'])

# Melihat ukuran matrix tfidf
tfidf_matrix.shape

# Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()

# Membuat dataframe untuk melihat tf-idf matrix
# Kolom diisi dengan jenis masakan
# Baris diisi dengan nama resto

num_cols_to_sample = min(22, tfidf_matrix.shape[1])  # Ensure sample size doesn't exceed columns
num_rows_to_sample = min(10, tfidf_matrix.shape[0])  # Ensure sample size doesn't exceed rows

pd.DataFrame(
    tfidf_matrix.todense(),
    columns=tf.get_feature_names_out(),
    index=food.Name
).sample(num_cols_to_sample, axis=1, replace=False).sample(num_rows_to_sample, axis=0, replace=False)

"""### Cosine similraity"""

from sklearn.metrics.pairwise import cosine_similarity

# Menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa nama resto
cosine_sim_df = pd.DataFrame(cosine_sim, index=food['Name'], columns=food['Name'])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada setiap resto
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""### Mendapatkan Rekomendasi"""

def food_recommendations(nama_makanan, similarity_data=cosine_sim_df, items=food[['Name', 'C_Type']], k=5):
    """
    Rekomendasi Resto berdasarkan kemiripan dataframe

    Parameter:
    ---
    nama_food : tipe data string (str)
                Nama Restoran (index kemiripan dataframe)
    similarity_data : tipe data pd.DataFrame (object)
                      Kesamaan dataframe, simetrik, dengan resto sebagai
                      indeks dan kolom
    items : tipe data pd.DataFrame (object)
            Mengandung kedua nama dan fitur lainnya yang digunakan untuk mendefinisikan kemiripan
    k : tipe data integer (int)
        Banyaknya jumlah rekomendasi yang diberikan
    ---


    Pada index ini, kita mengambil k dengan nilai similarity terbesar
    pada index matrix yang diberikan (i).
    """


    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,nama_makanan].to_numpy().argpartition(
        range(-1, -k, -1))

    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    # Drop nama_resto agar nama resto yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(nama_makanan, errors='ignore')

    return pd.DataFrame(closest).merge(items).head(k)

food[food.Name.eq('christmas cake')]

# Mendapatkan rekomendasi restoran yang mirip dengan KFC
food_recommendations('christmas cake')

"""## Collaborative Filtering"""

# Import library
import pandas as pd
import numpy as np
from zipfile import ZipFile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt

"""### Data preparation"""

# menunjukkan data yang akan diolah
rating.head()

#Checking the shape
rating.shape

# Checking for null values
rating.isnull().sum()

rating.info()

rating.tail()

# Removing the last row
rating = rating[:511]
rating.tail()

rating.head()

"""### Pengembangan Model Collaborative Filter"""

# Mengubah userID menjadi list tanpa nilai yang sama
user_ids = rating['User_ID'].unique().tolist()
print('list userID: ', user_ids)

# Melakukan encoding userID
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
print('encoded userID : ', user_to_user_encoded)

# Melakukan proses encoding angka ke ke userID
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}
print('encoded angka ke userID: ', user_encoded_to_user)

"""perhatian"""

# # Mengubah placeID menjadi list tanpa nilai yang sama
food_ids = rating['Food_ID'].unique().tolist()

# # Proses encoding placeID
food_to_food_encoded = {x: i for i, x in enumerate(food_ids)}

# # Proses decoding angka ke placeID
food_encoded_to_food = {i: x for i, x in enumerate(food_ids)}

"""---"""

# Mapping placeID ke dataframe food
rating['food'] = rating['Food_ID'].map(food_to_food_encoded)

# Cek apakah ada nilai NaN setelah mapping
if rating['food'].isnull().sum() > 0:
    print("Ada nilai NaN dalam kolom 'food' setelah mapping.")

# Cek jumlah unique Food_IDs
print("Unique Food_IDs:", len(rating['Food_ID'].unique()))

# Cek panjang mapping
print("Food to Food Encoded Length:", len(food_to_food_encoded))

# Cek apakah ada nilai Food_ID yang tidak termapping
unmapped_food_ids = set(rating['Food_ID']) - set(food_to_food_encoded.keys())
if unmapped_food_ids:
    print("Unmapped Food_IDs:", unmapped_food_ids)
else:
    print("All Food_IDs are mapped correctly.")

# Cek nilai NaN pada kolom food
print("Jumlah NaN pada kolom 'food':", rating['food'].isnull().sum())

# Tampilkan baris dengan nilai NaN
if rating['food'].isnull().sum() > 0:
    print("Baris dengan NaN di kolom 'food':")
    print(rating[rating['food'].isnull()])

# Proses encoding yang benar
food_to_food_encoded = {x: i for i, x in enumerate(food_ids)}
food_encoded_to_food = {i: x for i, x in enumerate(food_ids)}

# Mapping kolom 'Food_ID' ke 'food'
rating['food'] = rating['Food_ID'].map(food_to_food_encoded)

# Validasi nilai maksimum
# print("Max value in 'food':", rating['food'].max())
# assert rating['food'].max() < num_food, "Food ID encoding out of range!"

"""---"""

# Mapping userID ke dataframe user
rating['user'] = rating['User_ID'].map(user_to_user_encoded)

# Mapping placeID ke dataframe resto
rating['food'] = rating['Food_ID'].map(food_to_food_encoded)

# Mendapatkan jumlah user
num_users = len(user_to_user_encoded)
print(num_users)

# Mendapatkan jumlah resto
num_food = len(food_to_food_encoded)
print(num_food)

# Mengubah rating menjadi nilai float
rating['Rating'] = rating['Rating'].values.astype(np.float32)

# Nilai minimum rating
min_rating = min(rating['Rating'])

# Nilai maksimal rating
max_rating = max(rating['Rating'])

print('Number of User: {}, Number of Food: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_food, min_rating, max_rating
))

"""### Validasi"""

# Mengacak dataset
rating = rating.sample(frac=1, random_state=42)
rating

"""---
TAMBAHAN
"""

# Membuat ulang x dan y
x = rating[['user', 'food']].values
y = rating['Rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

# Membagi dataset
train_indices = int(0.8 * rating.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

# Cek nilai di x_train[:, 1] yang lebih besar dari num_food - 1
invalid_food_ids = x_train[:, 1][x_train[:, 1] >= num_food]
print("Invalid Food IDs in x_train:", invalid_food_ids)

"""---"""

# # Membuat variabel x untuk mencocokkan data user dan resto menjadi satu value
# x = rating[['user', 'food']].values

# # Membuat variabel y untuk membuat rating dari hasil
# y = rating['Rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

# # Membagi menjadi 80% data train dan 20% data validasi
# train_indices = int(0.8 * rating.shape[0])
# x_train, x_val, y_train, y_val = (
#     x[:train_indices],
#     x[train_indices:],
#     y[:train_indices],
#     y[train_indices:]
# )

# print(x, y)

"""### training"""

class RecommenderNet(tf.keras.Model):

  # Insialisasi fungsi
  def __init__(self, num_users, num_food, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_food = num_food
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.food_embedding = layers.Embedding( # layer embeddings food
        num_food,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.food_bias = layers.Embedding(num_food, 1) # layer embedding resto bias

  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    food_vector = self.food_embedding(inputs[:, -1]) # memanggil layer embedding 3
    food_bias = self.food_bias(inputs[:, -1]) # memanggil layer embedding 4

    dot_user_food = tf.tensordot(user_vector, food_vector, 2)

    x = dot_user_food + user_bias + food_bias

    return tf.nn.sigmoid(x) # activation sigmoid

model = RecommenderNet(num_users, num_food, 50) # inisialisasi model

# model compile
model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

# Memulai training

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 8,
    epochs = 100,
    validation_data = (x_val, y_val)
)

"""### Visualisasi Metrik"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""### Mendapatkan Rekomendasi Resto"""

food_df = food_rating
df = rating

# Mengambil sample user
user_id = df.User_ID.sample(1).iloc[0]
food_review_by_user = df[df.Food_ID == user_id]


# Operator bitwise (~), bisa diketahui di sini https://docs.python.org/3/reference/expressions.html
# Mengganti 'id' dengan 'Food_ID'
food_not_review = food_df[~food_df['Food_ID'].isin(food_review_by_user.Food_ID.values)]['Food_ID']
food_not_review = list(
    set(food_not_review)
    .intersection(set(food_to_food_encoded.keys()))
)

# Mengganti 'review_not_review' dengan 'food_not_review' dan 'User_ID' dengan 'user_id'
food_not_review = [[food_to_food_encoded.get(x)] for x in food_not_review]
user_encoder = user_to_user_encoded.get(user_id)
user_food_array = np.hstack(
    ([[user_encoder]] * len(food_not_review), food_not_review)
)

ratings = model.predict(user_food_array).flatten()

top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_food_ids = [
    food_encoded_to_food.get(food_not_review[x][0]) for x in top_ratings_indices
]

print('Showing recommendations for users: {}'.format(user_id))
print('===' * 9)
print('Food with high ratings from user')
print('----' * 8)

top_food_user = (
    food_review_by_user.sort_values(
        by='Rating',
        ascending=False
    )
    .head(5)
    .Food_ID.values
)

food_df_rows = food_df[food_df['Food_ID'].isin(top_food_user)]
# Remove duplicate rows based on 'Name' and 'C_Type'
food_df_rows = food_df_rows.drop_duplicates(subset=['Name', 'C_Type'])

for row in food_df_rows.itertuples():
    print(row.Name, ':', row.C_Type)

print('----' * 8)
print('Top 10 food recommendation')
print('----' * 8)

recommended_food = food_df[food_df['Food_ID'].isin(recommended_food_ids)]
# Remove duplicate rows based on 'Name' and 'C_Type'
recommended_food = recommended_food.drop_duplicates(subset=['Name', 'C_Type'])

for row in recommended_food.itertuples():
    print(row.Name, ':', row.C_Type)
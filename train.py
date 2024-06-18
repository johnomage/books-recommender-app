#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.sparse import csr_matrix
import gdown
import warnings
import os
import joblib
from sklearn.neighbors import NearestNeighbors

warnings.simplefilter('ignore')

# Download data
gdown.download_folder("https://drive.google.com/drive/u/1/folders/1qLH0F0FcnUp95Ximwz-P961_BpfB4LDP")

# Load and process books data
books = pd.read_csv("datastore/BX-Books.csv", on_bad_lines='skip', encoding='latin-1', sep=";")
books = books[["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher", "Image-URL-L"]]

books.rename(columns={
    "Book-Title": "title",
    "Year-Of-Publication": "year",
    "Image-URL-L": "image_url",
    "Book-Author": "author",
    "Publisher": "publisher"
}, inplace=True)

# Load and process users data
users = pd.read_csv("datastore/BX-Users.csv", sep=";", encoding='latin-1')
users.rename(columns={"User-ID": "user_id"}, inplace=True)

# Load and process ratings data
ratings = pd.read_csv("datastore/BX-Book-Ratings.csv", sep=";", encoding='latin-1')
ratings.rename(columns={"User-ID": "user_id", "Book-Rating": "rating"}, inplace=True)

# Filter users with at least 200 ratings
user_rating_counts = ratings['user_id'].value_counts()
users_with_200_ratings = user_rating_counts[user_rating_counts >= 200].index
ratings = ratings[ratings['user_id'].isin(users_with_200_ratings)]

# Merge ratings with books data
book_ratings = ratings.merge(books, on='ISBN')

# Count book ratings
count_book_ratings = book_ratings.groupby('title')['rating'].count().reset_index()
count_book_ratings.rename(columns={'rating': 'rating_count'}, inplace=True)

# Merge book ratings count with the main dataframe
merged_data = book_ratings.merge(count_book_ratings, on='title')
merged_data = merged_data[merged_data['rating_count'] >= 25]

# Create pivot table
books_pivot_table = merged_data.pivot_table(columns='user_id', index='title', values='rating').fillna(0)

# Compress table
compressed_table = csr_matrix(books_pivot_table)

# Train NearestNeighbors model
nn_model = NearestNeighbors(algorithm='brute')
nn_model.fit(compressed_table)

# Save models and preprocessed data
os.makedirs('artifacts', exist_ok=True)
joblib.dump(nn_model, 'artifacts/model.pkl')
joblib.dump(books_pivot_table.index, 'artifacts/book_titles.pkl')
joblib.dump(merged_data, 'artifacts/merged_data.pkl')
joblib.dump(books_pivot_table, 'artifacts/books_pivot_table.pkl')

def recommend_books(book_name: str):
    try:
        model = joblib.load(open('artifacts/model.pkl', 'rb'))
        book_pivot = joblib.load(open('artifacts/books_pivot_table.pkl', 'rb'))
        book_idx = np.where(book_pivot.index == book_name)[0][0]
        data = book_pivot.iloc[book_idx].values.reshape(1, -1)
        distances, recommendations = model.kneighbors(data, n_neighbors=7)
        recommended_books = book_pivot.index[recommendations[0][1:]]  # Exclude the input book itself

        print(f'Book recommendations for "{book_name}":')
        for title in recommended_books:
            print(title)
        print()
    except IndexError:
        print(f'Book "{book_name}" not found in the dataset.')
    except Exception as e:
        print(f'An error occurred: {e}')


# test recommendations
recommend_books('The Cat Who Knew Shakespeare')
recommend_books('Harry Potter and the Chamber of Secrets (Book 2)')
recommend_books('Trunk Music (Detective Harry Bosch Mysteries)')

# from rec_systems import recommend_books
import streamlit as st
import numpy as np
from joblib import load
from difflib import get_close_matches

# recommend_books('Harry Potter and the Chamber of Secrets (Book 2)')

st.header('Books Recommender App')
st.markdown('### This app helps you to find books similar to your interest.')

# Load the artifacts
model = load('artifacts/model.pkl')
book_pivot_table = load('artifacts/books_pivot_table.pkl')
merged_data = load('artifacts/merged_data.pkl')
book_titles = load('artifacts/book_titles.pkl')


def recommend_books(book_name: str):
    recommendations_list = []
    try:
        book_idx = np.where(book_pivot_table.index == book_name)[0][0]
        data = book_pivot_table.iloc[book_idx].values.reshape(1, -1)
        _, recommendations = model.kneighbors(data, n_neighbors=7)
        recommended_books = book_pivot_table.index[recommendations[0][1:]]  # Exclude the input book itself

        # st.success(f'Book recommendations for: "{book_name}"', icon='✅')
        for title in recommended_books:
            recommendations_list.append(title)
    except IndexError:
        st.error(f'Book "{book_name}" not found in the dataset.', icon='❌')
    except Exception as e:
        st.error(f'An error occurred: {e}', icon='❌')

    return book_name, recommendations_list
    

selected_book = st.selectbox(label='Search Books', options=book_titles)

book_name, recommendations = recommend_books(selected_book)

def generate_book_url(book_name):
    author = merged_data[merged_data['title'] == book_name].iloc[0]['author']
    isbn = merged_data[merged_data['title'] == book_name].iloc[0]['ISBN']
    url_author = author.strip().replace(" ", "-")
    url_book_name = book_name.strip().replace(" ", "-")
    book_url = f'https://www.amazon.co.uk/{url_author}-{url_book_name}/dp/{isbn}'
    return author, book_url, isbn

if selected_book:
    author, url, _ = generate_book_url(book_name)
    st.markdown(f'Book recommendations for: [{book_name}]({url}) by **{author}**', help='Click for more details')


image_holders = st.columns(7)

for i, title in enumerate(recommendations):
    book_details = merged_data[merged_data['title'] == title].iloc[0]
    
    image_url = book_details['image_url']
    author, rec_book_url, isbn = generate_book_url(title)
    
    # Format details into Markdown
    # image_caption = f"[![Title: {title} \n||\nAuthor: {author}\n||\nISBN: {isbn}]({image_url})]({rec_book_url})"
    image_caption = f"Title: {title} \n||\nAuthor: {author}\n||\nISBN: {isbn}" # 💠
    
    # Display image and details in columns
    with image_holders[i]:
        st.image(image_url, caption=image_caption)
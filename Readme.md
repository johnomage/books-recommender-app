# Book Recommendation System

This project provides a book recommendation system using collaborative filtering. It leverages the Nearest Neighbors algorithm to suggest books similar to a given book based on user ratings.

## Features

- **Book Recommendations**: Get book recommendations based on a selected book.
- **Data Processing**: Handles book, user, and rating data to create a pivot table for the recommendation model.
- **Streamlit Interface**: Provides an interactive web interface to get book recommendations.

## Setup

### Prerequisites

- Python 3.8+
- Conda (for managing the environment)

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/books-recommendation-system.git
   cd book-recommendation-system
   ```

2. **Create and activate the conda environment**:
   ```sh
   conda create -n recenv python=3.11 -y
   conda activate recenv
   ```

3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Download the dataset**:
   ```sh
   gdown download_folder "https://drive.google.com/drive/u/1/folders/1qLH0F0FcnUp95Ximwz-P961_BpfB4LDP"
   ```

## Usage

### Training the Model

To preprocess the data and train the Nearest Neighbors model:

```sh
python train.py
```

This script will:
- Load and preprocess the books, users, and ratings data.
- Create a pivot table of books vs users.
- Train a Nearest Neighbors model using the pivot table.
- Save the trained model and preprocessed data to the `artifacts` directory.

### Running the Streamlit App

To start the Streamlit app:

```sh
streamlit run app.py
```

### Interacting with the App

1. Open your web browser and go to `http://localhost:8501`.
2. Select a book from the dropdown menu.
3. Click on the "Get Recommendations" button to see the book recommendations.

### Getting Recommendations for Books Not in the List

If a book is not in the list, you can still get recommendations by entering the book title manually in the text input box. The app will suggest similar books based on the closest match found in the dataset.

## Code Overview

- `train.py`: Script to preprocess data and train the recommendation model.
- `app.py`: Streamlit app to provide an interactive interface for getting book recommendations.
- `artifacts/`: Directory to store the trained model and preprocessed data.

## Example

```python
# Example usage of the recommendation function in app.py
book_name = "The Cat Who Knew Shakespeare"
recommend_books(book_name)
```

## Author

Your Name - [John Omage](mailto:john.e.omage@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit) file for details.

## Acknowledgments

- The datasets used in this project were provided by [Book-Crossing Dataset](https://grouplens.org/datasets/book-crossing/).
- Background work provided by [Ahmed](https://www.youtube.com/@dswithbappy), [PraiseGod](https://linkedin.com/in/praizerema)

---

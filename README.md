# Book Recommender

A simple Python application that recommends books using the Google Books API. Get personalized book recommendations across different genres with ratings and reviews!

## Features
- Get random book recommendations
- Filter recommendations by genre
- View book details including ratings and publication year

## Requirements
- Python 3.7 or higher
- pandas
- requests

## Quick Start

1. Install required packages:
pip install pandas requests

2. Run the program:
python book_recommender.py

3. Follow the menu prompts to:

  - Choose option 1 to get a book recommendation
  - Select a specific genre or get a recommendation from any genre
  - Choose option 2 to exit the program

## How It Works
The app fetches book data from Google Books API, processes it, and provides recommendations based on ratings and availability. Each recommendation includes:
- Book title
- Author(s)
- Genre
- Published year
- Rating and number of reviews

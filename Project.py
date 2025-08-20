import requests
import pandas as pd
import random
import time

class BookRecommender:
    def __init__(self):
        """Initialize the BookRecommender with empty data structures."""
        self.books_df = pd.DataFrame()
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def fetch_books_data(self, genre, max_results=40):
        """
        Fetch books data from Google Books API for a specific genre.
        """
        try:
            params = {
                'q': f'subject:{genre}',
                'maxResults': max_results
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            books_data = []
            for item in response.json().get('items', []):
                volume_info = item.get('volumeInfo', {})
                
                # Skip books without ratings
                if not volume_info.get('averageRating'):
                    continue
                
                book = {
                    'title': volume_info.get('title', 'Unknown'),
                    'authors': ', '.join(volume_info.get('authors', ['Unknown'])),
                    'genre': genre,
                    'published_year': volume_info.get('publishedDate', 'Unknown')[:4] if volume_info.get('publishedDate') else 'Unknown',
                    'rating': volume_info.get('averageRating', 0),
                    'ratings_count': volume_info.get('ratingsCount', 0)
                }
                books_data.append(book)
            
            new_df = pd.DataFrame(books_data)
            if not new_df.empty:
                self.books_df = pd.concat([self.books_df, new_df], ignore_index=True)
            
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            raise
        
    def clean_data(self):
        """Clean and prepare the books data."""
        try:
            # Convert ratings to numeric
            self.books_df['rating'] = pd.to_numeric(self.books_df['rating'], errors='coerce')
            self.books_df['ratings_count'] = pd.to_numeric(self.books_df['ratings_count'], errors='coerce')
            self.books_df['published_year'] = pd.to_numeric(self.books_df['published_year'], errors='coerce')
            
            # Remove books with no ratings or rating count
            self.books_df = self.books_df[self.books_df['rating'] > 0]
            self.books_df = self.books_df[self.books_df['ratings_count'] > 0]
            
            # Drop duplicates
            self.books_df.drop_duplicates(subset=['title', 'authors'], inplace=True)
            
            # Sort by rating and ratings_count
            self.books_df.sort_values(['rating', 'ratings_count'], 
                                    ascending=[False, False], 
                                    inplace=True)
            
        except Exception as e:
            print(f"Error cleaning data: {e}")
            raise

    def get_random_recommendation(self, genre=None):
        """
        Get a random book recommendation, optionally filtered by genre.
        """
        try:
            filtered_df = self.books_df if not genre else self.books_df[self.books_df['genre'].str.lower() == genre.lower()]
            
            if filtered_df.empty:
                raise ValueError(f"No rated books found for genre: {genre}")
            
            random_book = filtered_df.sample(n=1).iloc[0]
            return random_book.to_dict()
            
        except Exception as e:
            print(f"Error getting recommendation: {e}")
            raise

def main():
    """Main function to demonstrate the BookRecommender functionality."""
    try:
        # Initialize recommender
        recommender = BookRecommender()
        
        # List of genres
        genres = [
            'science fiction',
            'fantasy',
            'thriller',
            'romance',
            'horror',
            'drama',
            'adventure',
            'psychology',
            'history',
            'travel',
            'music',
            'sports',
            'humor'
        ]

        # Fetch data for all genres
        print("Fetching books data... Please wait.")
        for genre in genres:
            print(f"Loading {genre} books...")
            recommender.fetch_books_data(genre)
            time.sleep(1)  # Respect API rate limits
        
        # Clean the data
        recommender.clean_data()
        print("\nBook data loaded successfully!")
        
        # Main program loop
        while True:
            print("\nBook Recommender Menu:")
            print("1. Get random recommendation")
            print("2. Exit")
            
            choice = input("Enter your choice (1-2): ")
            
            if choice == '1':
                print("\nAvailable genres:")
                available_genres = recommender.books_df['genre'].unique()
                for i, genre in enumerate(available_genres, 1):
                    print(f"{i}. {genre}")
                
                genre_choice = input("\nEnter genre number (or press enter for any genre): ")
                
                try:
                    if genre_choice.strip():
                        selected_genre = available_genres[int(genre_choice) - 1]
                    else:
                        selected_genre = None
                        
                    recommendation = recommender.get_random_recommendation(selected_genre)
                    print("\n Your Random Book Recommendation:")
                    print("=" * 50)
                    print(f"Title: {recommendation['title']}")
                    print(f"Author(s): {recommendation['authors']}")
                    print(f"Genre: {recommendation['genre']}")
                    print(f"Published Year: {recommendation['published_year']}")
                    print(f"Rating: {recommendation['rating']}/5 ({recommendation['ratings_count']} ratings)")
                    print("=" * 50)
                    
                except (ValueError, IndexError):
                    print("Invalid genre selection. Please try again.")
                    
            elif choice == '2':
                print("Thank you for using the Book Recommender! Goodbye!")
                break
                
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()

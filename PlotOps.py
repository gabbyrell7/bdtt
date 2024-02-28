import matplotlib.pyplot as plt
import pandas as pd

class PlotOps:
    def __init__(self, df):
        self.df = df

    def graph_songs_per_year(self):
        # Convert the release_year column to numeric to ensure proper sorting
        self.df['release_year'] = pd.to_numeric(self.df['release_year'], errors='coerce')

        # Plot the distribution of songs released in each year
        plt.figure(figsize=(12, 6))
        self.df['release_year'].value_counts().sort_index().plot(kind='bar', color='skyblue')
        plt.title('Distribution of Songs Released Each Year')
        plt.xlabel('Release Year')
        plt.ylabel('Number of Songs')
        plt.show(block=False)

    def graph_top_10_songs(self):
        # Convert the release_year column to numeric to ensure proper sorting
        self.df['popularity'] = pd.to_numeric(self.df['popularity'], errors='coerce')

        # Sort DataFrame by popularity in descending order
        pop_df = self.df.sort_values(by='popularity', ascending=False)

        # Plot the top 10 songs based on popularity
        top_10_df = pop_df.head(10)

        # Plot the distribution of songs released in each year
        plt.figure(figsize=(12, 6))
        plt.barh( top_10_df['track_name'], top_10_df['popularity'], color='blueviolet')
        plt.title('Top 10 Songs Based on Popularity')
        plt.xlabel('Track Name')
        plt.ylabel('Popularity')
        plt.tight_layout()
        plt.show()
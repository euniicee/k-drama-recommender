# Import libraries
import pandas as pd
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
db_name = os.getenv("DB_NAME")
print(f"Database Name: {db_name}")

# Input Csv Files
dataframe_1 = pd.read_csv(
    r"/Users/euniceoladele/K-Drama Project/k-drama-recommender/data/kdrama.csv"
)
dataframe_2 = pd.read_csv(r"/Users/euniceoladele/K-Drama Project/kdrama_list.csv")
dataframe_3 = pd.read_csv(r"/Users/euniceoladele/K-Drama Project/k_dramas_2026.csv")

# Drop columns from database_2
dataframe_2.drop(
    columns=["Unnamed: 0", "Sinopsis", "Content Rating", "Tags", "img url"],
    inplace=True,
)

# Rename columns in dataframe_2 to match the column names in dataframe
dataframe_2.rename(columns={"Name": "Drama Name"}, inplace=True)
dataframe_2.rename(columns={"Score": "Rating(Out of 10)"}, inplace=True)
dataframe_2.rename(columns={"Episode": "No of Episodes"}, inplace=True)
dataframe_2.rename(columns={"Main Cast": "Actors"}, inplace=True)

# Concatenate the two dataframes
dataframe = pd.concat([dataframe_1, dataframe_2, dataframe_3], ignore_index=True)

# Remove duplicates based on the 'Drama Name' column
dataframe.drop_duplicates(subset=["Drama Name"], inplace=True)

print(len(dataframe))

# Split the Genre column into a list of genres
dataframe["Genre"] = dataframe["Genre"].str.split(",")


# Strip whitespace from each genre in the list
def stripitems(items):
    if isinstance(items, list):
        return [item.strip() for item in items]
    else:
        return []


# Apply the stripitems function to the Genre column
dataframe["Genre"] = dataframe["Genre"].apply(stripitems)
print(dataframe["Genre"].head(10))

# Split the Actors column into a list of actors
dataframe["Actors"] = dataframe["Actors"].str.split(",")
dataframe["Actors"] = dataframe["Actors"].apply(stripitems)

dataframe["No of Episodes"] = (
    dataframe["No of Episodes"].astype(str).str.replace("Episodes", "").str.strip()
)
dataframe["No of Episodes"] = pd.to_numeric(
    dataframe["No of Episodes"], errors="coerce"
)
print(dataframe["Actors"].head(10))

print(dataframe_2.columns)

print(dataframe.head(20))
print(dataframe_2.columns)

# Save the combined dataframe to a new CSV file
dataframe.to_csv("combined_kdrama_data.csv", index=False)

# Replace NaN values with None
dataframe = dataframe.astype(object).where(pd.notnull(dataframe), None)

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=db_name,
)

# Create a cursor object to interact with the database
cursor = connection.cursor()
cursor.execute("SHOW DATABASES")
print(cursor.fetchall())
print(dataframe_2.columns)

# Create the dramas table
for index, row in dataframe.iterrows():
    name = row["Drama Name"]
    rating = row["Rating(Out of 10)"]
    actors = ", ".join(row["Actors"])  # Join the list of actors into a string
    viewership_rate = row["Viewship Rate"]
    director = row["Director"]
    writer = row["Writer"]
    year = row["Year"]
    episodes = row["No of Episodes"]
    network = row["Network"]

    # Insert data into the database
    cursor.execute(
        "INSERT INTO dramas (name, rating, viewership_rate, director, writer, year, episodes, network) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (name, rating, viewership_rate, director, writer, year, episodes, network),
    )
    drama_id = cursor.lastrowid

    for genre in row["Genre"]:
        cursor.execute("SELECT id FROM genres WHERE name = %s", (genre,))
        genre_id = cursor.fetchone()
    if not genre_id:
        cursor.execute("INSERT INTO genres (name) VALUES (%s)", (genre,))
        genre_id = cursor.lastrowid
    else:
        genre_id = genre_id[0]
    cursor.execute(
        "INSERT INTO drama_genres (drama_id, genre_id) VALUES (%s, %s)",
        (drama_id, genre_id),
    )

    # Insert actors into the actors table and create relationships in the drama_actors table
    for actor in row["Actors"]:
         cursor.execute("SELECT id FROM actors WHERE name = %s", (actor,))
         actor_id = cursor.fetchone()
         if not actor_id:
            cursor.execute("INSERT INTO actors (name) VALUES (%s)", (actor,))
            actor_id = cursor.lastrowid
         else:
            actor_id = actor_id[0]
    cursor.execute(
        "INSERT INTO drama_actors (drama_id, actor_id) VALUES (%s, %s)",
        (drama_id, actor_id),
    )
connection.commit()

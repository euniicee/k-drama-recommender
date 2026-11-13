import fastapi
from fastapi import FastAPI, HTTPException
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables
load_dotenv() 

# Initialize FastAPI app
app = fastapi.FastAPI()

# Define allowed origins for CORS
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a function to establish a connection to the MySQL database
app = fastapi.FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Mine Api!"}

# Define a function to establish a connection to the MySQL database
def get_connection():
    connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"))
    return connection

# Define API endpoints for retrieving dramas, genres, and recommendations
@app.get("/dramas")
def get_dramas():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dramas LIMIT 20")
    dramas = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"dramas": dramas}

# Define an API endpoint to retrieve all genres from the database
@app.get("/genres")  
def get_genres():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute =("SELECT * FROM genres")
    genres = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"genres": genres}

# Define an API endpoint to retrieve dramas by genre from the database
@app.get("/dramas/by-genre")
def get_dramas_by_genre(genre: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT d.* FROM dramas d JOIN drama_genres dg ON d.id = dg.drama_id JOIN genres g ON dg.genre_id = g.id WHERE g.name = %s ORDER BY d.rating DESC", (genre,))
    dramas = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"dramas": dramas}
    
# Define an API endpoint to retrieve a specific drama by its ID from the database    
@app.get("/dramas/{drama_id}")
def get_drama_by_id(drama_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dramas WHERE id = %s", (drama_id,))
    drama = cursor.fetchone()
    cursor.close()
    connection.close()
    if not drama:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"drama": drama}

# Define an API endpoint to retrieve drama recommendations based on shared genres
@app.get("/dramas/{drama_id}/recommendations")
def get_drama_recommendations(drama_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT d.* , COUNT(*) AS shared_genres, GROUP_CONCAT(g.name) AS matched_genres FROM dramas d JOIN drama_genres dg ON d.id = dg.drama_id JOIN genres g ON g.id = dg.genre_id WHERE dg.genre_id IN (SELECT genre_id FROM drama_genres WHERE drama_id = %s) AND d.id != %s GROUP BY d.id ORDER BY shared_genres DESC, d.rating DESC LIMIT 10", (drama_id, drama_id))
    recommendations = cursor.fetchall()
    cursor.close()
    connection.close()
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return {"recommendations": recommendations}

# Define an API endpoint to retrieve drama recommendations based on a list of liked dramas
@app.get("/recommendations")
def get_recommendations(liked: list[int] = Query([])):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    if not liked:
        cursor.execute('SELECT * FROM dramas ORDER BY rating DESC LIMIT 10')
        recommendations = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"dramas": recommendations} 
    placeholders = ','.join(['%s'] * len(liked))
    cursor.execute(f"SELECT d.* , COUNT(*) AS shared_genres, GROUP_CONCAT(g.name) AS matched_genres FROM dramas d JOIN drama_genres dg ON d.id = dg.drama_id  JOIN genres g ON g.id = dg.genre_id WHERE dg.genre_id IN (SELECT genre_id FROM drama_genres WHERE drama_id IN ({placeholders}) ) AND d.id NOT IN ({placeholders})  GROUP BY d.id  ORDER BY shared_genres DESC, d.rating DESC  LIMIT 20", tuple(liked + liked))
    recommendations = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"dramas": recommendations}
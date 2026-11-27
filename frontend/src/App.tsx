import { useState, useEffect } from "react";
import type { Drama } from "./types";
import DramaCard from "./DramaCard";
import type { Genre } from "./types";

function App() {
  const [dramas, setDramas] = useState<Drama[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);
  const [likedIds, setLikedIds] = useState<number[]>(() => {
    const saved = localStorage.getItem("likedIds");
    if (saved === null) {
      return [];
    }
    return JSON.parse(saved);
  });

  useEffect(() => {
    if (selectedGenre == null) {
      fetch("http://127.0.0.1:8000/dramas")
        .then((response) => response.json())
        .then((data) => setDramas(data.dramas))
        .catch((error) => console.error("Error fetching dramas:", error));
    } else {
      fetch(
        `http://127.0.0.1:8000/dramas/by-genre?genre=${encodeURIComponent(selectedGenre)}`,
      )
        .then((response) => response.json())
        .then((data) => setDramas(data.dramas))
        .catch((error) => console.error("Error fetching dramas", error));
    }
  }, [selectedGenre]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/genres")
      .then((response) => response.json())
      .then((data) => setGenres(data.genres))
      .catch((error) => console.error("Error fetching genres", error));
  }, []);

  useEffect (() => {
    localStorage.setItem("likedIds", JSON.stringify(likedIds));
  }, [likedIds]);

  function toggleLike(id: number) {
    if (likedIds.includes(id)) {
      setLikedIds(likedIds.filter((x) => x !== id));
    } else {
      setLikedIds([...likedIds, id]);
    }
  }
  return (
    <div>
      <p>Liked: {likedIds.join(",")}</p>
      <button onClick={() => setSelectedGenre(null)}>All</button>
      {genres.map((genre) => (
        <button key={genre.id} onClick={() => setSelectedGenre(genre.name)}>
          {genre.name}
        </button>
      ))}
      {dramas.map((drama) => (
        <DramaCard
          key={drama.id}
          drama={drama}
          liked={likedIds.includes(drama.id)}
          onLike={() => toggleLike(drama.id)}
        />
      ))}
    </div>
  );
}
export default App;

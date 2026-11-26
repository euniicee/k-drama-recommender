import { useState, useEffect } from "react";
import type { Drama } from "./types";
import DramaCard from "./DramaCard";
import type { Genre } from "./types";

function App() {
  const [dramas, setDramas] = useState<Drama[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);

  useEffect(() => {
    if (selectedGenre == null) {
      fetch("http://127.0.0.1:8000/dramas")
        .then((response) => response.json())
        .then((data) => setDramas(data.dramas))
        .catch((error) => console.error("Error fetching dramas:", error));
    }
    else {
      fetch(`http://127.0.0.1:8000/dramas/by-genre?genre=${encodeURIComponent(selectedGenre)}`)
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

  return (
    <div>
       <button onClick={() => setSelectedGenre(null)}>All</button>

      {genres.map((genre) => (
        <button key={genre.id} onClick={() => setSelectedGenre(genre.name)}>
          {genre.name}
        </button>
      ))}
      {dramas.map((drama) => (
        <DramaCard key={drama.id} drama={drama} />
      ))}
    </div>
  );
}
export default App;

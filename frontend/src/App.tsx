import { useState, useEffect} from 'react';

 type Drama = {
    id: number;
    name: string;
    rating: number | null;
    viewership_rate: number | null;
    director: string |  null;
    writer: string | null;
    year: number | null;
    episodes: number | null;
    network: string | null; 
  }

function App() {
const [dramas, setDramas] = useState<Drama[]>([]);
useEffect(() => {
  fetch('http://127.0.0.1:8000/dramas')
  .then(response => response.json()
)
  .then(data => setDramas(data.dramas))
  .catch(error => console.error('Error fetching dramas:', error));
}, []);

return (
  <ul>
    {dramas.map(drama => (
      <li key={drama.id}>{drama.name}</li>
   ))}
  </ul>

 )
}
export default App;


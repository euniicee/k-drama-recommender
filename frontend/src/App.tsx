import { useState, useEffect} from 'react';
import type { Drama} from './types';
import DramaCard from './DramaCard';

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
  <div>
    {dramas.map(drama => (
      <DramaCard key={drama.id} drama={drama}/>
   ))}
  </div>

 )
}
export default App;
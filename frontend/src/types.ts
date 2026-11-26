import { useState, useEffect} from 'react';

 export type Drama = {
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

  export type Genre = {
    id: number;
    name: string;
  }




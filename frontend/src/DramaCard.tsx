import type { Drama } from "./types";

type DramaCardProps = {
  drama: Drama;
  liked: boolean;
  onLike: () => void;
  
};

function DramaCard({ drama, liked, onLike}: DramaCardProps) {
  return (
    <div>
      <h3>{drama.name}</h3>
      <p>{drama.year ?? "Year unknown"}</p>
      <p>{drama.rating ?? "rating unknown"}</p>
      <p>{drama.network ?? "Network unknown"}</p>
      <button onClick={onLike}>{liked ? "Liked": "Like"}</button>
    </div>
  );
}

export default DramaCard;

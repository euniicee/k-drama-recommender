import type { Drama } from "./types";

type DramaCardProps = {
  drama: Drama;
  onLike: () => void;
};

function DramaCard({ drama, onLike }: DramaCardProps) {
  return (
    <div>
      <h3>{drama.name}</h3>
      <p>{drama.year ?? "Year unknown"}</p>
      <p>{drama.rating ?? "rating unknown"}</p>
      <p>{drama.network ?? "Network unknown"}</p>
      <button onClick={onLike}>Like</button>
    </div>
  );
}

export default DramaCard;

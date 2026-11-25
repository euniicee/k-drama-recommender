import type { Drama } from "./types";

type DramaCardProps = { 
    drama: Drama;
}

function DramaCard  ({drama}: DramaCardProps) {
    return (
        <div>
            <h3>{drama.name}</h3>
            <p>{drama.year ?? "Year unknown"}</p>
            <p>{drama.rating ?? "rating unknown"}</p>
            <p>{drama.network ?? "Network unknown"}</p>

        </div>
    )
}

export default DramaCard
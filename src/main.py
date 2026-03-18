from api import fetch_pokemon_batch
from load import ensure_indexes, insert_many_documents


def main() -> None:
    """
    Run the ingestion pipeline:
    fetch Pokémon data from the API and store raw documents in MongoDB.
    """
    limit = 5
    offset = 0

    print("[PIPELINE] Ensuring indexes...")
    ensure_indexes()

    print(f"[PIPELINE] Fetching Pokémon batch (limit={limit}, offset={offset})...")
    pokemon_batch = fetch_pokemon_batch(limit=limit, offset=offset)

    print(f"[PIPELINE] Inserting {len(pokemon_batch)} Pokémon into MongoDB...")
    insert_many_documents(pokemon_batch)

    print("[PIPELINE] Done.")


if __name__ == "__main__":
    main()

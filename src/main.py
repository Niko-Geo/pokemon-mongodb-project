from api import fetch_pokemon_batch
from config import get_settings
from load import ensure_indexes, insert_many_documents


def main() -> None:
    """
    Run the ingestion pipeline:
    fetch Pokémon data from the API and store raw documents in MongoDB.
    """
    settings = get_settings()

    print("[PIPELINE] Ensuring indexes...")
    ensure_indexes()

    print(
        f"[PIPELINE] Fetching Pokémon batch "
        f"(limit={settings.api_limit}, offset={settings.api_offset})..."
    )
    pokemon_batch = fetch_pokemon_batch(
        limit=settings.api_limit,
        offset=settings.api_offset,
    )

    print(f"[PIPELINE] Inserting {len(pokemon_batch)} Pokémon into MongoDB...")
    insert_many_documents(pokemon_batch)

    print("[PIPELINE] Done.")


if __name__ == "__main__":
    main()

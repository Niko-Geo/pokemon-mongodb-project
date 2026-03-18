from api import fetch_pokemon_batch
from config import get_settings
from load import ensure_indexes, insert_many_documents
from transform import create_clean_collection


def main() -> None:
    settings = get_settings()

    print("[PIPELINE] Ensuring indexes...")
    ensure_indexes()

    print(
        "[PIPELINE] Fetching Pokémon batch "
        f"(limit={settings.api_limit}, offset={settings.api_offset})..."
    )
    pokemon_batch = fetch_pokemon_batch(
        limit=settings.api_limit,
        offset=settings.api_offset,
    )

    print(f"[PIPELINE] Inserting {len(pokemon_batch)} Pokémon into MongoDB...")
    insert_many_documents(pokemon_batch)

    print("[PIPELINE] Creating cleaned collection...")
    create_clean_collection()

    print("[PIPELINE] Done.")


if __name__ == "__main__":
    main()

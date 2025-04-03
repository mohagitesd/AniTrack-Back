import httpx


ANILIST_API_URL = 'https://graphql.anilist.co'

# 
async def get_work_details(anilist_id: str):
    query = """
    query ($id: Int) {
      Media(id: $id) {
        id
        title {
          romaji
          english
          native
        }
        type
        format
        status
        description
        episodes
        chapters
        genres
        averageScore
        startDate {
          year
        }
        studios {
          nodes {
            name
          }
        }
      }
    }
    """

    variables = {"id": int(anilist_id)}

    async with httpx.AsyncClient() as client:
        response = await client.post(ANILIST_API_URL, json={"query": query, "variables": variables})
        response.raise_for_status()
        return response.json()["data"]["Media"]

# fonction pour rechercher des oeuvres
async def search_works(search=None, type=None, genre=None, status=None):
    query = """
    query ($search: String, $type: MediaType, $genre: String, $status: MediaStatus) {
      Page(perPage: 20) {
        media(
          search: $search,
          type: $type,
          genre_in: [$genre],
          status: $status
        ) {
          id
          title {
            romaji
            english
          }
          type
          genres
          averageScore
          startDate {
            year
          }
          coverImage {
            large
          }
        }
      }
    }
    """

    variables = {
        "search": search,
        "type": type,
        "genre": genre,
        "status": status
    }

    #  Nettoyer les champs vides
    variables = {k: v for k, v in variables.items() if v is not None}

    print("[DEBUG] Variables envoyées à Anilist:")
    for k, v in variables.items():
        print(f"  - {k}: {v}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://graphql.anilist.co",
            json={"query": query, "variables": variables}
        )

    if response.status_code != 200:
        print("[Anilist Error]", response.text)  # log d’erreur
        response.raise_for_status()

    return response.json()["data"]["Page"]["media"]


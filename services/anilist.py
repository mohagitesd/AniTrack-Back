import httpx

ANILIST_API_URL = "https://graphql.anilist.co"

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

from elasticsearch_dsl import Q, connections
from storage.schemas import CapitalWeatherDBModel

from .schema import CapitalWeatherEs


class BookSearchService:
    def __init__(self):
        self.es = connections.get_connection()
        if not self.es.indices.exists(index=CapitalWeatherEs.Index.name):
            CapitalWeatherEs.init()

    @staticmethod
    def save(capital_weather_model: CapitalWeatherDBModel):
        book = CapitalWeatherEs(
            meta={"id": capital_weather_model.id},
            entity_id=capital_weather_model.id,
            capital_name=capital_weather_model.capital.name,
            location={
                "lat": capital_weather_model.capital.lat,
                "lon": capital_weather_model.capital.lng,
            },
            updated_at=capital_weather_model.updated_at,
        )
        book.save()

    @staticmethod
    def search_by_country_name(search_term: str):
        query = CapitalWeatherEs.search()
        query = query.extra(
            track_scores=True,
            _source={
                "exclude": [
                    # "entity_id",
                    "location",
                    "updated_at",
                    "added_at",
                ]
            },
        )
        query = query.query(Q("match", capital_name={"query": search_term}))
        return query.execute().hits

    @staticmethod
    def search_by_location(lat: float, lng: float):
        return CapitalWeatherEs.search().filter(
            "location", distance="1000km", headquarter_location={"lat": lat, "lon": lng}
        )

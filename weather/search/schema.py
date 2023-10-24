from datetime import datetime

from elasticsearch_dsl import Date, Document, Keyword, Text, GeoPoint


class CapitalWeatherEs(Document):
    entity_id = Text(fields={"keyword": Keyword()}, required=True)
    capital_name = Text(fields={"keyword": Keyword()}, required=True)
    location = GeoPoint(required=True)
    updated_at = Date(default_timezone="UTC", required=True)
    added_at = Date(default_timezone="UTC", required=True)

    class Index:
        name = "capital_weather"
        settings = {
            "analysis": {
                "stemmer": {"tokenizer": "standard", "filter": ["lowercase", "stemmer"]}
            }
        }

    def save(self, **kwargs):
        if self.added_at is None:
            self.added_at = datetime.utcnow()
        return super().save(**kwargs)

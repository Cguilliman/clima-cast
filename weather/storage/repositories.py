import typing
from datetime import datetime, timezone

from app.mongo import collection
from bson.objectid import ObjectId
from storage.schemas import CapitalWeatherModel, CapitalWeatherDBModel


class CapitalWeatherNotExists(Exception):
    pass


class WeatherRepository:
    @staticmethod
    def get_capital_weather_by_name(
        name: str,
    ) -> typing.Optional[CapitalWeatherDBModel]:
        document = collection.find_one({"capital.name": name})
        if not document:
            return None
        document["id"] = str(document.get("_id"))
        return CapitalWeatherDBModel(**document)

    @staticmethod
    def get_capital_weather_by_id(
        object_id: str,
    ) -> typing.Optional[CapitalWeatherDBModel]:
        document = collection.find_one({"_id": ObjectId(object_id)})
        if not document:
            raise CapitalWeatherNotExists()
        document["id"] = str(document.get("_id"))
        return CapitalWeatherDBModel(**document)

    @staticmethod
    def save_capital_weather(
        capital_weather: CapitalWeatherModel,
    ) -> CapitalWeatherDBModel:
        capital_weather_data = capital_weather.model_dump()
        capital_weather_name_to_update = capital_weather_data.get("capital").get("name")
        capital_weather_data["updated_at"] = datetime.now(tz=timezone.utc)

        exists_capital_weather = WeatherRepository.get_capital_weather_by_name(
            capital_weather_name_to_update
        )

        if exists_capital_weather is not None:
            result = collection.update_one(
                {"_id": ObjectId(exists_capital_weather.id)},
                {"$set": capital_weather_data},
            )
            saved_capital_weather_id = exists_capital_weather.id
        else:
            capital_weather_data["created_at"] = datetime.now(tz=timezone.utc)
            result = collection.insert_one(capital_weather_data)
            saved_capital_weather_id = str(result.inserted_id)

        assert result.acknowledged
        capital_weather_model = WeatherRepository.get_capital_weather_by_id(
            saved_capital_weather_id
        )
        return capital_weather_model

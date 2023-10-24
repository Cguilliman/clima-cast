import time
import typing
from datetime import datetime, timezone

from loguru import logger
from search.repository import BookSearchService
from storage.repositories import WeatherRepository
from storage.schemas import CapitalWeatherDBModel, CapitalWeatherModel


class WeatherCRUDService:
    @staticmethod
    def save_capital_weather(
        capital_weather: CapitalWeatherModel,
    ) -> CapitalWeatherDBModel:
        saved_capital_weather: CapitalWeatherDBModel = (
            WeatherRepository.save_capital_weather(capital_weather)
        )
        BookSearchService().save(saved_capital_weather)
        return saved_capital_weather

    @staticmethod
    def get_capital_weather_by_capital_name(
        name: str,
    ) -> typing.List[CapitalWeatherDBModel]:
        search_results = BookSearchService().search_by_country_name(name)
        return [
            WeatherRepository.get_capital_weather_by_id(search_result.entity_id)
            for search_result in search_results
        ]

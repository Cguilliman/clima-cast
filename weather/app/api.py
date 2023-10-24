import typing
from datetime import datetime

import weather_pb2_grpc

from loguru import logger
from grpc import ServicerContext
from weather_pb2 import (
    WeatherEntity,
    CapitalEntity,
    UpdateCapitalRequest,
    EmptyResponse,
    CapitalWeather,
    FetchByCapitalNameRequest,
    CapitalsWeatherResponse,
    CapitalWeather,
)
from services.weather_crud import WeatherCRUDService
from storage.schemas import (
    CapitalWeatherDBModel,
    CapitalWeatherModel,
    CapitalModel,
    WeatherModel,
)

import grpc


class WeatherServicer(weather_pb2_grpc.WeatherServicer):
    def Update(
        self, request: UpdateCapitalRequest, context: ServicerContext
    ) -> EmptyResponse:
        logger.info("Update")
        capital_weather = CapitalWeatherModel(
            capital=CapitalModel(
                name=request.capital.name,
                lat=request.capital.lat,
                lng=request.capital.lng,
            ),
            weather=WeatherModel(
                main=request.weather.main,
                weather=[item.value for item in request.weather.weather],
                wind=request.weather.wind,
            ),
            send_at=datetime.fromtimestamp(
                request.send_at.seconds + request.send_at.nanos / 1e9
            ),
        )
        logger.info(capital_weather)
        WeatherCRUDService.save_capital_weather(capital_weather)
        return EmptyResponse()

    def FetchByCapitalName(self, request: FetchByCapitalNameRequest, context):
        capitals_weathers: typing.List[CapitalWeatherDBModel] = WeatherCRUDService.get_capital_weather_by_capital_name(request.name)
        if len(capitals_weathers) == 0:
            context.abort(grpc.StatusCode.NOT_FOUND, "Found nothing")
        response = CapitalsWeatherResponse(
            data=[
                CapitalWeather(
                    capital=CapitalEntity(
                        name=capital_weather.capital.name,
                        lat=capital_weather.capital.lat,
                        lng=capital_weather.capital.lng,
                    ),
                    weather=WeatherEntity(
                        main=capital_weather.weather.main,
                        weather=[
                            WeatherEntity.SubWeather(value=item)
                            for item in capital_weather.weather.weather
                        ],
                        wind=capital_weather.weather.wind,
                    )
                ) for capital_weather in capitals_weathers
            ]
        )
        return response

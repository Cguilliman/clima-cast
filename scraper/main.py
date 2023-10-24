import asyncio
import os
import typing
from dataclasses import dataclass
from pprint import pprint
from datetime import datetime
from loguru import logger

import aiohttp
from google.protobuf.timestamp_pb2 import Timestamp
from dotenv import load_dotenv
import grpc
from weather_pb2 import WeatherEntity, CapitalEntity, UpdateCapitalRequest
from weather_pb2_grpc import WeatherStub


load_dotenv()
WEATHER_API_KEY = os.getenv("API_KEY")
IS_TEST = os.getenv("IS_TEST", False)

SCRAPER_HOST = os.getenv("SCRAPER_HOST", "localhost")

logger.add("run.log")

@dataclass
class Weather:
    main: typing.Dict
    weather: typing.Dict
    wind: typing.Dict


@dataclass
class Capital:
    name: str
    lat: float
    lng: float
    weather: typing.Optional[Weather] = None


class WeatherService:
    COUNTRIES_EP = "https://restcountries.com/v3.1/all"
    WEATHER_EP = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={key}"

    def __init__(self):
        self.channel = grpc.insecure_channel(f"{SCRAPER_HOST}:50051")

    async def get_capitals(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.COUNTRIES_EP) as resp:
                countries = await resp.json()
                for country in countries:
                    if not country.get("capitalInfo"):
                        continue
                    country_lat, country_lng = country.get("capitalInfo").get("latlng")
                    yield Capital(
                        name=country.get("capital")[0], lat=country_lat, lng=country_lng
                    )

    async def get_weather(self, capital: Capital):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.WEATHER_EP.format(
                    lat=capital.lat, lng=capital.lng, key=WEATHER_API_KEY
                )
            ) as resp:
                weather_data = await resp.json()
                weather = Weather(
                    main=weather_data.get("main"),
                    weather=weather_data.get("weather"),
                    wind=weather_data.get("wind"),
                )
                capital.weather = weather
                return capital

    async def send_capital_weather(self, capital: Capital):
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now())

        WeatherStub(self.channel).Update(
            UpdateCapitalRequest(
                capital=CapitalEntity(
                    name=capital.name,
                    lat=capital.lat,
                    lng=capital.lng,
                ),
                weather=WeatherEntity(
                    main={key: str(value) for key, value in capital.weather.main.items()},
                    weather=[
                        WeatherEntity.SubWeather(value={key: str(value) for key, value in weather_item.items()})
                        for weather_item in capital.weather.weather
                    ],
                    wind={key: str(value) for key, value in capital.weather.wind.items()},
                ),
                send_at=timestamp
            )
        )

    async def process_capital_weather(self, capital: Capital):
        capital = await self.get_weather(capital=capital)
        await self.send_capital_weather(capital)

    async def main(self):
        capitals = [capital async for capital in self.get_capitals()]
        logger.info(f"Received {len(capitals)}")
        if IS_TEST:
            capitals = capitals[:50]
        await asyncio.gather(
            *[self.process_capital_weather(capital) for capital in capitals]
        )


if __name__ == "__main__":
    async def periodic():
        async def run_processing(f):
            logger.info("Start scraping loop")
            await f
            logger.info("Finish scraping loop")

        while True:
            asyncio.create_task(run_processing(WeatherService().main()))
            await asyncio.sleep(60*5)

    logger.info("Scraper process has started")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(periodic())
    logger.info("Scraper process has down")

import typing
from datetime import datetime

from pydantic import BaseModel


class CapitalModel(BaseModel):
    name: str
    lat: float
    lng: float


class WeatherModel(BaseModel):
    main: typing.Dict
    weather: typing.List[typing.Dict]
    wind: typing.Dict


class CapitalWeatherModel(BaseModel):
    capital: CapitalModel
    weather: typing.Optional[WeatherModel] = None
    send_at: datetime


class CapitalDBModel(CapitalModel):
    pass


class WeatherDBModel(WeatherModel):
    pass


class CapitalWeatherDBModel(BaseModel):
    id: str
    capital: CapitalDBModel
    weather: WeatherDBModel
    send_at: datetime
    created_at: datetime
    updated_at: datetime

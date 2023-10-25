# Sandbox application

## Initial idea

Overhead architecture application that will collect weather for possible capitals, save it and the client will be able to receive this data.
Source data is fetching from: https://restcountries.com/ (country data), https://home.openweathermap.org/api_keys (weather data)

## System design)

- Gateway (golang gin-gonic) a service that is an external interface for accessing weather data
- Scraper - (solid python) a scrapping service, fetch data from resources and send into weather service to process that data
  - MongoDB - collect full weather data
  - ElasticSearch - searching machine
- Weather - (python grpc) a core service that responsible for saving, indexing and processing weather data, also return saved info
- Monitoring system
  - Grafana - metrics dashboard
  - InfluxDB - metrics storage
  - Telegraf - metrics agent

## How to run

### run infrastructure 

`docker-compose -f ./provisioning/docker-compose-infra.yml up --build -d`

### run services

`docker-compose -f ./provisioning/docker-compose-services.yml up --build -d`

### run monitoring

`docker-compose -f ./provisioning/docker-compose-monitoring.yml up --build -d`

## How to test performance

`siege -c 50 -t 1m --content-type="application/json" 'http://localhost/weather/capital-name POST {"name": "Budapest"}'`

package weather

import (
	"clima-cast-gateway/models"
	"clima-cast-gateway/weather_proto"
	"context"
	"log"

	"google.golang.org/grpc"
)

type Connection struct {
	Client weather_proto.WeatherClient
}

func initConnection() Connection {
	// TODO: get from env
	conn, err := grpc.Dial("weather:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Did not connect: %v", err)
		return Connection{}
	}
	// defer conn.Close()

	client := weather_proto.NewWeatherClient(conn)
	return Connection{Client: client}
}

func (connection *Connection) FetchByName(name string) ([]models.CapitalWeatherModel, error) {
	weatherRequest := &weather_proto.FetchByCapitalNameRequest{Name: name}
	response, err := connection.Client.FetchByCapitalName(context.Background(), weatherRequest)
	if err != nil {
		return []models.CapitalWeatherModel{}, err
	}

	searchResponse := make([]models.CapitalWeatherModel, 0)

	for _, item := range response.GetData() {
		var weathers []map[string]string
		for _, weather := range item.Weather.Weather {
			weathers = append(weathers, weather.Value)
		}

		var resItem models.CapitalWeatherModel = models.CapitalWeatherModel{
			Capital: models.CapitalModel{
				Name: item.Capital.Name,
				Lat:  float64(item.Capital.Lat),
				Lng:  float64(item.Capital.Lng),
			},
			Weather: models.WeatherModel{
				Main:    item.Weather.Main,
				Wind:    item.Weather.Wind,
				Weather: weathers,
			},
		}
		searchResponse = append(searchResponse, resItem)
	}
	return searchResponse, nil
}

var ExistsConnection Connection = initConnection()

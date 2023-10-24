package models

type CapitalModel struct {
	Name string  `json:"name"`
	Lat  float64 `json:"lat"`
	Lng  float64 `json:"lng"`
}

type WeatherModel struct {
	Main    map[string]string   `json:"main"`
	Weather []map[string]string `json:"weather"`
	Wind    map[string]string   `json:"wind"`
}

type CapitalWeatherModel struct {
	Capital CapitalModel `json:"capital"`
	Weather WeatherModel `json:"weather"`
}

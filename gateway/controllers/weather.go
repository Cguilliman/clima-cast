package controllers

import (
	"clima-cast-gateway/metrics"
	"clima-cast-gateway/weather"
	"net/http"

	"github.com/gin-gonic/gin"
)

type CapitalWeather struct {
	Name string `json:"name" binding:"required"`
}

func IsAlive(context *gin.Context) {
	context.JSON(http.StatusOK, gin.H{"data": "OK"})
}

func FetchByCapitalNameController(context *gin.Context) {
	var input CapitalWeather
	metrics.SaveMetric("requests", 1)

	if err := context.ShouldBindJSON(&input); err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		metrics.SaveMetric("bad_requests", 1)
		return
	}

	capitalWeather, err := weather.ExistsConnection.FetchByName(input.Name)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		metrics.SaveMetric("bad_requests_to_weather_service", 1)
		return
	}

	metrics.SaveMetric("success_requests", 1)
	context.JSON(http.StatusOK, gin.H{"data": capitalWeather})
}

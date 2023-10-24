package controllers

import (
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

	if err := context.ShouldBindJSON(&input); err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	capital_weather, err := weather.ExistsConnection.FetchByName(input.Name)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	context.JSON(http.StatusOK, gin.H{"data": capital_weather})
}

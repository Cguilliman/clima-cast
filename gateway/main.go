// save go bin path in PATH - export PATH=$PATH:~/go/bin
// protoc -I ../protobufs/ --go_out=./weather_proto --go_opt=paths=source_relative --go-grpc_out=./weather_proto --go-grpc_opt=paths=source_relative ../protobufs/weather.proto
package main

import (
	"clima-cast-gateway/controllers"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	publicRouter := router.Group("/weather")
	publicRouter.GET("/helthcheck", controllers.IsAlive)
	publicRouter.POST("/capital-name", controllers.FetchByCapitalNameController)

	router.Run(":8000")
}

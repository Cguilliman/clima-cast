package middlewares

import (
	"clima-cast-gateway/metrics"
	"time"

	"github.com/gin-gonic/gin"
)

func HttpConnectionMiddleware() gin.HandlerFunc {
	return func(context *gin.Context) {
		metrics.SaveMetric("http_connections", 1)
		start := time.Now()
		context.Next()
		handlerTime := time.Since(start)
		if handlerTime >= 1000 {
			metrics.SaveMetric("slow_requests", 1)
		}
	}
}

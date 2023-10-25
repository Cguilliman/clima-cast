package metrics

import (
	"fmt"

	"github.com/mdaffin/go-telegraf"
)

func SaveMetric(metric string, value int) {
	client, err := telegraf.NewTCP("telegraf:8094")
	if err != nil {
		fmt.Println("Failed1")
		fmt.Println(err)
	}
	defer client.Close()

	m := telegraf.MeasureInt("gateway", metric, value)
	if err := client.Write(m); err != nil {
		fmt.Println("Failed2")
		fmt.Println(err)
	}
}

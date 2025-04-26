package main

import (
	"log/slog"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	cfg := NewConfig()
	db := GetDB(cfg)
	defer db.Close()
	repo := NewRepo(db)
	service := NewService(repo)
	controller := NewController(service)
	cronjob := NewCronJob(service)

	scheduler(cronjob)
	err := server(controller)
	if err != nil {
		slog.Error(err.Error())
	}
}

func server(controller *Controller) error {
	e := echo.New()

	e.Use(middleware.Recover())
	e.Use(
		// https://echo.labstack.com/docs/middleware/static
		middleware.StaticWithConfig(middleware.StaticConfig{
			Root:  "./dist",
			HTML5: true,
		}),
	)

	api := e.Group("/api")
	api.GET("/winning_data", controller.GetWinningData)

	err := e.Start(":8080")

	return err
}

func scheduler(cronjob *CronJob) {
	go func() {
		// 先 10s 后执行一次，然后每天早上 8:00 执行一次
		nextTime := time.Now().Add(10 * time.Second)
		for {
			defer func() {
				if r := recover(); r != nil {
					slog.Error("cronjob panic!", "cronjob", "FetchLotteryData", "error", r)
				}
			}()
			time.Sleep(time.Until(nextTime))
			cronjob.FetchLotteryData()
			today8 := time.Date(nextTime.Year(), nextTime.Month(), nextTime.Day(), 8, 0, 0, 0, nextTime.Location())
			if nextTime.Before(today8) {
				nextTime = today8
			} else {
				nextTime = today8.Add(24 * time.Hour)
			}
		}
	}()
}

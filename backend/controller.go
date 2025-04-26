package main

import "github.com/labstack/echo/v4"

type Response struct {
	Code    int         `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

type Controller struct {
	service *Service
}

func NewController(service *Service) *Controller {
	return &Controller{service: service}
}

func (c *Controller) GetWinningData(ctx echo.Context) error {
	data, err := c.service.GetWinningData(ctx.Request().Context())
	if err != nil {
		return ctx.JSON(200, Response{
			Code:    1,
			Message: err.Error(),
			Data:    nil,
		})
	} else {
		return ctx.JSON(200, Response{
			Code:    0,
			Message: "success",
			Data:    data,
		})
	}
}

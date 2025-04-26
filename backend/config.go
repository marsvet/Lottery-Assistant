package main

import "os"

type Config struct {
	EnvName string
	DB      string
}

func NewConfig() *Config {
	cfg := &Config{}
	cfg.EnvName = os.Getenv("ENV_NAME")
	if cfg.EnvName != "dev" && cfg.EnvName != "prod" {
		panic("ENV_NAME must be dev or prod")
	}
	if cfg.EnvName == "dev" {
		cfg.DB = "../database.sqlite3"
	} else {
		cfg.DB = "./database.sqlite3"
	}
	return cfg
}

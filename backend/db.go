package main

import (
	"sync"

	"github.com/jmoiron/sqlx"
	_ "github.com/mattn/go-sqlite3"
)

var (
	db   *sqlx.DB
	once sync.Once
)

func GetDB(cfg *Config) *sqlx.DB {
	once.Do(func() {
		var err error
		db, err = sqlx.Open("sqlite3", cfg.DB)
		if err != nil {
			panic(err)
		}
		err = db.Ping()
		if err != nil {
			panic(err)
		}
	})
	return db
}

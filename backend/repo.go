package main

import (
	"context"

	"github.com/jmoiron/sqlx"
)

type IRepo interface {
	GetWinningData(ctx context.Context) ([]WinningData, error)
	GetLatestDate(ctx context.Context) (string, error)
	InsertLotteryData(ctx context.Context, args []interface{}) error
}

type Repo struct {
	db *sqlx.DB
}

func NewRepo(db *sqlx.DB) *Repo {
	return &Repo{db: db}
}

// GetWinningData 从“中奖数据”视图中获取所有中奖数据
func (r *Repo) GetWinningData(ctx context.Context) ([]WinningData, error) {
	sql := "SELECT * FROM 中奖数据"
	var result []WinningData
	err := r.db.SelectContext(ctx, &result, sql)
	if err != nil {
		return nil, err
	}
	return result, nil
}

// GetLatestDate 从“lottery_data”表中获取最新的开奖日期
func (r *Repo) GetLatestDate(ctx context.Context) (string, error) {
	sql := "SELECT max(开奖日期) FROM lottery_data"
	var result string
	err := r.db.GetContext(ctx, &result, sql)
	if err != nil {
		return "", err
	}
	return result, nil
}

// InsertLotteryData 向“lottery_data”表中插入新的开奖数据
func (r *Repo) InsertLotteryData(ctx context.Context, args []interface{}) error {
	sql := "INSERT INTO lottery_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	_, err := r.db.ExecContext(ctx, sql, args...)
	if err != nil {
		return err
	}
	return nil
}

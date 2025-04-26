package main

import (
	"context"
	"testing"
)

type RepoMock struct{}

func (r *RepoMock) GetWinningData(ctx context.Context) ([]WinningData, error) {
	return []WinningData{
		{
			Issue:    "2023001",
			Date:     "2023-01-01",
			Hundreds: 1,
			Tens:     2,
			Units:    3,
		},
	}, nil
}

func (r *RepoMock) GetLatestDate(ctx context.Context) (string, error) {
	return "2025-01-01", nil
}

func (r *RepoMock) InsertLotteryData(ctx context.Context, args []interface{}) error {
	return nil
}

func TestServiceGetWinningData(t *testing.T) {
	repo := &RepoMock{}
	service := NewService(repo)
	data, err := service.GetWinningData(context.Background())
	if err != nil {
		t.Errorf("GetWinningData() error = %v", err)
		return
	}
	t.Logf("GetWinningData(), len(data) = %v, data[0] = %v", len(data), data[0])
}

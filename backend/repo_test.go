package main

import (
	"context"
	"testing"
)

func TestGetWinningData(t *testing.T) {
	cfg := NewConfig()
	db := GetDB(cfg)
	repo := NewRepo(db)
	data, err := repo.GetWinningData(context.Background())
	if err != nil {
		t.Errorf("GetWinningData() error = %v", err)
		return
	}
	t.Logf("GetWinningData(), len(data) = %v, data[0] = %v", len(data), data[0])
}

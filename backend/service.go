package main

import "context"

type Service struct {
	repo IRepo
}

func NewService(repo IRepo) *Service {
	return &Service{repo: repo}
}

func (s *Service) GetWinningData(ctx context.Context) ([][]interface{}, error) {
	result, err := s.repo.GetWinningData(ctx)
	if err != nil {
		return nil, err
	}
	data := make([][]interface{}, 0)
	for _, row := range result {
		rowData := []interface{}{row.Issue, row.Date, row.Hundreds, row.Tens, row.Units}
		data = append(data, rowData)
	}
	return data, nil
}

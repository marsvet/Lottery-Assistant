package main

type CronJob struct {
	service *Service
}

func NewCronJob(service *Service) *CronJob {
	return &CronJob{service: service}
}

func (c *CronJob) FetchLotteryData() error {
	return nil
}

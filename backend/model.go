package main

type WinningData struct {
	Issue    string `db:"期号"`
	Date     string `db:"开奖日期"`
	Hundreds int    `db:"中奖号码_百位"`
	Tens     int    `db:"中奖号码_十位"`
	Units    int    `db:"中奖号码_个位"`
}

type WinningNumber struct {
	Number string `db:"中奖号码"`
}

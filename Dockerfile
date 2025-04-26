FROM node:16-alpine AS fe-build

WORKDIR /app/

COPY ./package.json /app/

RUN set -x; yarn config set registry https://registry.npm.taobao.org/ \
    && yarn install

COPY . /app/

RUN yarn run build



FROM golang:1.23-alpine AS be-build

RUN apk --no-cache add tzdata

WORKDIR /app/

ENV GOPROXY=https://goproxy.cn,direct
COPY go.mod go.sum /app/
RUN go mod download

COPY . /app
RUN CGO_ENABLED=0 GOOS=linux go build



FROM scratch

COPY --from=be-build /usr/share/zoneinfo /usr/share/zoneinfo
ENV TZ=Asia/Shanghai

COPY database.sqlite3 .
COPY --from=fe-build /app/dist/ .
COPY --from=be-build /app/Lottery-Assistant .

CMD ["/Lottery-Assistant"]

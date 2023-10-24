FROM golang:1.21.3

RUN curl -sSfL https://raw.githubusercontent.com/cosmtrek/air/master/install.sh | sh -s -- -b $(go env GOPATH)/bin
RUN mkdir /go/src/clima-cast-gateway/
COPY protobufs/ /protobufs/
COPY ./gateway /go/src/clima-cast-gateway
WORKDIR /go/src/clima-cast-gateway/

RUN go get -d -v ./...
RUN apt-get update && apt-get install -y protobuf-compiler
RUN go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

ENV GOPATH=/go
ENV GOBIN=/go/bin
ENV PATH=$PATH:/go/bin
RUN protoc -I /protobufs/ --go_out=/go/src/clima-cast-gateway/weather_proto --go_opt=paths=source_relative \
    --go-grpc_out=/go/src/clima-cast-gateway/weather_proto --go-grpc_opt=paths=source_relative \
    /protobufs/weather.proto

CMD ["air"]

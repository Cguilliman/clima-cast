// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.3.0
// - protoc             v4.24.4
// source: weather.proto

package weather_proto

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

const (
	Weather_Update_FullMethodName             = "/Weather/Update"
	Weather_FetchByCapitalName_FullMethodName = "/Weather/FetchByCapitalName"
)

// WeatherClient is the client API for Weather service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type WeatherClient interface {
	Update(ctx context.Context, in *UpdateCapitalRequest, opts ...grpc.CallOption) (*EmptyResponse, error)
	FetchByCapitalName(ctx context.Context, in *FetchByCapitalNameRequest, opts ...grpc.CallOption) (*CapitalsWeatherResponse, error)
}

type weatherClient struct {
	cc grpc.ClientConnInterface
}

func NewWeatherClient(cc grpc.ClientConnInterface) WeatherClient {
	return &weatherClient{cc}
}

func (c *weatherClient) Update(ctx context.Context, in *UpdateCapitalRequest, opts ...grpc.CallOption) (*EmptyResponse, error) {
	out := new(EmptyResponse)
	err := c.cc.Invoke(ctx, Weather_Update_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *weatherClient) FetchByCapitalName(ctx context.Context, in *FetchByCapitalNameRequest, opts ...grpc.CallOption) (*CapitalsWeatherResponse, error) {
	out := new(CapitalsWeatherResponse)
	err := c.cc.Invoke(ctx, Weather_FetchByCapitalName_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// WeatherServer is the server API for Weather service.
// All implementations must embed UnimplementedWeatherServer
// for forward compatibility
type WeatherServer interface {
	Update(context.Context, *UpdateCapitalRequest) (*EmptyResponse, error)
	FetchByCapitalName(context.Context, *FetchByCapitalNameRequest) (*CapitalsWeatherResponse, error)
	mustEmbedUnimplementedWeatherServer()
}

// UnimplementedWeatherServer must be embedded to have forward compatible implementations.
type UnimplementedWeatherServer struct {
}

func (UnimplementedWeatherServer) Update(context.Context, *UpdateCapitalRequest) (*EmptyResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Update not implemented")
}
func (UnimplementedWeatherServer) FetchByCapitalName(context.Context, *FetchByCapitalNameRequest) (*CapitalsWeatherResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method FetchByCapitalName not implemented")
}
func (UnimplementedWeatherServer) mustEmbedUnimplementedWeatherServer() {}

// UnsafeWeatherServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to WeatherServer will
// result in compilation errors.
type UnsafeWeatherServer interface {
	mustEmbedUnimplementedWeatherServer()
}

func RegisterWeatherServer(s grpc.ServiceRegistrar, srv WeatherServer) {
	s.RegisterService(&Weather_ServiceDesc, srv)
}

func _Weather_Update_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(UpdateCapitalRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(WeatherServer).Update(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Weather_Update_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(WeatherServer).Update(ctx, req.(*UpdateCapitalRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Weather_FetchByCapitalName_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FetchByCapitalNameRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(WeatherServer).FetchByCapitalName(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Weather_FetchByCapitalName_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(WeatherServer).FetchByCapitalName(ctx, req.(*FetchByCapitalNameRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Weather_ServiceDesc is the grpc.ServiceDesc for Weather service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Weather_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "Weather",
	HandlerType: (*WeatherServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Update",
			Handler:    _Weather_Update_Handler,
		},
		{
			MethodName: "FetchByCapitalName",
			Handler:    _Weather_FetchByCapitalName_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "weather.proto",
}
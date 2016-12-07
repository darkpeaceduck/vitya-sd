from grpc.tools import protoc

protoc.main(
    (
    '',
    '-I./protos',
    '--python_out=python/chat/',
    '--grpc_python_out=python/chat/',
    './protos/grpc_serv.proto',
    )
)
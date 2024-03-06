import sqlite3
from concurrent import futures
import grpc
import configuracion_pb2
import configuracion_pb2_grpc

class FileServiceServicer(configuracion_pb2_grpc.FileServiceServicer):
    def Upload(self, request, context):
        message = "El archivo fue cargado con éxito"
        print(message)
        return configuracion_pb2.UploadResponse(message=message)

    def Download(self, request, context):
        message = "El archivo fue descargado con éxito"
        print(message)
        file = configuracion_pb2.File(content=message)
        return configuracion_pb2.DownloadResponse(file=file)

def serve():
    print("Corriendo en el puerto 3000")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    configuracion_pb2_grpc.add_FileServiceServicer_to_server(FileServiceServicer(), server)
    server.add_insecure_port('[::]:3000')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

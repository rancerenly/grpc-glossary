import grpc
from concurrent import futures
import time

import glossary_pb2
import glossary_pb2_grpc

terms_db = {}

class GlossaryServiceServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def AddTerm(self, request, context):
        if request.keyword in terms_db:
            return glossary_pb2.Response(message="Термин уже существует")
        terms_db[request.keyword] = request.description
        return glossary_pb2.Response(message="Термин успешно добавлен")

    def GetTerm(self, request, context):
        term = terms_db.get(request.keyword)
        if term is None:
            return glossary_pb2.Term(keyword=request.keyword, description="Термин не найден")
        return glossary_pb2.Term(keyword=request.keyword, description=term)

    def GetTerms(self, request, context):
        terms_list = [glossary_pb2.Term(keyword=key, description=value) for key, value in terms_db.items()]
        return glossary_pb2.TermsList(terms=terms_list)

    def UpdateTerm(self, request, context):
        if request.keyword not in terms_db:
            return glossary_pb2.Response(message="Термин не найден")
        terms_db[request.keyword] = request.description
        return glossary_pb2.Response(message="Термин успешно обновлен")

    def DeleteTerm(self, request, context):
        if request.keyword not in terms_db:
            return glossary_pb2.Response(message="Термин не найден")
        del terms_db[request.keyword]
        return glossary_pb2.Response(message="Термин успешно удален")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started at port 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)  # 24 hours
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

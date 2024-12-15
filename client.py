import grpc
import glossary_pb2
import glossary_pb2_grpc

def run():
    channel = grpc.insecure_channel('glossary-server:50051')
    stub = glossary_pb2_grpc.GlossaryServiceStub(channel)

    response = stub.AddTerm(glossary_pb2.Term(keyword="Асинхронный рендеринг", description="Рендеринг, который не блокирует основной поток выполнения приложения"))
    print("Добавление термина:", response.message)

    response = stub.GetTerm(glossary_pb2.KeywordRequest(keyword="Асинхронный рендеринг"))
    print("Получение термина:", response.keyword, response.description)

    response = stub.GetTerms(glossary_pb2.Empty())
    for term in response.terms:
        print(f"Получение всех терминов: {term.keyword} - {term.description}")

    response = stub.UpdateTerm(glossary_pb2.Term(keyword="Асинхронный рендеринг", description="Рендеринг, при котором части интерфейса обновляются асинхронно"))
    print("Обновление термина:", response.message)

    response = stub.DeleteTerm(glossary_pb2.KeywordRequest(keyword="Асинхронный рендеринг"))
    print("Удаление термина:", response.message)

if __name__ == '__main__':
    run()

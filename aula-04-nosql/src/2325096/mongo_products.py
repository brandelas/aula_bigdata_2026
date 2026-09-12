"""
Lab - Aula 04: Modelos e Implementações NoSQL (MongoDB)

Complete as funções abaixo utilizando a API do pymongo (ou mongomock).
"""


def insert_products(collection, products: list[dict]) -> int:
    """
    Insere uma lista de documentos de produtos na coleção.

    :param collection: Coleção MongoDB (pymongo / mongomock).
    :param products: Lista de dicionários representando produtos.
    :return: Quantidade de documentos inseridos (int).
    """
    if not products:
        return 0
    result = collection.insert_many(products)
    return len(result.inserted_ids)


def find_by_category(collection, category: str) -> list[dict]:
    """
    Busca todos os produtos de uma determinada categoria.
    Requisitos:
    - Retornar ordenado por 'price' em ordem crescente (do menor para o maior).
    - Ocultar o campo '_id' do MongoDB nos dicionários retornados.
    """
    cursor = collection.find({"category": category}, {"_id": 0}).sort("price", 1)
    return list(cursor)


def average_price_by_category(collection) -> dict:
    """
    Calcula o preço médio dos produtos para cada categoria usando o pipeline de agregação do MongoDB.

    Retorno esperado: Um dicionário no formato:
    {"eletronicos": 1000.0, "livros": 50.0}
    """
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "avg_price": {"$avg": "$price"}
            }
        }
    ]
    raw_results = collection.aggregate(pipeline)
    return {doc["_id"]: doc["avg_price"] for doc in raw_results}


def increment_stock(collection, product_id: str, quantity: int) -> int | None:
    """
    Incrementa (ou decrementa) o campo 'stock' de um produto identificado por 'product_id'.
    Usa o operador atômico $inc.

    :param collection: Coleção MongoDB.
    :param product_id: ID do produto (campo 'product_id').
    :param quantity: Quantidade a somar no estoque (pode ser negativa para decremento).
    :return: Novo valor do campo 'stock' (int) ou None se o produto não for encontrado.
    """
    updated_doc = collection.find_one_and_update(
        {"product_id": product_id},
        {"$inc": {"stock": quantity}},
        return_document=True
    )
    if updated_doc is not None:
        return updated_doc.get("stock")
    return None
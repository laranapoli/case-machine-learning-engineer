from mongomock.mongo_client import MongoClient


class InMemoryDatabase:
    _instance = None  # armazena a instância única do banco de dados
    # Implementa o padrão Singleton
    def __new__(cls) -> MongoClient:
        if cls._instance is None:
            client = MongoClient()
            cls._instance = client.get_database('memory_db')
        return cls._instance

    def get_collection(self, collection_name):
        """
        Retorna uma coleção do banco de dados em memória.

        Args:
            collection_name (str): Nome da coleção.

        Returns:
            Collection: A coleção correspondente no banco de dados.
        """
        # new cria e retorna nova instância da classe
        # Garantir instância única: Singleton
        return self.__new__(InMemoryDatabase)[collection_name]

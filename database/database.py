from pymongo import MongoClient
import os

class Database:
    def __init__(self):
        self.client = MongoClient(os.environ["DATABASE_URL"])
        self.db = self.client['trading']
        self.max_huck_size = 16 * 1024 * 1024
        
    def insert_one(self, data, target_table):
        self[target_table].insert_one(data)
    
    def bulk_insert(self, data, targetTable):
        print("data testing", data)
        chunks = []
        current_chunk = []
        current_chunk_size = 0
        for document in data:
            document_size = len(str(document))
            if current_chunk_size + document_size < self.max_huck_size:
                current_chunk.append(document)
                current_chunk_size += document_size
            else:
                chunks.append(current_chunk)
                current_chunk = [document]
                current_chunk_size = document_size
                
        if current_chunk:
            chunks.append(current_chunk)
            
        try:
            total_inserted = 0
            for chunk in chunks:
                result = self.db[targetTable].insert_many(chunk)
                total_inserted += len(result.inserted_ids)
            print(f"Inserted {total_inserted} documents")
        
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def insert_one(self, data, target_table):
        inserted_data = self.db[target_table].insert_one(data)
        print("Inserted Data ID:", inserted_data.inserted_id)


    def find_all(self, target_table, query, projection,):
        return self.db[target_table].find(query, projection)
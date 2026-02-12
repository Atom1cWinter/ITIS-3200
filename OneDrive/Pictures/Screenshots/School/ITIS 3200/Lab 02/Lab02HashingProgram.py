import hashlib
import os
import json

class fileHasher:
    "Handles hasing of file content"
    @staticmethod
    def hash_file(filepath):
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except (PermissionError, FileNotFoundError):
            return None

class HashRepository:
    "Handles data persistence as JSON"
    @staticmethod
    def save_table(data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_table(filename):
        if not os.path.exists(filename):
            return {}
        with open(filename, 'r') as file:
            return json.load(file)

class HashManager:
    "Organizes directory traversal and validation"
    def __init__(self, hasher: FileHasher, repo:HashRepository):
        self.hasher = hasher
        self.repo = repo

    def generate_new_table(self, directory_path):
        hash_table = {}
        for root, _, files in os.walk(directory_path):
            for names in files:
                filepath = os.path.join(root, names)
                file_hash = self.hasher.hash_file(filepath)
                if file_hash:
                    hash_table[filepath] = file_hash
        
        self.repo.save_table(hash_table, "hash_table.json")
        print ("Hash table generated to hash_table.json")

        def validate_hashes(self, directory_path):
            stored_hashes = self.repo.load_table("hash_table.json")
            current_files = set()

            for root, _, files in os.walk(directory_path):
                for names in files:
                    filepath = os.path.join(root, names)
                    current_files.add(filepath)
                    current_hash = self.hasher.hash_file(filepath)

                if filepath not in stored_hashes:
                    print(f"NEW FILE: {filepath}")
                elif current_hash == stored_hashes[filepath]:
                    print(f"VALID: {filepath}")
                else:
                    print(f"INVALID (Modified): {filepath}")
            
            for stored_path in stored_hashes:
                if stored_path not in current_files:
                    print(f"DELETED: {stored_path}")

def main():
    manager = HashManager(FileHasher(), HashRepository())
    
    print("1. Generate New Hash Table")
    print("2. Verify Hashes")
    choice = input("Select an option: ")
    
    path = input("Enter the directory path (e.g., ./Docs/3200Notes): ")

    if choice == '1':
        manager.generate_new_table(path)
    elif choice == '2':
        manager.validate_hashes(path)
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
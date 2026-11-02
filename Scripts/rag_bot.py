import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

# ==========================================
# 1. KONFIGURATION (Pfade & Modelle)
# ==========================================
# Trage hier den Pfad zu deinem Obsidian-Vault ein:
OBSIDIAN_VAULT_PATH = r"C:\Users\chris\Documents\AI Überblick\Obsidian\KI_Knowledge_Base"
PERSIST_DIR = "./chroma_db"

# ==========================================
# 2. SETUP: LLM & EMBEDDINGS (100% LOKAL)
# ==========================================
print("🔄 Initialisiere lokale Ollama-Modelle...")
llm = Ollama(model="qwen2.5:3b", request_timeout=300.0)
embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# ==========================================
# 3. CHUNKING & INDEXIERUNG
# ==========================================
def build_or_load_index():
    # Persistenten Vektor-Speicher (ChromaDB) initialisieren
    db = chromadb.PersistentClient(path=PERSIST_DIR)
    chroma_collection = db.get_or_create_collection("obsidian_notes")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Prüfen, ob bereits Daten in ChromaDB liegen
    if chroma_collection.count() > 0:
        print("💾 Vorhandener Index aus ChromaDB geladen!")
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embed_model
        )
    else:
        print("📂 Lade Markdown-Notizen aus dem Obsidian Vault...")
        reader = SimpleDirectoryReader(
            input_dir=OBSIDIAN_VAULT_PATH,
            recursive=True,
            required_exts=[".md"]
        )
        documents = reader.load_data()
        print(f"📄 {len(documents)} Dokumente gefunden.")

        # Chunking: Dokumente in sinnvolle Abschnitte teilen (512 Token, 50 Overlap)
        text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

        print("⚡ Generiere Vektor-Embeddings und erstelle Index...")
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            embed_model=embed_model,
            transformations=[text_splitter]
        )
        print("✅ Index erfolgreich erstellt und gespeichert!")

    return index

# ==========================================
# 4. CHAT-SCHLEIFE UND QUELLENANGABE
# ==========================================
def start_chat():
    index = build_or_load_index()
    
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=3  # Holt die 3 relevantesten Text-Häppchen
    )

    print("\n" + "="*50)
    print("🤖 Obsidian RAG-Assistent bereit! (Tippe 'exit' zum Beenden)")
    print("="*50 + "\n")

    while True:
        user_query = input("Deine Frage: ")
        if user_query.lower() in ["exit", "quit", "q"]:
            break

        if not user_query.strip():
            continue

        print("\n🔍 Suche in deinen Notizen und generiere Antwort...")
        response = query_engine.query(user_query)

        print("\n--- Antwort ---")
        print(response.response)

        print("\n📚 Verwendete Quellen:")
        sources_found = set()
        for node in response.source_nodes:
            file_path = node.metadata.get("file_path", "Unbekannt")
            file_name = os.path.basename(file_path)
            sources_found.add(file_name)

        for src in sources_found:
            print(f"  • {src}")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    start_chat()
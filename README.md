# 💬 Lokaler Obsidian-RAG-Chatbot (100% Privacy-First Wissensassistent)

> Entwicklung eines lokalen RAG-Chatbots (Retrieval-Augmented Generation) zur datenschutzkonformen Abfrage des eigenen Obsidian-Wissensarchivs ohne Cloud-Anbindung.

---

## 💡 Hinweis zur Entwicklung (AI-Driven Architecture & Development)
*Transparenz-Hinweis:* Dieses Projekt wurde von mir als Solution Architect und Product Owner konzipiert und umgesetzt, wobei ich **Modern AI-Coding-Tools als High-Performance-Entwicklungspartner** genutzt habe. Mein Fokus lag dabei voll und ganz auf Systemarchitektur, Datenfluss, der lokalen RAG-Pipeline (LlamaIndex, ChromaDB, Ollama), Sicherheits- und Datenschutz-Aspekten sowie dem sauberen Setup. Das Projekt demonstriert mustergültig, wie man als moderner Builder und Architekt KI-Kollaboration einsetzt, um datenschutzkonforme, lokale KI-Applikationen auf Enterprise-Niveau umzusetzen.

---

## 🚀 Executive Summary

* **Herausforderung:** Die effiziente und semantische Durchsuchung eines umfangreichen, lokalen Obsidian-Wissensarchivs (über 40 Markdown-Notizen), ohne sensible Notizen oder Daten an Cloud-Dienste (wie OpenAI oder Anthropic) zu übergeben.
* **Lösung:** Entwicklung einer komplett lokalen RAG-Pipeline in Python. Das System indiziert den Obsidian-Vault, konvertiert Notizen in Vektoren und ermöglicht präzise Fragerunden mit exakter Quellenangabe (Dateinamen).
* **Kern-Ergebnis:** Ein blitzschneller, offline-fähiger Chatbot mit lokal ausgeführten Ollama-Modellen, persistentem Vetherspeicher (ChromaDB) und absoluter Datensouveränität (Privacy-First).

---

## 🛠️ Tech Stack & Architecture

* **Framework:** LlamaIndex (spezialisiert auf Data-Centric LLM-Applikationen und sauberes Markdown-Parsing).
* **Embedding & LLM Layer:** Ollama (lokale Ausführung von `nomic-embed-text` für Vektoren und `qwen2.5:3b` für die Antwortgenerierung).
* **Vector Database:** ChromaDB (lokale, persistente In-Memory/Dateisystem-Datenbank über `./chroma_db`).
* **Laufzeitumgebung:** Python 3.11 in einer isolierten virtuellen Umgebung (`venv`) auf Windows.

---

## ⚙️ Umsetzung & Pipeline-Design

1. **Ingestion & Parsing:** Einlesen von Markdown-Notizen aus dem Obsidian-Vault via `SimpleDirectoryReader` inklusive automatischer Metadaten-Zuordnung (`file_path`).
2. **Chunking & Transformation:** Aufteilung der Notizen über den `SentenceSplitter` (Chunk-Größe: 512 Token, Overlap: 50 Token), um semantische Brüche an Dokumentengrenzen zu verhindern.
3. **Persistente Indexierung:** Generierung von Embeddings und Speicherung in der lokalen ChromaDB. Dank persistenter Ablage werden Folgestarts in Bruchteilen einer Sekunde geladen.
4. **Retrieval & Generation (Query Engine):** Bei einer Anfrage werden die 3 relevantesten Text-Chunks (`similarity_top_k=3`) ermittelt, dem lokalen LLM als Kontext übergeben und mit Verweis auf die Quelldatei ausgegeben.

---

## 🖼️ Terminal Execution & Live-Ausführung

![Terminal Execution Output](Pictures/rag-terminal-execution-output.png)

---

## 🎯 Key Learnings & Architecture Insights

1. **Python-Versionen & C++ Dependencies:** Moderne AI-Bibliotheken (wie ChromaDB, `hnswlib` und `numpy`) setzen auf tiefe Kompilierungen. Die Verwendung von Python 3.11 anstelle brandneuer Python-Releases verhindert Build-Fehler (`metadata-generation-failed`) und garantiert Stabilität.
2. **Modulare Paketstruktur:** LlamaIndex hat Vektor-Store-Integrationen ausgelagert. Korrekte Paketbezeichnungen (z. B. `llama-index-vector-stores-chroma`) sind essenziell für fehlerfreie Importe.
3. **Ground Truth & Traceability:** Die Verknüpfung von `node.metadata` mit dem Dateinamen stellt sicher, dass generierte Antworten stets überprüfbar und frei von Halluzinationen über das eigene Notizarchiv sind.

---

## 📂 Repository-Structure

```text
├── Scripts/
│   └── rag_bot.py                 # Hauptskript für den interaktiven RAG-Chatbot
├── Pictures/
│   └── rag-terminal-execution-output.png # Terminal-Ausführungs-Asset
├── chroma_db/                     # Persistenter lokaler Vektorspeicher-Index (local)
├── requirements.txt               # Python-Abhängigkeiten (LlamaIndex, ChromaDB, Ollama etc.)
└── README.md                      # Projektdokumentation

(Hinweis: Der persistente Vektorspeicher chroma_db/ sowie lokale Konfigurationen verbleiben aufgrund der lokalen Dateigröße und Datenschutzaspekte in der lokalen Entwicklungsumgebung und sind über .gitignore vom Public Upload ausgeschlossen).

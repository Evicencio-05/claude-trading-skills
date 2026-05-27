# Thesis Manager

Run:     streamlit run tools/thesis-manager/app.py
Purpose: Thesis input and position review for trader-memory-core
Data:    Reads state/theses/ and state/pending_ingest.json
Writes:  Calls thesis_store API (never directly edits YAML files)

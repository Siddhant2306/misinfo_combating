# Hackathon Problem statement

flowchart TD
    A[User Input<br/>(Claim / Article)] --> B[Fetch Relevant Data<br/>(News APIs, Search Engines, Fact-check DBs)]
    B --> C[Preprocess & Extract Key Facts]
    C --> D[Evidence Scoring<br/>(LLM checks Supports/Refutes)]
    D --> E[Verdict Engine<br/>(Aggregate Scores & Confidence)]
    E --> F[Return Verdict to UI<br/>(True / False / Inconclusive)]

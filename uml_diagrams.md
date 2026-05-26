# RealityCheck AI – UML Diagram Package

This document contains professional, standard UML diagrams for the **RealityCheck AI – Fake News & Misinformation Analyzer** web application. The diagrams map to clean software engineering notations, showcasing structural models, behavioral workflows, and modular deployment topologies.

---

## 1. Use Case Diagram

The Use Case Diagram displays structural boundaries and interactions between the actor (`User`) and the functional capabilities of the system.

```mermaid
graph LR
    %% Definition of Actor
    subgraph SystemBoundary [" RealityCheck AI Application Boundary "]
        uc1(["Enter Headline, Text, or URL"])
        uc2(["Analyze Content"])
        uc3(["View Credibility Score (0-100)"])
        uc4(["View Bias & Slant Spectrum"])
        uc5(["View Highlighted Suspicious Words"])
        uc6(["View Verification Report Explanations"])
    end

    ActorUser["👤 User"]

    %% Connect User to all Use Cases with straight UML association lines
    ActorUser --- uc1
    ActorUser --- uc2
    ActorUser --- uc3
    ActorUser --- uc4
    ActorUser --- uc5
    ActorUser --- uc6

    %% Styling & Aesthetics
    style ActorUser fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#e0e7ff
    style SystemBoundary fill:rgba(15,23,42,0.4),stroke:#334155,stroke-width:2px,color:#94a3b8
    
    style uc1 fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc
    style uc2 fill:#0f172a,stroke:#6366f1,stroke-width:2px,color:#f8fafc
    style uc3 fill:#0f172a,stroke:#34d399,stroke-width:2px,color:#f8fafc
    style uc4 fill:#0f172a,stroke:#fbbf24,stroke-width:2px,color:#f8fafc
    style uc5 fill:#0f172a,stroke:#fb7185,stroke-width:2px,color:#f8fafc
    style uc6 fill:#0f172a,stroke:#22d3ee,stroke-width:2px,color:#f8fafc
```

---

## 2. Class Diagram

The Class Diagram presents the static object-oriented architecture of the platform, including attributes, methods, types, and standard UML structural relationships (Associations, Dependencies, and Creations).

```mermaid
classDiagram
    class User {
        +int user_id
        +string input_text
        +submitInput() void
    }

    class APIController {
        +analyzeRequest(AnalyzeRequest payload) AnalyzeResponse
        +returnResponse() dict
    }

    class Analyzer {
        +string text
        +calculateScore(string text, bool is_trusted, bool is_blocked) tuple
        +detectBias(string text) string
        +extractKeywords(string text) list
    }

    class Result {
        +int score
        +float fake_probability
        +string bias
        +list highlights
        +list explanations
        +generateReport() dict
    }

    %% UML Relationships
    User --> APIController : Association
    APIController ..> Analyzer : Dependency
    Analyzer ..> Result : Creates

    %% Custom Class Diagram Theming
    style User fill:#0f172a,stroke:#6366f1,stroke-width:2px,color:#e2e8f0
    style APIController fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#e2e8f0
    style Analyzer fill:#0f172a,stroke:#22d3ee,stroke-width:2px,color:#e2e8f0
    style Result fill:#0f172a,stroke:#34d399,stroke-width:2px,color:#e2e8f0
```

---

## 3. Sequence Diagram

The Sequence Diagram details the time-ordered interactive messaging flow between subsystems when a user triggers content verification.

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 User
    participant Frontend as 🖥️ Frontend UI
    participant API as ⚙️ API (FastAPI)
    participant Analyzer as 🧠 NLP Analyzer Engine
    participant Result as 📊 Result Object

    User->>Frontend: Enters article text / URL & clicks Scan
    activate Frontend
    
    Frontend->>API: POST /analyze (Payload JSON)
    activate API
    note over API: Validates fields & handles scraping (if URL)
    
    API->>Analyzer: analyze_content(text, url)
    activate Analyzer
    
    note over Analyzer: Runs rule-based syntactic models
    Analyzer->>Analyzer: calculate_score()
    Analyzer->>Analyzer: detect_bias()
    Analyzer->>Analyzer: extract_keywords()
    
    Analyzer->>Result: instantiate with scores & offsets
    activate Result
    Result-->>Analyzer: Result object created
    deactivate Result
    
    Analyzer-->>API: returns aggregated Result data
    deactivate Analyzer
    
    API-->>Frontend: returns HTTP 200 (JSON payload response)
    deactivate API
    
    Frontend-->>User: Renders score dials, highlights map, & report
    deactivate Frontend
```

---

## 4. Activity Diagram

The Activity Diagram highlights the behavioral execution flow and logical decision routing branches within the verification workflow.

```mermaid
graph TD
    StartNode([● Start]) --> EnterInput["Enter Text Block or Article URL"]
    EnterInput --> ValidateInput["Validate Fields (Format & Length Check)"]
    ValidateInput --> DecisionValid{"Is Input Valid?"}

    %% Decision branch: NO
    DecisionValid -- "No (Empty or <30 chars)" --> ShowError["Show UI Validation Error Banner"]
    ShowError --> EndNode([● End])

    %% Decision branch: YES
    DecisionValid -- "Yes" --> AnalyzeContent["Analyze Text Patterns & Match Triggers"]
    AnalyzeContent --> GenerateMetrics["Generate Credibility Score & Bias Slants"]
    GenerateMetrics --> RenderUI["Render Animated Gauge & Highlights Map"]
    RenderUI --> EndNode

    %% Styling & Aesthetics
    style StartNode fill:#334155,stroke:#94a3b8,stroke-width:2px,color:#f8fafc
    style EndNode fill:#334155,stroke:#94a3b8,stroke-width:2px,color:#f8fafc
    
    style EnterInput fill:#0f172a,stroke:#6366f1,stroke-width:2px,color:#e2e8f0
    style ValidateInput fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#e2e8f0
    
    style DecisionValid fill:#1e1b4b,stroke:#f59e0b,stroke-width:2px,color:#fef3c7
    
    style ShowError fill:#7f1d1d,stroke:#ef4444,stroke-width:2px,color:#fee2e2
    style AnalyzeContent fill:#0f172a,stroke:#22d3ee,stroke-width:2px,color:#e2e8f0
    style GenerateMetrics fill:#0f172a,stroke:#34d399,stroke-width:2px,color:#e2e8f0
    style RenderUI fill:#0f172a,stroke:#a855f7,stroke-width:2px,color:#e2e8f0
```

---

## 5. Component Diagram

The Component Diagram displays the high-level physical modular building blocks of the platform, showing interfaces and wiring connections.

```mermaid
graph LR
    subgraph ClientSpace [" Client Environment "]
        ComponentUI["🖥️ Frontend UI Component <br> (index.html, styles.css, app.js)"]
    end

    subgraph ServerSpace [" Server Environment (FastAPI App) "]
        ComponentAPI["⚙️ API Controller Component <br> (routes/analyze.py)"]
        ComponentNLP["🧠 NLP Analyzer Component <br> (utils/nlp.py)"]
        ComponentScrape["🕷️ Scraper Service Component <br> (services/scraper.py)"]
        ComponentDB[("🗃️ Reputation Database <br> (whitelists/blacklists)")]
    end

    %% Wiring Connections
    ComponentUI -->|"REST API (HTTP POST /analyze)"| ComponentAPI
    ComponentAPI -->|"Calls logic"| ComponentNLP
    ComponentAPI -->|"Invokes crawl"| ComponentScrape
    ComponentNLP -->|"Queries domains"| ComponentDB
    ComponentScrape -->|"Checks reliability"| ComponentDB

    %% Styling & Aesthetics
    style ClientSpace fill:rgba(30,41,59,0.2),stroke:#475569,stroke-width:2px,color:#94a3b8
    style ServerSpace fill:rgba(30,41,59,0.4),stroke:#475569,stroke-width:2px,color:#94a3b8
    
    style ComponentUI fill:#0f172a,stroke:#6366f1,stroke-width:2px,color:#f8fafc
    style ComponentAPI fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc
    style ComponentNLP fill:#0f172a,stroke:#22d3ee,stroke-width:2px,color:#f8fafc
    style ComponentScrape fill:#0f172a,stroke:#fb7185,stroke-width:2px,color:#f8fafc
    style ComponentDB fill:#1e1b4b,stroke:#34d399,stroke-width:2px,color:#f8fafc
```

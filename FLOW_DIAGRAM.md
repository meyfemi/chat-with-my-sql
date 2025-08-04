# Chat with MySQL - Application Flow Diagram

## Main Application Flow

```mermaid
flowchart LR
    A[User Question] --> B[AI Processing]
    B --> C[SQL Generation]
    C --> D[Database Query]
    D --> E[Results]
    E --> F[Natural Response]
    F --> G[Visualization]
    
    subgraph "User Interface"
        A
        G
    end
    
    subgraph "AI Engine"
        B
        C
        F
    end
    
    subgraph "Database"
        D
        E
    end
    
    style A fill:#e1f5fe
    style G fill:#c8e6c9
    style B fill:#fff3e0
    style C fill:#fff3e0
    style F fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#f3e5f5
```

## Database Connection Flow

```mermaid
flowchart TD
    A[User Clicks Connect] --> B[Validate Connection Parameters]
    B --> C{Parameters Valid?}
    C -->|No| D[Show Error: Invalid Parameters]
    C -->|Yes| E[Create DatabaseManager Instance]
    
    E --> F[Test Database Connection]
    F --> G{Connection Successful?}
    G -->|No| H[Show Error: Connection Failed]
    G -->|Yes| I[Initialize ChatManager with AI]
    
    I --> J[Load Database Schema]
    J --> K[Cache Schema for Performance]
    K --> L[Show Success: Connected]
    L --> M[Enable Chat Interface]
    
    style A fill:#e1f5fe
    style M fill:#c8e6c9
    style H fill:#ffcdd2
    style D fill:#ffcdd2
```

## AI Processing Flow

```mermaid
flowchart LR
    A[User Question] --> B[AI Analysis]
    B --> C[SQL Generation]
    C --> D[Database Query]
    D --> E[Results Processing]
    E --> F[Natural Response]
    F --> G[Visualization Suggestion]
    
    subgraph "Gemini AI"
        B
        C
        F
        G
    end
    
    subgraph "Database"
        D
        E
    end
    
    style A fill:#e1f5fe
    style G fill:#c8e6c9
    style B fill:#fff3e0
    style C fill:#fff3e0
    style F fill:#fff3e0
    style G fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#f3e5f5
```

## Error Handling Flow

```mermaid
flowchart TD
    A[Process Request] --> B{Database Connection?}
    B -->|No| C[Show Connection Error]
    B -->|Yes| D{Valid SQL Generated?}
    
    D -->|No| E[Show SQL Generation Error]
    D -->|Yes| F{Query Execution Success?}
    
    F -->|No| G[Show Database Error]
    F -->|Yes| H{Response Generation Success?}
    
    H -->|No| I[Show AI Response Error]
    H -->|Yes| J{Visualization Creation Success?}
    
    J -->|No| K[Show Visualization Error]
    J -->|Yes| L[Display Complete Response]
    
    C --> M[Log Error + Show User Message]
    E --> M
    G --> M
    I --> M
    K --> M
    
    style A fill:#e1f5fe
    style L fill:#c8e6c9
    style M fill:#ffcdd2
```

## Component Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Streamlit UI]
        B[Chat Interface]
        C[Database Connection Form]
        D[Visualization Display]
    end
    
    subgraph "Application Layer"
        E[ChatApp]
        F[ChatManager]
        G[DatabaseManager]
        H[VisualizationManager]
    end
    
    subgraph "AI Layer"
        I[Gemini AI]
        J[SQL Generation]
        K[Response Generation]
    end
    
    subgraph "Data Layer"
        L[MySQL Database]
        M[Connection Pool]
        N[Schema Cache]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    E --> G
    E --> H
    
    F --> I
    F --> J
    F --> K
    
    G --> L
    G --> M
    G --> N
    
    H --> D
    
    style A fill:#e3f2fd
    style E fill:#f3e5f5
    style I fill:#fff3e0
    style L fill:#e8f5e8
```

## Data Flow Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit UI
    participant C as ChatManager
    participant AI as Gemini AI
    participant DB as MySQL Database
    participant V as Visualization
    
    U->>S: Type Question
    S->>S: Add to Chat History
    S->>S: Show Loading Spinner
    
    S->>C: get_response(question, history)
    C->>C: Format Chat History
    C->>AI: Generate SQL Prompt
    AI->>C: Return SQL Query
    
    C->>DB: Execute SQL Query
    DB->>C: Return Query Results
    
    C->>AI: Generate Response Prompt
    AI->>C: Return Natural Response + Viz Tags
    
    alt Has Visualization
        C->>V: Create Chart
        V->>C: Return Chart Data
    end
    
    C->>S: Return Response + Viz Data
    S->>S: Update Chat History
    S->>S: Display Response
    S->>S: Show SQL Query
    S->>S: Display Visualization
    
    S->>U: Show Complete Response
```

## Performance Optimization Flow

```mermaid
flowchart LR
    A[User Request] --> B{Schema Cached?}
    B -->|No| C[Load Schema from DB]
    B -->|Yes| D[Use Cached Schema]
    
    C --> E[Cache Schema for 1 Hour]
    D --> F[Generate SQL Prompt]
    E --> F
    
    F --> G[AI Processing]
    G --> H{Connection Pool Available?}
    H -->|No| I[Wait for Connection]
    H -->|Yes| J[Execute Query]
    
    I --> J
    J --> K[Return Results]
    K --> L[Release Connection to Pool]
    
    style A fill:#e1f5fe
    style L fill:#c8e6c9
    style D fill:#e8f5e8
    style J fill:#f3e5f5
```

---

## Diagram Usage Instructions

These Mermaid diagrams can be:

1. **Embedded in Medium** using Mermaid support
2. **Converted to images** using online Mermaid editors
3. **Used in documentation** for technical explanations
4. **Shared in presentations** to explain the architecture

### Key Color Coding:
- 🔵 **Blue**: User interactions and inputs
- 🟢 **Green**: Successful completions and data sources
- 🟡 **Orange**: AI processing steps
- 🟣 **Purple**: Database operations
- 🔴 **Red**: Error handling paths 
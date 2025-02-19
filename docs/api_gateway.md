erDiagram
    REQUESTS {
        int id PK
        string endpoint
        string method
        string request_body
        datetime timestamp
    }
    
    LOGS {
        int id PK
        string level
        string message
        datetime created_at
    }
    
    ROUTES {
        int id PK
        string path
        string target_service
        string method
    }

    REQUESTS ||--o{ LOGS : logs
    ROUTES ||--o{ REQUESTS : handles


erDiagram
    USERS {
        int id PK
        string username
        string email
        string password_hash
        string role
        datetime created_at
    }

    SESSIONS {
        int id PK
        int user_id FK
        string token
        datetime expires_at
    }

    ROLES {
        int id PK
        string role_name
        string permissions
    }

    REQUESTS {
        int id PK
        int user_id FK
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

    POSTS {
        int id PK
        int user_id FK
        string content
        datetime created_at
        int likes
        int comments_count
    }

    COMMENTS {
        int id PK
        int post_id FK
        int user_id FK
        string text
        datetime created_at
    }

    PROMOCODES {
        int id PK
        string code
        int discount
        datetime valid_until
    }

    STATISTICS {
        int id PK
        int user_id FK
        int post_id FK
        int comment_id FK
        int views
        int likes
        int comments
        datetime collected_at
    }

    EVENTS {
        int id PK
        int user_id FK
        string event_type
        string metadata
        datetime created_at
    }

    DASHBOARDS {
        int id PK
        int user_id FK
        string config
        datetime last_updated
    }

    KAFKA_MESSAGES {
        int id PK
        string topic
        string payload
        datetime created_at
    }

    USERS ||--o{ SESSIONS : has
    ROLES ||--o{ USERS : assigns
    USERS ||--o{ POSTS : writes
    POSTS ||--o{ COMMENTS : receives
    REQUESTS ||--o{ LOGS : logs
    ROUTES ||--o{ REQUESTS : handles
    USERS ||--o{ STATISTICS : tracks
    EVENTS ||--o{ STATISTICS : generates
    DASHBOARDS ||--o{ USERS : owned_by
    STATISTICS ||--o{ POSTS : analyzes
    STATISTICS ||--o{ COMMENTS : analyzes
    REQUESTS ||--o{ USERS : made_by
    EVENTS ||--o{ KAFKA_MESSAGES : published_to


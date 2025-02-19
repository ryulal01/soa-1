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

    USERS ||--o{ SESSIONS : has
    ROLES ||--o{ USERS : assigns


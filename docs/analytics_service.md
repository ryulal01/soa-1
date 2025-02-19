erDiagram
    STATISTICS {
        int id PK
        int user_id FK
        int post_id FK
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

    USERS ||--o{ STATISTICS : tracks
    EVENTS ||--o{ STATISTICS : generates


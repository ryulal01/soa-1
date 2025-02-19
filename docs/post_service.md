erDiagram
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

    USERS ||--o{ POSTS : writes
    POSTS ||--o{ COMMENTS : receives


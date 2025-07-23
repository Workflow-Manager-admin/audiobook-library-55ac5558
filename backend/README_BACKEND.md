# Audiobook Backend API

This Flask backend provides RESTful APIs for:
- Browsing the audiobook store
- Handling audiobook purchases
- Retrieving a user's personal library
- Managing audiobook playback progress

## Main Features

**Store Browse:**  
`GET /api/store/` — Returns all available audiobooks.

**Purchase:**  
`POST /api/store/purchase`  
Payload: `{ "user_id": ..., "audiobook_id": ... }`
Buys an audiobook for the user.

**Personal Library:**  
`GET /api/library/<user_id>` — Returns all audiobooks purchased by the user.

**Playback Progress:**  
`GET /api/progress/<user_id>/<audiobook_id>` — Get playback progress  
`PUT /api/progress/<user_id>/<audiobook_id>` — Update playback progress  
Payload: `{ "position_seconds": ... }`

All endpoints use JSON.

## Database

- PostgreSQL database required.
- Connection determined by `DATABASE_URL` environment variable.
- Data models: User, Audiobook, Purchase, PlaybackProgress.

## Setup

1. Ensure PostgreSQL is running and create a database for the app.
2. Set the `DATABASE_URL` environment variable (`export DATABASE_URL=postgresql://username:password@host:port/dbname`).
3. Install dependencies:  
   `pip install -r requirements.txt`
4. Initialize the DB models:
   ```
   from app import app, db
   with app.app_context():
       db.create_all()
   ```
5. Run the backend:
   ```
   python run.py
   ```
6. The API docs will be at `/docs/openapi.json` and Swagger UI at `/docs/`.

## Notes

- User management (registration/auth) is not covered and must be provided or adapted for your use case.
- All data access uses SQLAlchemy ORM.
- Marshmallow schemas handle input/output validation and OpenAPI docs.

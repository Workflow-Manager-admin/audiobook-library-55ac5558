from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# PUBLIC_INTERFACE
class User(db.Model):
    """User model, represents a registered app user."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    purchases = db.relationship("Purchase", back_populates="user")
    playback_progresses = db.relationship("PlaybackProgress", back_populates="user")

# PUBLIC_INTERFACE
class Audiobook(db.Model):
    """Audiobook in the global store."""
    __tablename__ = "audiobooks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cover_url = db.Column(db.String(200))
    audio_url = db.Column(db.String(200))
    duration_seconds = db.Column(db.Integer)
    price = db.Column(db.Float)
    purchases = db.relationship("Purchase", back_populates="audiobook")

# PUBLIC_INTERFACE
class Purchase(db.Model):
    """Records a user's purchase of an audiobook."""
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    audiobook_id = db.Column(db.Integer, db.ForeignKey("audiobooks.id"), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", back_populates="purchases")
    audiobook = db.relationship("Audiobook", back_populates="purchases")

# PUBLIC_INTERFACE
class PlaybackProgress(db.Model):
    """Tracks user's current playback position for a given audiobook."""
    __tablename__ = "playback_progresses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    audiobook_id = db.Column(db.Integer, db.ForeignKey("audiobooks.id"), nullable=False)
    position_seconds = db.Column(db.Integer, nullable=False, default=0)
    last_update = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", back_populates="playback_progresses")
    audiobook = db.relationship("Audiobook")

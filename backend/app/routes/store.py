from flask.views import MethodView
from flask_smorest import Blueprint, abort
from .schemas import AudiobookSchema, LibraryAudiobookSchema, PlaybackProgressSchema, PurchaseRequestSchema, PlaybackProgressRequestSchema, PurchaseResponseSchema
from ..models import db, Audiobook, Purchase, PlaybackProgress
from datetime import datetime

blp = Blueprint(
    "Audiobook Store",
    "audiobook_store",
    url_prefix="/api/store",
    description="Browse and buy audiobooks"
)

# PUBLIC_INTERFACE
@blp.route("/")
class StoreList(MethodView):
    """Audiobook store: browse available audiobooks."""
    @blp.response(200, AudiobookSchema(many=True))
    def get(self):
        """
        Get list of all audiobooks in the store.
        ---
        tags:
          - Store
        """
        audiobooks = Audiobook.query.all()
        return audiobooks

# PUBLIC_INTERFACE
@blp.route("/purchase")
class PurchaseAudiobook(MethodView):
    """Endpoint for purchasing audiobooks."""
    @blp.arguments(PurchaseRequestSchema)
    @blp.response(201, PurchaseResponseSchema)
    def post(self, purchase_data):
        """
        Create a purchase for a user for an audiobook.
        ---
        tags:
          - Purchase
        """
        user_id = purchase_data["user_id"]
        audiobook_id = purchase_data["audiobook_id"]
        # Check if the purchase already exists
        if Purchase.query.filter_by(user_id=user_id, audiobook_id=audiobook_id).first():
            abort(409, message="Audiobook already purchased.")
        purchase = Purchase(
            user_id=user_id,
            audiobook_id=audiobook_id,
            purchase_date=datetime.utcnow(),
        )
        db.session.add(purchase)
        db.session.commit()
        return {"purchase_id": purchase.id, "user_id": user_id, "audiobook_id": audiobook_id}

blp_library = Blueprint(
    "User Library",
    "user_library",
    url_prefix="/api/library",
    description="Access personal library of purchased audiobooks"
)

# PUBLIC_INTERFACE
@blp_library.route("/<int:user_id>")
class UserLibrary(MethodView):
    """View audiobooks purchased by the user."""
    @blp_library.response(200, LibraryAudiobookSchema(many=True))
    def get(self, user_id):
        """
        Get all audiobooks purchased by a user.
        ---
        tags:
          - Library
        """
        purchases = Purchase.query.filter_by(user_id=user_id).all()
        audiobooks = []
        for purchase in purchases:
            audiobook = Audiobook.query.filter_by(id=purchase.audiobook_id).first()
            if audiobook:
                audiobooks.append(audiobook)
        return audiobooks

blp_playback = Blueprint(
    "Playback Progress",
    "playback_progress",
    url_prefix="/api/progress",
    description="Get and update playback positions"
)

# PUBLIC_INTERFACE
@blp_playback.route("/<int:user_id>/<int:audiobook_id>")
class PlaybackProgressView(MethodView):
    """Manage the playback position for a user's audiobook."""
    @blp_playback.response(200, PlaybackProgressSchema)
    def get(self, user_id, audiobook_id):
        """
        Get the playback position for a user's audiobook.
        ---
        tags:
          - Progress
        """
        progress = PlaybackProgress.query.filter_by(user_id=user_id, audiobook_id=audiobook_id).first()
        if not progress:
            abort(404, message="No playback progress found.")
        return progress

    @blp_playback.arguments(PlaybackProgressRequestSchema)
    @blp_playback.response(200, PlaybackProgressSchema)
    def put(self, data, user_id, audiobook_id):
        """
        Update or create playback progress for a user and audiobook.
        ---
        tags:
          - Progress
        """
        position_seconds = data["position_seconds"]
        progress = PlaybackProgress.query.filter_by(user_id=user_id, audiobook_id=audiobook_id).first()
        if progress:
            progress.position_seconds = position_seconds
            progress.last_update = datetime.utcnow()
        else:
            progress = PlaybackProgress(
                user_id=user_id,
                audiobook_id=audiobook_id,
                position_seconds=position_seconds,
                last_update=datetime.utcnow()
            )
            db.session.add(progress)
        db.session.commit()
        return progress


def register_routes(api):
    """Register all blueprints for the API."""
    from .store import blp as store_blp, blp_library, blp_playback
    api.register_blueprint(store_blp)
    api.register_blueprint(blp_library)
    api.register_blueprint(blp_playback)

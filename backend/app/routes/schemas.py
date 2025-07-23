from marshmallow import Schema, fields

# PUBLIC_INTERFACE
class AudiobookSchema(Schema):
    """Schema for Audiobook model."""
    id = fields.Int(dump_only=True, description="Audiobook ID")
    title = fields.Str(required=True, description="Title of the audiobook")
    author = fields.Str(required=True, description="Author")
    description = fields.Str(description="Description")
    cover_url = fields.Str(description="Cover image URL")
    audio_url = fields.Str(description="Audio file URL")
    duration_seconds = fields.Int(description="Duration in seconds")
    price = fields.Float(description="Price of the audiobook")

# PUBLIC_INTERFACE
class PurchaseRequestSchema(Schema):
    """Request schema for making a purchase."""
    user_id = fields.Int(required=True, description="User ID")
    audiobook_id = fields.Int(required=True, description="Audiobook ID")

# PUBLIC_INTERFACE
class PurchaseResponseSchema(Schema):
    """Response schema for a purchase."""
    purchase_id = fields.Int(description="Purchase ID")
    user_id = fields.Int(description="User ID")
    audiobook_id = fields.Int(description="Audiobook ID")

# PUBLIC_INTERFACE
class LibraryAudiobookSchema(AudiobookSchema):
    """Schema for a user's audiobook in their library."""
    pass

# PUBLIC_INTERFACE
class PlaybackProgressRequestSchema(Schema):
    """Request for updating playback progress."""
    position_seconds = fields.Int(required=True, description="Playback position (seconds)")

# PUBLIC_INTERFACE
class PlaybackProgressSchema(Schema):
    """Response for playback progress."""
    id = fields.Int(description="Progress ID")
    user_id = fields.Int(description="User ID")
    audiobook_id = fields.Int(description="Audiobook ID")
    position_seconds = fields.Int(description="Playback position in seconds")
    last_update = fields.DateTime(description="Last updated at")

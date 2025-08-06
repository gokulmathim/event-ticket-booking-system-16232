from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import (
    EventResponseSchema, EventListResponseSchema
)
from app import models

blp = Blueprint(
    "Events", "events", url_prefix="/events",
    description="Event listing endpoints"
)

@blp.route("/")
class EventList(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, EventListResponseSchema)
    def get(self):
        """List all available events."""
        models.seed_demo_data()  # Seed demo data for testing
        events = models.list_events()
        return {"events": [
            {
                "id": e["id"], "title": e["title"], "description": e["description"],
                "datetime": e["datetime"], "venue": e["venue"]
            }
            for e in events
        ]}

@blp.route("/<event_id>")
class EventDetail(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, EventResponseSchema)
    def get(self, event_id):
        """Get details for a specific event."""
        event = models.get_event(event_id)
        if not event:
            abort(404, message="Event not found")
        return {
            "id": event["id"], "title": event["title"], "description": event["description"],
            "datetime": event["datetime"], "venue": event["venue"]
        }

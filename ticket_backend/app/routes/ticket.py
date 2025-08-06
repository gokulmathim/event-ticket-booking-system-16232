from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import TicketResponseSchema, TicketListResponseSchema
from app import models

blp = Blueprint(
    "Tickets", "tickets", url_prefix="/tickets",
    description="Ticket management endpoints"
)

@blp.route("/")
class TicketList(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, TicketListResponseSchema)
    def get(self):
        """List all tickets (for demo; real usage would require auth filter)."""
        return {"tickets": list(models._db["tickets"].values())}

@blp.route("/user/<user_id>")
class UserTickets(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, TicketListResponseSchema)
    def get(self, user_id):
        """List all tickets booked by a user."""
        return {"tickets": models.list_tickets_for_user(user_id)}

@blp.route("/<ticket_id>")
class TicketDetail(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, TicketResponseSchema)
    def get(self, ticket_id):
        """Get ticket details."""
        ticket = models.get_ticket(ticket_id)
        if not ticket:
            abort(404, message="Ticket not found")
        return ticket

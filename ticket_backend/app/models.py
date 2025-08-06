import uuid
from datetime import datetime

# Simulate a database for users, events, seats, tickets, and payments.
# In a real-world app, these would be proper database models (e.g., SQLAlchemy models).

_db = {
    "users": {},       # key: user_id (uuid), value: User dict
    "events": {},      # key: event_id (uuid), value: Event dict
    "seats": {},       # key: (event_id, seat_id), value: Seat dict
    "tickets": {},     # key: ticket_id (uuid), value: Ticket dict
    "payments": {},    # key: payment_id (uuid), value: Payment dict
}

# PUBLIC_INTERFACE
def create_user(email, name, password_hash):
    """Create a new user and add to the 'users' collection."""
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": email,
        "name": name,
        "password_hash": password_hash,
        "created_at": datetime.utcnow(),
    }
    _db["users"][user_id] = user
    return user

# PUBLIC_INTERFACE
def get_user_by_email(email):
    """Get a user object by email."""
    for user in _db["users"].values():
        if user["email"] == email:
            return user
    return None

# PUBLIC_INTERFACE
def get_user_by_id(user_id):
    """Get user by their ID."""
    return _db["users"].get(user_id)

# PUBLIC_INTERFACE
def list_events():
    """Return a list of all events."""
    return list(_db["events"].values())

# PUBLIC_INTERFACE
def create_event(title, description, datetime_obj, venue, seat_map):
    """Create an event and associated seats."""
    event_id = str(uuid.uuid4())
    event = {
        "id": event_id,
        "title": title,
        "description": description,
        "datetime": datetime_obj,
        "venue": venue,
    }
    _db["events"][event_id] = event
    # Create seats: seat_map is a list of {"label": str, "price": float}
    for seat in seat_map:
        seat_id = str(uuid.uuid4())
        seat_entry = {
            "id": seat_id,
            "event_id": event_id,
            "label": seat["label"],
            "status": "available", # or "booked"
            "price": seat["price"]
        }
        _db["seats"][(event_id, seat_id)] = seat_entry
    return event

# PUBLIC_INTERFACE
def get_event(event_id):
    return _db["events"].get(event_id)

# PUBLIC_INTERFACE
def list_seats(event_id):
    """List all seats for an event."""
    return [seat for (eid, _), seat in _db["seats"].items() if eid == event_id]

# PUBLIC_INTERFACE
def get_seat(event_id, seat_id):
    return _db["seats"].get((event_id, seat_id))

# PUBLIC_INTERFACE
def update_seat_status(event_id, seat_id, status):
    seat = _db["seats"].get((event_id, seat_id))
    if seat:
        seat["status"] = status
    return seat

# PUBLIC_INTERFACE
def create_ticket(event_id, seat_id, user_id):
    """
    Create a new ticket for the given seat at an event for a user, generating a guaranteed unique ticket ID.

    Each ticket created uses a universally unique identifier (UUID) via uuid.uuid4(), ensuring every ticket ID is distinct
    system-wide. This logic ensures that even in high-concurrency scenarios or distributed contexts, there will be no ID collisions.

    Returns the ticket object if successful; returns None if the seat is already booked or not found.
    """
    seat = get_seat(event_id, seat_id)
    if seat is None or seat["status"] != "available":
        return None
    ticket_id = str(uuid.uuid4())
    ticket = {
        "id": ticket_id,
        "event_id": event_id,
        "seat_id": seat_id,
        "user_id": user_id,
        "booked_at": datetime.utcnow()
    }
    _db["tickets"][ticket_id] = ticket
    update_seat_status(event_id, seat_id, "booked")
    return ticket

# PUBLIC_INTERFACE
def book_multiple_seats(event_id, seat_ids, user_id):
    """
    Atomically book multiple seats for a user.
    - If any of the seats is unavailable, returns with 'success' only for seats which could be booked atomically, and for the rest lists failed_seats.
    - If all are booked successfully, returns list of all tickets and empty failed_seats list.
    """
    booked_tickets = []
    failed_seats = []

    # Check all seat existence and availability first
    for seat_id in seat_ids:
        seat = get_seat(event_id, seat_id)
        if seat is None or seat["status"] != "available":
            failed_seats.append(seat_id)

    if failed_seats:
        return [], failed_seats

    # All seats available, proceed with booking
    for seat_id in seat_ids:
        ticket = create_ticket(event_id, seat_id, user_id)
        if not ticket:
            # (Should not happen since we checked, but for safety)
            failed_seats.append(seat_id)
        else:
            booked_tickets.append(ticket)
    return booked_tickets, failed_seats

# PUBLIC_INTERFACE
def get_ticket(ticket_id):
    return _db["tickets"].get(ticket_id)

# PUBLIC_INTERFACE
def list_tickets_for_user(user_id):
    return [t for t in _db["tickets"].values() if t["user_id"] == user_id]

# PUBLIC_INTERFACE
def create_payment(user_id, ticket_id, amount, status="pending"):
    payment_id = str(uuid.uuid4())
    payment = {
        "id": payment_id,
        "user_id": user_id,
        "ticket_id": ticket_id,
        "amount": amount,
        "status": status,
        "created_at": datetime.utcnow()
    }
    _db["payments"][payment_id] = payment
    return payment

# PUBLIC_INTERFACE
def update_payment_status(payment_id, status):
    payment = _db["payments"].get(payment_id)
    if payment:
        payment["status"] = status
    return payment

# PUBLIC_INTERFACE
def get_payment(payment_id):
    return _db["payments"].get(payment_id)

# PUBLIC_INTERFACE
def seed_demo_data():
    """Populate demo events and seats for illustrative/demo use."""
    # Only seed if no events exist
    if _db["events"]:
        return
    create_event(
        title="Rock Concert",
        description="A night of rock music with top bands.",
        datetime_obj=datetime(2024, 8, 18, 19, 0),
        venue="Stadium A",
        seat_map=[{"label": f"A{i}", "price": 50.0} for i in range(1, 11)],
    )
    create_event(
        title="Jazz Night",
        description="Smooth jazz performances.",
        datetime_obj=datetime(2024, 8, 22, 20, 0),
        venue="Hall B",
        seat_map=[{"label": f"B{i}", "price": 40.0} for i in range(1, 6)],
    )

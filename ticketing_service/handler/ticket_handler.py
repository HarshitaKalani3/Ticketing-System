from ..dao.models import Ticket, Comment
import uuid

ALLOWED_CREATE_FIELDS = {'title', 'description', 'priority'}

class TicketHandler:
    @staticmethod
    def create_ticket(data, user):
        safe_data = {k: v for k, v in data.items() if k in ALLOWED_CREATE_FIELDS}
        safe_data['ticket_id'] = f"TICK-{uuid.uuid4().hex[:6].upper()}"
        return Ticket.objects.create(created_by=user, **safe_data)

    @staticmethod
    def add_comment(ticket_id, user, text):
        return Comment.objects.create(ticket_id=ticket_id, author=user, text=text)

    @staticmethod
    def perform_action(ticket_id, action_type):
        try:
            ticket = Ticket.objects.get(pk=ticket_id, is_deleted=False)
        except Ticket.DoesNotExist:
            return None, "Ticket not found"
        if action_type == "RESOLVE":
            ticket.status = "RESOLVED"
        elif action_type == "CLOSE":
            ticket.status = "CLOSED"
        ticket.save()
        return ticket, None
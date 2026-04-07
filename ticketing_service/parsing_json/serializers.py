def ticket_view(ticket):
    return {
        "id": ticket.id,
        "ticket_no": ticket.ticket_id,
        "title": ticket.title,
        "status": ticket.status,
        "created_at": ticket.created_at.isoformat(),
        "created_by": {
            "id": ticket.created_by.id,
            "username": ticket.created_by.username
        } if ticket.created_by else None
    }

def tickets_list_view(tickets):
    return [ticket_view(t) for t in tickets]
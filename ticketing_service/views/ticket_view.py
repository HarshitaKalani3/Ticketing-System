from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ..handler.ticket_handler import TicketHandler
from ..parsing_json import serializers
from ..validator.ticket_validator import validate_ticket_request
from ..dao.models import Ticket


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # disable CSRF for API testing


ALLOWED_PATCH_FIELDS = {'title', 'description', 'priority', 'status', 'assigned_to'}
VALID_ACTIONS = {'RESOLVE', 'CLOSE'}


class BaseView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class TicketController(BaseView):
    # 1. Create Ticket
    def post(self, request):
        is_valid, error = validate_ticket_request(request.data)
        if not is_valid:
            return Response({"error": error}, status=400)
        ticket = TicketHandler.create_ticket(request.data, request.user)
        return Response(serializers.ticket_view(ticket), status=201)

    # 2. Get All Tickets
    def get(self, request):
        tickets = Ticket.objects.filter(is_deleted=False)
        return Response(serializers.tickets_list_view(tickets))

class TicketDetailController(BaseView):
    def get_ticket(self, pk):
        try:
            return Ticket.objects.get(pk=pk, is_deleted=False), None
        except Ticket.DoesNotExist:
            return None, Response({"error": "Ticket not found"}, status=404)

    # 3. Get By ID
    def get(self, request, pk):
        ticket, err = self.get_ticket(pk)
        if err: return err
        return Response(serializers.ticket_view(ticket))

    # 4. Patch Ticket
    def patch(self, request, pk):
        ticket, err = self.get_ticket(pk)
        if err: return err
        safe_data = {k: v for k, v in request.data.items() if k in ALLOWED_PATCH_FIELDS}
        Ticket.objects.filter(pk=pk).update(**safe_data)
        return Response({"message": "Updated"})

    # 5. Delete Ticket
    def delete(self, request, pk):
        ticket, err = self.get_ticket(pk)
        if err: return err
        Ticket.objects.filter(pk=pk).update(is_deleted=True)
        return Response(status=204)

class CommentController(BaseView):
    # 6. Add Comment
    def post(self, request, pk):
        try:
            Ticket.objects.get(pk=pk, is_deleted=False)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)
        comment = TicketHandler.add_comment(pk, request.user, request.data.get('text'))
        return Response({"id": comment.id}, status=201)

    # 7. List Comments
    def get(self, request, pk):
        try:
            comments = Ticket.objects.get(pk=pk, is_deleted=False).comments.all()
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)
        return Response([{"text": c.text, "user": c.author.username} for c in comments])

class UserTicketController(BaseView):
    # 8. Assigned to me
    def get(self, request):
        tickets = Ticket.objects.filter(assigned_to=request.user, is_deleted=False)
        return Response(serializers.tickets_list_view(tickets))

class CreatedTicketController(BaseView):
    # 9. My Created Tickets
    def get(self, request):
        tickets = Ticket.objects.filter(created_by=request.user, is_deleted=False)
        return Response(serializers.tickets_list_view(tickets))

class ActionController(BaseView):
    # 10. Perform Action (Resolve/Close)
    def post(self, request, pk):
        action = request.data.get('action')
        if action not in VALID_ACTIONS:
            return Response({"error": f"Invalid action. Must be one of: {VALID_ACTIONS}"}, status=400)
        ticket, err = TicketHandler.perform_action(pk, action)
        if err:
            return Response({"error": err}, status=404)
        return Response({"status": "Action Performed"})
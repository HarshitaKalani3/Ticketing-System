from django.urls import path
from .views.ticket_view import (
    TicketController,
    TicketDetailController,
    CommentController,
    UserTicketController,
    CreatedTicketController,
    ActionController,
)

urlpatterns = [
    path('tickets/', TicketController.as_view()),                        # POST: create, GET: list all
    path('tickets/<int:pk>/', TicketDetailController.as_view()),         # GET, PATCH, DELETE
    path('tickets/<int:pk>/comments/', CommentController.as_view()),     # POST: add, GET: list
    path('tickets/<int:pk>/action/', ActionController.as_view()),        # POST: resolve/close
    path('tickets/assigned-to-me/', UserTicketController.as_view()),     # GET: assigned to me
    path('tickets/created-by-me/', CreatedTicketController.as_view()),   # GET: created by me
]

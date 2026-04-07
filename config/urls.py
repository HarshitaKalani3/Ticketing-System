from django.contrib import admin
from django.urls import path
from ticketing_service.views import ticket_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tickets/', ticket_view.TicketController.as_view()),                        # POST: create, GET: list all
    path('api/tickets/<int:pk>/', ticket_view.TicketDetailController.as_view()),         # GET, PATCH, DELETE
    path('api/tickets/<int:pk>/comments/', ticket_view.CommentController.as_view()),     # POST: add, GET: list
    path('api/tickets/<int:pk>/perform-action/', ticket_view.ActionController.as_view()),# POST: resolve/close
    path('api/tickets/assigned-to-me/', ticket_view.UserTicketController.as_view()),     # GET: assigned to me
    path('api/tickets/created-by-me/', ticket_view.CreatedTicketController.as_view()),   # GET: created by me
]

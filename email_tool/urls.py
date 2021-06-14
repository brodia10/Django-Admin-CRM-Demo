from django.urls import path
from . import views

urlpatterns = [
    path("unsubscribe/<uuid:message_token>", views.unsubscribe, name="unsubscribe"),
    path(
        "unsubscribe/<uuid:message_token>/confirmed/",
        views.unsubscribe_confirmed,
        name="unsubscribe_confirmed",
    ),
    path("batches/<uuid:batch_token>/preview", views.preview_batch, name="preview_batch"),
]

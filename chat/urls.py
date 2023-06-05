from django.urls import path
from . import views

urlpatterns = [
    path("messages", views.message_home, name="messages"),
    path("message/<pk>", views.chat, name="message-one"),
    path("messages/<uuid>", views.message_page, name="message-area"),
    path("messages/upload/<uuid>", views.msg_upload, name="upload")
]

# fake_site/app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('admin-messages/', views.admin_messages, name='admin_messages'),
    path("send-reply/<int:msg_id>/", views.send_reply, name="send_reply"),
    path("notifications/", views.notifications, name="notifications"),
    path('notifications/read/', views.mark_read, name='mark_read'),
    path("admin-messages/", views.admin_messages, name="admin_messages"),
    path("admin-messages/<int:message_id>/reply/", views.reply_message, name="reply_message"),

    # Prediction routes
    path('predict/', views.predict_review, name='predict_review'),
]


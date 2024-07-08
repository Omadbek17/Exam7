from django.urls import path, include
from blog.views import IndexView, EventsListView, EventsDetailView, verify_email_done, verify_email_confirm, verify_email_complete, PeopleSave, ContactSave
from blog.auth import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('events-lists/',EventsListView.as_view(),name='events-lists'),
    path('event-detail/<int:pk>',EventsDetailView.as_view(),name='event-detail'),
    # login
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
     #  verify email url
    path('verify-email-done/', verify_email_done, name='verify_email_done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify_email_confirm'),
    path('verify-email/complete/', verify_email_complete, name='verify_email_complete'),
    path('people-save/', PeopleSave.as_view(),name = 'people_save'),
    path('contact-save/', ContactSave.as_view(),name = 'contact_save'),

]

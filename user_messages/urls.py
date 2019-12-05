from django.urls import include, path
from user_messages.views import *

app_name = 'user_messages'

urlpatterns = [
    path('', UserMessageListView.as_view(), name='List'),
    path('create/<int:user_id>/<int:pet_id>/', UserMessageCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', UserMessageDetailView.as_view(), name='detail'),
    path('<int:pk>/delete', UserMessageDeleteView.as_view(), name='delete'),
]




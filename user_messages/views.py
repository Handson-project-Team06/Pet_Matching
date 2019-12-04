from django.shortcuts import render, get_object_or_404
from django.views import generic
from .forms import UserMessageForm
from .models import UserMessages
from django.urls import reverse_lazy
from matching.models import *
from accounts.models import User


class UserMessageCreateView(generic.CreateView):
    form_class = UserMessageForm
    model = UserMessages
    template_name = 'user_messages/user_message_form.html'
    success_url = reverse_lazy('matching:home')

    def get_form_kwargs(self):
        receiver = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        pet = get_object_or_404(Pet, pk=self.kwargs.get('pet_id'))
        kwargs = super(UserMessageCreateView, self).get_form_kwargs()
        kwargs['sender'] = self.request.user
        kwargs['receiver'] = receiver
        kwargs['pet'] = pet
        return kwargs


class UserMessageDetailView(generic.DetailView):
    model = UserMessages
    template_name = 'user_messages/user_message_detail.html'

class UserMessageListView(generic.ListView):
    model = UserMessages
    template_name = 'user_messages/user_message_list.html'

    def get_queryset(self):
        queryset = super(UserMessageListView, self).get_queryset()
        return queryset.filter(receiver=self.request.user)

class UserMessageDeleteView(generic.DeleteView):
    model = UserMessages
    success_url = reverse_lazy('user_messages:List')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

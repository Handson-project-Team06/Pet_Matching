from django.shortcuts import render
from .models import Pet
from .filters import PetFilter
from django.views import generic
from matching.forms import PetCreationForm
from django.urls import reverse_lazy


# Create your views here.

def home(request):
    pet_list = Pet.objects.all()
    pet_filter = PetFilter(request.GET,queryset=pet_list)
    return render(request,'matching/home.html',{'filter':pet_filter})


# 반려동물 리스트
class PetListView(generic.ListView):
    template_name = 'matching/pet_list.html'
    model = Pet

    def get_queryset(self):
        queryset = super(PetListView, self).get_queryset()
        return queryset.exclude(owner=self.request.user)


# 내 반려동물 등록
class PetCreateView(generic.CreateView):
    model = Pet
    form_class = PetCreationForm
    template_name = 'matching/pet_form.html'
    success_url = reverse_lazy('matching:my_pet_list')

    def get_form_kwargs(self):
        kwargs = super(PetCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# 내 반려동물 등록
class PetUpdateView(generic.UpdateView):
    model = Pet
    form_class = PetCreationForm
    template_name = 'matching/pet_form.html'
    success_url = reverse_lazy('matching:my_pet_list')

    def get_form_kwargs(self):
        kwargs = super(PetUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# 내 반려동물 보기
class MyPetListView(generic.ListView):
    template_name = 'matching/my_pet_list.html'
    model = Pet

    def get_queryset(self):
        queryset = super(MyPetListView, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class PetDeleteView(generic.DeleteView):
    model = Pet
    success_url = reverse_lazy('matching:my_pet_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

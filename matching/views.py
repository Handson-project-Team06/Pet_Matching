from django.shortcuts import render,get_object_or_404
from .models import Pet
from .filters import PetFilter
from django.views import generic
from matching.forms import PetCreationForm
from django.urls import reverse_lazy
import urllib.request,urllib.parse
import simplejson as json
# Create your views here.

def home(request):
    pet_list = Pet.objects.all()
    pet_filter = PetFilter(request.GET,queryset=pet_list)
    nearby_locations , distance = get_locations_nearby_coords(2,5, 7000)
    town, country = getplace(2.0, 3)
    return render(request,'home.html',{'filter':pet_filter, 'nearby_locations':nearby_locations, 'distance':distance, 'town' : town, 'country' : country})


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
        self.new_pet()
        #form = PetCreationForm(self.request.POST)
        #form.save(commit=True)
        return kwargs

    def geocode(self, location):
        key = "AIzaSyBlu5QpKaxho5vC2yN871kC0vEgtcMqNfQ"
        output = "json"
        location = urllib.parse.quote(location)
        request = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=%s&language=ko&inputtype=textquery&fields=geometry&key=%s" % (location, key)
        data = urllib.request.urlopen(request).read()
        dlist = json.loads(data.decode('utf-8'))
        if dlist["status"] == "OK":
            return "%s,%s" % (dlist['candidates'][0]['geometry']['location']['lat'],\
                 dlist['candidates'][0]['geometry']['location']['lng'])
        else:
            return ','

    def new_pet(self):
        #pet=get_object_or_404(Pet,pk=self.kwargs['pk'])
        print(self.kwargs)
        address = self.request.POST.get('address')
        city = self.request.POST.get('city')
        country = self.request.POST.get('country')
        print(address,city,country)
        location = "%s, %s, %s" % (address, city, country)
        latlng = self.geocode(location)
        latlng = latlng.split(',')
        self.lat = latlng[0]
        self.lon = latlng[1]
        return self

# 내 반려동물 수정
class PetUpdateView(generic.UpdateView,):
    model = Pet
    form_class = PetCreationForm
    template_name = 'matching/pet_form.html'
    success_url = reverse_lazy('matching:my_pet_list')

    def get_form_kwargs(self):
        kwargs = super(PetUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        self.edit_pet()
        return kwargs

    def geocode(self, location):
        key = "AIzaSyBlu5QpKaxho5vC2yN871kC0vEgtcMqNfQ"
        output = "json"
        location = urllib.parse.quote(location)
        request = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=%s&language=ko&inputtype=textquery&fields=geometry&key=%s" % (location, key)
        data = urllib.request.urlopen(request).read()
        dlist = json.loads(data.decode('utf-8'))
        if dlist["status"] == "OK":
            return "%s,%s" % (dlist['candidates'][0]['geometry']['location']['lat'],\
                 dlist['candidates'][0]['geometry']['location']['lng'])
        else:
            return ','

    def edit_pet(self):
        pet=get_object_or_404(Pet,pk=self.kwargs['pk'])
        location = "%s, %s, %s" % (pet.address, pet.city, pet.country)
        latlng = self.geocode(location)
        latlng = latlng.split(',')
        if pet.lat != latlng[0] :
            pet.lat = latlng[0]
            pet.lon = latlng[1]
        pet.save()
    
    

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

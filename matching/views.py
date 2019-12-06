from django.shortcuts import render,get_object_or_404
from .models import Pet
from .filters import PetFilter,get_locations_nearby_coords,getplace
from django.views import generic
from matching.forms import PetCreationForm
from django.urls import reverse_lazy
import urllib.request,urllib.parse
import simplejson as json
from accounts.models import User
# Create your views here.

def pet_list_function(request):
    pet_list = Pet.objects.all()
    pet_filter = PetFilter(request.GET,queryset=pet_list)
    owner=request.user
    if 'distance_search' in request.GET and request.GET['distance_search'] :
        max_distance = int(request.GET['distance_search'])
        dis_filter , distance = get_locations_nearby_coords(owner.address, max_distance)
        flag=int(request.GET['distance_search'])
        #dis_filter = PetFilter(request.GET,queryset=dis_filter)
        return render(request,'matching/pet_list.html',{'filter':pet_filter,'dis_filter':dis_filter, 'distance':distance,'owner':owner,'flag':flag})
    return render(request,'matching/pet_list.html',{'filter':pet_filter,'owner':owner})


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
        kwargs['lat'], kwargs['lon'] = self.new_pet()
        kwargs['user'] = self.request.user
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
        address = self.request.POST.get('address')
        location = "%s" % (address)
        latlng = self.geocode(location)
        latlng = latlng.split(',')
        return latlng[0], latlng[1]

# 내 반려동물 수정
class PetUpdateView(generic.UpdateView):
    model = Pet
    form_class = PetCreationForm
    template_name = 'matching/pet_form.html'
    success_url = reverse_lazy('matching:my_pet_list')

    def get_form_kwargs(self):
        kwargs = super(PetUpdateView, self).get_form_kwargs()
        kwargs['lat'], kwargs['lon'] = self.edit_pet()
        kwargs['user'] = self.request.user
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
        location = "%s" % (pet.address)
        latlng = self.geocode(location)
        latlng = latlng.split(',')
        return latlng[0],latlng[1]
    
#반려동물 상세페이지
class PetListDetailView(generic.DetailView):
        template_name = 'matching/pet_detail.html'
        model = Pet
        

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

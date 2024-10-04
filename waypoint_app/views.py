from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets

from .forms import *
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import AllowAny
import requests
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]


class DestinationDetail(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestinationUpdate(generics.RetrieveUpdateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestinationDelete(generics.DestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestinationSearch(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        place_name = self.kwargs.get('Name')
        return Destination.objects.filter(place_name__icontains=place_name)


def create_Destination(request):
    if request.method == 'POST':
        print(request.POST)
        form = DestinationForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/destinations/'
                data = form.cleaned_data
                print(data)

                response = requests.post(api_url, data=data, files={'image': request.FILES['image']})
                print(response)
                if response.status_code == 400:
                    messages.success(request, 'destination inserted successfully')
                    return redirect('/index')
                else:
                    messages.error(request, f'Error{response.status_code}')

            except requests.RequestException as e:
                messages.error(request, f'Error during api request {str(e)}')
        else:
            print(form.errors)
            messages.error(request, 'Form is invalid')
    else:
        form = DestinationForm()
    return render(request, 'add_place.html', {'form': form})


def update_detail(request, id):
    api_url = 'http://127.0.0.1:8000/detail/{id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        details = data['description'].split(',')
    return render(request, 'destination_list.html', {Destination: data, 'details': details})


def update_destination(request, id):
    if request.method == 'POST':
        place_name = request.POST['place_name']
        weather = request.POST['weather']
        location_state = request.POST['location_state']
        location_district = request.POST['location_district']
        google_map_link = request.POST['google_map_link']
        print('Image Url', request.FILES.get('image'))
        print(request.POST)
        print(request.FILES)
        description = request.POST['description']
        api_url = f'http://127.0.0.1:8000/update/{id}/'

        data = {
            'place_name': place_name,
            'weather': weather,
            'location_state': location_state,
            'location_district': location_district,
            'google_map_link': google_map_link,
            'description': description
        }
        files = {'image': request.FILES.get('image')}
        response = requests.put(api_url, data=data, files=files)
        if response.status_code == 200:
            messages.success(request, 'Destination update successfully')
            return redirect(f'/destination_fetch/{id}')

        else:
            messages.error(request, f'error submitting data to the rest api:{response.status_code}')
    return redirect('/')


def index(request):
    if request.method == 'POST':
        search = request.POST['search']

        api_url = f'http://127.0.0.1:8000/search/{search}/'
        # try:
        #     response = requests.get(api_url)
        #     print(response.status_code)
        #     if response.status_code == 200:
        #         data=response.json()
        #     else:
        #         data=None
        # except requests.RequestException as e:
        #     data:None
        # return render(request,'destination_list.html',{'data':data})
    else:
        api_url = f'http://127.0.0.1:8000/destinations/'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            original_data = data
            paginator = Paginator(original_data, 6)

            try:
                page = int(request.GET.get('page', 1))
            except:
                page = 1
            try:
                destination = paginator.page(page)
            except(EmptyPage, InvalidPage):
                destination = Paginator.page(paginator.num_pages)

            context = {
                'original_data': original_data,
                'destinations': destination
            }
            return render(request, 'destination_list.html', context)
        else:
            return render(request, 'destination_list.html', {'error_message': f'Error:{response.status_code}'})
    except requests.RequestException as e:
        return render(request, 'destination_list.html', {'error_message': f'Error:{str(e)}'})

    return render(request, 'destination_list.html')


def destination_fetch(request, id):
    api_url = f'http://127.0.0.1:8000/detail/{id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        details = data['description'].split(',')
        return render(request, 'destination_detail.html', {'destination': data, 'details': details})
    return render(request, 'destination_detail.html')


def destination_update_form(request, id):
    api_url = f'http://127.0.0.1:8000/detail/{id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        details = data['description'].split(',')
        return render(request, 'destination_update.html', {'destination': data, 'details': details})
    return render(request, 'destination_update.html')


def destination_delete(request, id):
    api_url = f'http://127.0.0.1:8000/delete/{id}/'
    response = requests.delete(api_url)
    if response.status_code == 200:
        print(f'Item with id{id} has been deleted')
    else:
        print(f'Failed to delete item.status code {response.status_code}')
    return redirect('/index')

#from django.shortcuts import render
from .models import facility,Account,Profile
from .serializers import FacilitySerializer, AccountSeriallizer,ProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from rest_framework.filters import SearchFilter
from rest_framework import filters, generics
import haversine as hs
# Create your views here.


# Create your views here




#@api_view(['POST'])
#def Facilitycreate(request):
#    serializer = FacilitySerializer(data=request.data)
#    if serializer.is_valid():
#            serializer.save()
#          return Response(serializer.data)
#    return Response(serializer.data)


# def addgeo(request):
def Facilitycreate(request):


    URL = "https://discover.search.hereapi.com/v1/discover"
    latitude = 31.331892
    longitude = 75.546906
    api_key = 'QluWI2XJf3Cq9cee46zVvBP5ys0KaH0yd8_3v6GlNGc'  # Acquire from developer.here.com
    query = 'Hotel'
    limit = 5

    PARAMS = {
        'apikey': api_key,
        'q': query,
        'limit': limit,
        'at': '{},{}'.format(latitude, longitude)
    }

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    print(data)

    for x in range(5):
        hospitalOne = data['items'][x]['title']
        hospitalOne_address = data['items'][x]['address']['label']
        hospitalOne_state = data['items'][x]['address']['state']
        hospitalOne_country = data['items'][x]['address']['countryName']
        hospitalOne_city = data['items'][x]['address']['city']
        hospitalOne_latitude = data['items'][x]['position']['lat']
        hospitalOne_longitude = data['items'][x]['position']['lng']
        hospitalOne_email = hospitalOne + '@gmail.com'
        hospitalOne_pin = data['items'][x]['address']['postalCode']
        hospitalOne_phone = '9876543211'
        d = facility.objects.create(category='Hotel',Name=hospitalOne,email=hospitalOne_email,phone=hospitalOne_phone,local=hospitalOne_address,city=hospitalOne_city,state=hospitalOne_state,country=hospitalOne_country,
                                        pincode=hospitalOne_pin,longitude=hospitalOne_longitude,lattitude=hospitalOne_latitude
                                    )
        d.save()
    print(hospitalOne, hospitalOne_address, hospitalOne_city, hospitalOne_state, hospitalOne_country,
              hospitalOne_longitude, hospitalOne_latitude, hospitalOne_phone, hospitalOne_email)

class FacilityAPIView(generics.ListCreateAPIView):
    facilty=facility.objects.all()
    for x in facilty:
        loc1 = (31.341229983813587, 75.54846299825678)
        print(x.lattitude, x.longitude)
        loc2 = (x.lattitude, x.longitude)
        dis= hs.haversine(loc1, loc2)
        print(dis)
        y=facility.objects.update(distance=dis)

        print(x)

    class Filter(FilterSet):
        class Meta:
            model = facility
            fields = {'category' : ['exact'],
                      'mode': ['exact'],
                      'field': ['exact'],
                      'distance': ['lte'],}

    queryset = facility.objects.all()
    serializer_class = FacilitySerializer
    filter_class = Filter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['Name']

class Profile_filter(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = {'interests1' :['exact'],
                     'interests2' :['exact'],
                     'interests3' :['exact'],
                     'interests4' :['exact'],}


class AccountView(APIView):
    def get(self,request,id=None,format=None):
        id=id
        if id is not None:
            user=Account.objects.get(id=id)
            serializer=AccountSeriallizer(user)
            return Response(serializer.data)

        user=Account.objects.all()
        serializer=AccountSeriallizer(user,many=True)
        return Response(serializer.data)



    def post(self,request,format=None):
        serializer=AccountSeriallizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"usercreated"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self,request,format=None):
        user=Profile.objects.all()
        serializer=ProfileSerializer(user,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer=ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Profile created successfully"},status=status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)





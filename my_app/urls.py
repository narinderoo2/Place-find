from django.urls import path
from my_app import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('accountApi/',views.AccountView.as_view()),
    path('accountApi/<int:id>',views.AccountView.as_view(),name='accountApi'),
    path('profileApi/',views.ProfileView.as_view(),name='profileApi'),
    path('login/',obtain_auth_token,name='login'),
#    path('', views.Facilitycreate),
    path('fac/', views.FacilityAPIView.as_view()),
    path('profilters',views.Profile_filter.as_view()),
]

#on testing static file location url Below
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
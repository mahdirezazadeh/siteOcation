from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('websites/', views.WebsiteListView.as_view(), name='websites'),

    # pk (short for primary key) in our website model is website_domain_name
    # path(r'^website/(?P<pk>[-\w]+)$', views.WebisteDetailView.as_view(), name='website-detail'),
]

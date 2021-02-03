"""siteOcation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls import include
from django.views.generic import RedirectView
# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
from website import views as website_veiws

# url for admin page
urlpatterns = [
    path('admin/', admin.site.urls),
]

# url for home
urlpatterns += [
    path('home/', include('website.urls')),
]

# urls for website , user , about and contact
urlpatterns += [
    path('', RedirectView.as_view(url='home/', permanent=True)),
    path('website/<pk>/', website_veiws.website_detail, name='website-detail'),
    path('user/<pk>/', website_veiws.user_detail, name='user-detail'),
    path('about/', website_veiws.about),
    path('contact/', website_veiws.contact),
    path('websites/', website_veiws.website_list_view, name='websites'),

    # pk (short for primary key) in our website model is website_domain_name
    # re_path(r'^website\/(?P<pk>[\w-]+)\/$', website_veiws.WebisteDetailView.as_view(website_domain_name='pk'),
    #         name='website-detail'),
]

# Use static() to add url mapping to serve static files during development (only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# url for accounts
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

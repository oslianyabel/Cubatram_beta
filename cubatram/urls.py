"""
URL configuration for cubatram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from home.views import destination_selected, home, tour_detail, tour_list

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
] + i18n_patterns(
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path(
        "tours/destination/<slug:slug>/",
        destination_selected,
        name="destination_selected",
    ),
    path(
        "tours/destination/<slug:destination_slug>/category/<slug:category_slug>/",
        tour_list,
        name="tour_list",
    ),
    path(
        "tours/destination/<slug:destination_slug>/category/<slug:category_slug>/<slug:tour_slug>/",
        tour_detail,
        name="tour_detail",
    ),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

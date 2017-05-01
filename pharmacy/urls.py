"""pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from authentication import views as peekstudy_auth_views
from core import views as core_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from search import views as search_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^home/$', core_views.home_main, name='home_main'),
#auth urls
    url(r'^login/', auth_views.login, {'template_name': 'core/cover.html'},
        name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', peekstudy_auth_views.signup, name='signup'),
    url(r'^signupdetailed/$', peekstudy_auth_views.signupdetailed, name='signupdetailed'),

#account urls
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    url(r'^settings/upload_picture/$', core_views.upload_picture,
        name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^settings/password/$', core_views.password, name='password'),

#admin url
    url(r'^useradmin/', include('useradmin.urls')),

#company url
    url(r'^usercompany/', include('usercompany.urls')),

#shop url
    url(r'^usershop/', include('usershop.urls')),

    url(r'^activities/', include('activities.urls')),

    url(r'^search/$', search_views.search, name='search'),

    url(r'^user/(?P<username>[^/]+)/$', core_views.profile, name='profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

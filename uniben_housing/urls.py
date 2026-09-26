from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # This sends all normal website traffic to our housing app
    path('', include('housing.urls')),
    
    path('accounts/', include('allauth.urls')), # path for google authentication
    
    # Route to serve the Service Worker at the root of the domain
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),
]

# This line allows Django to serve your uploaded videos while in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

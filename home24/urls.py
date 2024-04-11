from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from yourhome.views import login_register
from yourhome import two_factor_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/jsi18n/', JavaScriptCatalog.as_view(), name='jsi18n'),
    path('admin/jsi18n/', JavaScriptCatalog.as_view(), name='jsi18n'),
    path("", include("yourhome.urls")),
    path('accounts/login_register/', login_register, name='login_register'),
    path('accounts/', include((two_factor_urls, 'two_factor'), namespace='accounts')),
]



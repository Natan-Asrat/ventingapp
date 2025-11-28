from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/account/", include("account.urls")),
    path("api/post/", include("post.urls")),
    path("api/transaction/", include("transaction.urls")),
    path("api/notification/", include("notification.urls")),
    path("api/report/", include("report.urls")),
    path("api/support/", include("support.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

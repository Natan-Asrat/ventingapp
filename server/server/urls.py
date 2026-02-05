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
    path("api/usage/", include("usage.urls")),
    path("api/chat/", include("conversation.urls")),
    path("api/support/", include("support.urls")),
    path("api/analytics/", include("analytics.urls"))
]

if not settings.FROM_S3:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path(f"{settings.PATH_PREFIX}/admin/", admin.site.urls),
    path(f"{settings.PATH_PREFIX}/api/account/", include("account.urls")),
    path(f"{settings.PATH_PREFIX}/api/post/", include("post.urls")),
    path(f"{settings.PATH_PREFIX}/api/transaction/", include("transaction.urls")),
    path(f"{settings.PATH_PREFIX}/api/notification/", include("notification.urls")),
    path(f"{settings.PATH_PREFIX}/api/report/", include("report.urls")),
    path(f"{settings.PATH_PREFIX}/api/usage/", include("usage.urls")),
    path(f"{settings.PATH_PREFIX}/api/chat/", include("conversation.urls")),
    path(f"{settings.PATH_PREFIX}/api/support/", include("support.urls")),
    path(f"{settings.PATH_PREFIX}/api/analytics/", include("analytics.urls"))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()

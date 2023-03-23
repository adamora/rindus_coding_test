from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from rindus_coding_test.core.api.views import CommentViewSet, PostViewSet
from rindus_coding_test.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)


app_name = "api"
urlpatterns = router.urls

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = router.urls
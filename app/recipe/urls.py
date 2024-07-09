from recipe.views import RecipeViewSet
from rest_framework.routers import DefaultRouter

app_name = 'recipe'

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="recipe")
urlpatterns = router.urls
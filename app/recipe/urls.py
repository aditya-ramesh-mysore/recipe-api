from recipe.views import RecipeViewSet, TagViewSet
from rest_framework.routers import DefaultRouter

app_name = 'recipe'

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("tags", TagViewSet, basename="tag")
urlpatterns = router.urls
print(urlpatterns)
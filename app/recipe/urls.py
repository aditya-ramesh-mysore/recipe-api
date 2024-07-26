from recipe.views import RecipeViewSet, TagViewSet, IngredientListView, IngredientDetailView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

app_name = 'recipe'

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("tags", TagViewSet, basename="tag")

ingredient_urls = [
    path('ingredients/', IngredientListView.as_view(), name="ingredient-list"),
    path('ingredients/<int:id>/', IngredientDetailView.as_view(), name="ingredient-detail"),
]
urlpatterns = router.urls + ingredient_urls

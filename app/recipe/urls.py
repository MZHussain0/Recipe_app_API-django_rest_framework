from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('tag', views.TagViewSet)
router.register('ingredient', views.IngredientViewset)
router.register('recipes', views.RecipeViewset)

aap_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]

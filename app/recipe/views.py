from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from core.models import Tag, Ingredient, Recipe


class BaseRecipeAttr(viewsets.GenericViewSet,
                     mixins.CreateModelMixin, mixins.ListModelMixin):
    """ Basic viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return the object for the authenticatd user """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new tag """

        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttr):
    """ Manage Tags in the database """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewset(BaseRecipeAttr):
    """ Manage ingredients in the database """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewset(viewsets.ModelViewSet):
    """ Manages recipes in the database """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Retrieve recipes for the authenticated users """
        return self.queryset.filter(user=self.request.user)

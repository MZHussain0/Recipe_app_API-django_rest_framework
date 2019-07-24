from core.models import Tag, Ingredient, Recipe
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TagSerializer, IngredientSerializer, \
    RecipeSerializer, RecipeDetailSerializer, RecipeImageSerializer


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

    def get_serializer_class(self):
        """ Return appropriate serializer """
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """ Create new recipe """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ upload an image to a recipe """
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Ressponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

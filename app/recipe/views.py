from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, authentication, permissions, mixins, generics, views
from rest_framework.response import Response
from core.models import Recipe, Tag, Ingredient
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer, RecipeImageSerializer
from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description="Tag IDs list"
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description="Ingredient IDs list"
            )
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def __convert_string_to_int_list(self, string_list):
        return [int(s) for s in string_list.split(',')]
    def get_object(self):
        try:
            qs = self.get_queryset()
            recipe_obj = qs.get(id=self.kwargs['id'])
            return recipe_obj
        except Recipe.DoesNotExist:
            raise Http404


    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        ingredients = self.request.query_params.get('ingredients', None)
        qs = Recipe.objects.all()
        if tags:
            tags = self.__convert_string_to_int_list(tags)
            qs = Recipe.objects.filter(tags__id__in=tags)
        if ingredients:
            ingredients = self.__convert_string_to_int_list(ingredients)
            qs = qs.filter(ingredients__id__in=ingredients)

        return qs.filter(user=self.request.user).order_by('-id')

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RecipeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        recipe = self.get_object()
        serializer = self.serializer_class(recipe)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeImageView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecipeImageSerializer

    def post(self, request, *args, **kwargs):
        recipe_id = self.kwargs['id']
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(recipe_id)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        recipe_id = self.kwargs['id']
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404
        serializer = self.serializer_class(recipe)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.STR,
                description="Integer 1, indicating only tags attached to a recipe is allowed, 0 otherwise"
            )
        ]
    )
)
class TagViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        assigned_only = bool(int (self.request.query_params.get('assigned_only', 0)))
        qs = Tag.objects.filter(user=self.request.user).order_by('name')
        if assigned_only:
            qs = qs.filter(recipe__isnull=False)
        return qs.distinct()

class IngredientView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IngredientSerializer

class IngredientListView(IngredientView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.STR,
                description="Integer 1, indicating only ingredients attached to a recipe is allowed, 0 otherwise"
            )
        ]
    )
    def get(self, request, format=None):
        assigned_only = bool(int(request.query_params.get('assigned_only', 0)))
        qs = Ingredient.objects.filter(user=request.user)
        if assigned_only:
            qs = qs.filter(recipe__isnull=False)
        serializer = self.serializer_class(qs.distinct(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetailView(IngredientView):

    def get_object(self, id=None):
        try:
            obj = Ingredient.objects.get(id=id)
        except Ingredient.DoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, *args, **kwargs):
        id = kwargs.get('id')
        ingredient = self.get_object(id)
        serializer = self.serializer_class(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        ingredient = self.get_object(id)
        serializer = self.serializer_class(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        ingredient = self.get_object(id)
        serializer = self.serializer_class(ingredient)
        ingredient.delete()
        return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        ingredient = self.get_object(kwargs.get("id"))
        serializer = self.serializer_class(ingredient)
        return Response(serializer.data, status=status.HTTP_200_OK)
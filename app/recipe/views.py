from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, authentication, permissions, mixins, generics, views
from rest_framework.response import Response
from core.models import Recipe, Tag, Ingredient
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer
from django.http import Http404

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_object(self):
        try:
            qs = self.get_queryset()
            recipe_obj = qs.get(id=self.kwargs['id'])
            return recipe_obj
        except Recipe.DoesNotExist:
            raise Http404


    def get_queryset(self):
        if self.request.user:
            return Recipe.objects.filter(user=self.request.user).order_by('-id')
        else:
            return Recipe.objects.all()

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


class TagViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('name')

class IngredientView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IngredientSerializer

class IngredientListView(IngredientView):

    def get(self, request, format=None):
        qs = Ingredient.objects.filter(user=request.user)
        serializer = self.serializer_class(qs, many=True)
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
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, authentication, permissions, mixins, generics
from rest_framework.response import Response
from core.models import Recipe, Tag
from .serializers import RecipeSerializer, TagSerializer
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
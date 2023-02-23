from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView

from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer
from django.core.exceptions import ValidationError
import json


class CategoriaView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProdutoView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CategoriaList(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutosCategoriaView(APIView):
    def get(self, request, categoria_id):
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            produtos = Produto.objects.filter(categoria=categoria)
            serializer = ProdutoSerializer(produtos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoria não encontrada"}, status=status.HTTP_404_NOT_FOUND)

class ProdutoListView(ListAPIView):

    serializer_class = ProdutoSerializer

    def get_queryset(self):
        queryset = Produto.objects.all()

        operador = self.request.query_params.get('operador')
        preco = self.request.query_params.get('preco')

        if operador and preco:
            if operador == '<':
                queryset = queryset.filter(preco__lt=preco)
            elif operador == '<=':
                queryset = queryset.filter(preco__lte=preco)
            elif operador == '=':
                queryset = queryset.filter(preco=preco)
            elif operador == '=>':
                queryset = queryset.filter(preco__gte=preco)
            elif operador == '>':
                queryset = queryset.filter(preco__gt=preco)
            else:
                raise ValidationError("Operador inválido. Os operadores válidos são: <, <=, =, =>, >.")
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

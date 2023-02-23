from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CategoriaView, ProdutoView, CategoriaList, ProdutosCategoriaView, ProdutoListView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('cad_categorias/', CategoriaView.as_view(), name="categoria-cad"),
    path('cad_produtos/', ProdutoView.as_view(), name="produto-cad"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('categorias/', CategoriaList.as_view(), name='categorias'),
    path('categorias/<int:categoria_id>/produtos/', ProdutosCategoriaView.as_view()),
    path('produtos/', ProdutoListView.as_view(), name='produto-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from store.views import *

app_name = "store"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search/", SearchView.as_view(), name="search"),
    path("tag/<slug:slug>", TagView.as_view(), name="tag"),
    path("category/<int:idcategory>/", CategoryView.as_view(), name="category"),
    path("remedios/<int:pk>/", Goods_View.as_view(), name="goods"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
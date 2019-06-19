from django.urls import path

from appMovie.api.viewsets import ExampleViewset, ExampleModelViewset

viewsetmodel_list = ExampleModelViewset.as_view({
    'get': 'list',
    'post': 'create'
})
viewsetmodel_detail = ExampleModelViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [

    path('movie/', viewsetmodel_list, name="viewsetmodel-list"),
    path('movie/<slug>', viewsetmodel_detail, name="viewsetmodel-detail"),
]

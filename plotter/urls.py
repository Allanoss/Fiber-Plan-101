from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='plotter-index'),
    path('plot/create', views.create, name='plotter-create'),
    path('plot/<int:id>/populate', views.populate, name='plotter-populate'),
    path('plot/<int:id>/more_settings', views.more_settings, name='plotter-more_settings'),
    path('plot/<int:id>properties', views.properties, name='plotter-properties'),
    path('plot/coordinate/<int:id>/delete', views.coordinate_delete, name='plotter-coordinate-delete'),
    path('plot/<int:id>', views.plot, name='plotter-plot'),
    path('plot/<int:id>/item', views.quote_item, name='plotter-quote_item'),
    path('plot/<int:id>/price', views.quote_price, name='plotter-quote_price'),
    path('network/<int:id>', views.network, name='plotter-network'),
    path('plot/<int:id>/delete', views.plot_delete, name='plotter-plot-delete'),
    # items
    path('items', views.item_list, name='plotter-item_list'),
    path('items/create', views.item_create, name='plotter-item_create'),
    path('items/<int:id>/update', views.item_update, name='plotter-item_update'),
    path('items/<int:id>/delete', views.item_delete, name='plotter-item_delete'),
]

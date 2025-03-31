import django_filters 
from multimedia.models import videos, VideoUpload
from Members.models import Purchased, DepositHistory, DownloadHistory, Onwatch,Cart

class VideoFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    
    class Meta:
        model = videos
        fields = ["name"]
class VideoUploadFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='contains')
    typs = django_filters.CharFilter(field_name='typs', lookup_expr='contains')
    
    class Meta:
        model = VideoUpload
        fields = ["title", "typs"]

class SearchUploadFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='contains')
    cartegory = django_filters.CharFilter(field_name='cartegory', lookup_expr='exact')
    typs = django_filters.CharFilter(field_name='typs', lookup_expr='contains')
    popular = django_filters.BooleanFilter(field_name='popular', lookup_expr='exact')
    
    class Meta:
        model = VideoUpload
        fields = ["title", "cartegory", "popular", "typs"]

class PurchaseFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='exact')
    
    class Meta:
        model = Purchased
        fields = ['username']  
class DepositFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    
    class Meta:
        model = DepositHistory
        fields = ['name']  
class DownloadsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    
    class Meta:
        model = DownloadHistory
        fields = ['name']  
class CartFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='exact')
    
    class Meta:
        model = Cart
        fields = ['username']  

class WatchFilter(django_filters.FilterSet):
    watcher = django_filters.CharFilter(field_name='watcher', lookup_expr='exact', label="watcher")
    def __str__(self):
        return self.username
    class Meta:
        model = Onwatch
        fields = ['watcher']  
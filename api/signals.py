from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from multimedia.models import *
from Members.models import *
@receiver([post_save, post_delete], sender=VideoUpload)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('video_uploads')
@receiver([post_save, post_delete], sender=Cartegories)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('cartegory')
@receiver([post_save, post_delete], sender=videos)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('videos')
@receiver([post_save, post_delete], sender=Purchased)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('purchased')
@receiver([post_save, post_delete], sender=DepositHistory)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('deposit')
@receiver([post_save, post_delete], sender=Onwatch)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('watch')
@receiver([post_save, post_delete], sender=Review)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('review')
@receiver([post_save, post_delete], sender=Profile)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('profile')
@receiver([post_save, post_delete], sender=BettingRecords)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('betting')
@receiver([post_save, post_delete], sender=Members)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('members')
@receiver([post_save, post_delete], sender=Notification)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('notifications')from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from multimedia.models import *
@receiver([post_save, post_delete], sender=VideoUpload)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('video_uploads')
@receiver([post_save, post_delete], sender=Cartegories)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('cartegory')
@receiver([post_save, post_delete], sender=videos)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('videos')
@receiver([post_save, post_delete], sender=Purchased)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('purchased')
@receiver([post_save, post_delete], sender=DepositHistory)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('deposit')
@receiver([post_save, post_delete], sender=Onwatch)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('watch')
@receiver([post_save, post_delete], sender=Review)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('review')
@receiver([post_save, post_delete], sender=Profile)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('profile')
@receiver([post_save, post_delete], sender=BettingRecords)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('betting')
@receiver([post_save, post_delete], sender=Members)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('members')
@receiver([post_save, post_delete], sender=Notification)
def invalidate_video_cache(sender, instance, **kwargs):
    """
    Invalidate the cache for the VideoUpload model when a video is saved or deleted.
    """
    print("Cache invalidated for VideoUpload")
    cache.delete('notifications')

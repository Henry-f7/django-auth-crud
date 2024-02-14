from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deleteTime = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
        
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(pre_delete, sender=User)
    def update_delete_time(sender, instance, **kwargs):
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.deleteTime = timezone.now()
            profile.save()
        except UserProfile.DoesNotExist:
            pass

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important= models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    deletetime = models.DateTimeField(null=True, blank=True) 
    
    def __str__(self):
        return self.title + '- by ' + self.user.user.username
    
    @receiver(pre_delete, sender=UserProfile)
    def update_task_delete_time(sender, instance, **kwargs):
        # Actualizar deleteTime en las tareas relacionadas
        Task.objects.filter(user=instance).update(deleteTime=timezone.now())
    
    
    
    

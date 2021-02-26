from django.db import models

from django.conf import settings
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


#friends request models function start
from django.db import models



class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name = 'user')
    friends  = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='friends')

    def __str__(self):
        return self.user.username

    
    def add_friend(self,account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    
    
    def mutual_friend(self, account):
        if account in self.friends.all():
            return True
        return False



class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="sender")
    reciver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="reciver")
    is_active = models.BooleanField(blank=True, null=False,default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        print('heloo')
        receiver_friend_list = FriendList.objects.get(user=self.reciver)
        print(receiver_friend_list)

        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            
            if sender_friend_list:
                sender_friend_list.add_friend(self.reciver)
                self.is_active=False
                self.save()


#for message


from django.db import models


class Room(models.Model):
    name1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user11')
    name2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user12')
    is_friends = models.BooleanField(default=True)

    def __str__(self):
        return self.name1.username


class Chat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
    msg = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.msg
    
    
    


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_save(sender, instance, **kwargs):
    FriendList.objects.get_or_create(user=instance)

from django.contrib import admin




#for request send

from .models import FriendList,FriendRequest

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    # readonly_fields = ['user']

    class Meta:
        model = FriendList


admin.site.register(FriendList,FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter =['sender','reciver']
    list_display = ['sender','reciver','id','sender_id','reciver_id']
    search_fields = ['sender__username','sender__email','reciver']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest,FriendRequestAdmin)


#for message
from .models import Room, Chat

class RoomAdmin(admin.ModelAdmin):
    list_display=['name1','name2','name1_id','id']

    class Meta:
        model = Room

admin.site.register(Room,RoomAdmin)

class ChatAdmin(admin.ModelAdmin):
    list_display=['room','id']
    class Meta:
        model = Chat

admin.site.register(Chat,ChatAdmin)
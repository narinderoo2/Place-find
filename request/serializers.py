     
        
# friends request serializer start
from rest_framework import serializers
from .models import FriendRequest,FriendList,Account

class SendSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset = Account.objects.all())
    reciver = serializers.SlugRelatedField(many=False,slug_field='username',queryset=Account.objects.all())
    class Meta:
        model = FriendRequest
        fields = ('sender','reciver')



class FriendsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendList
        fields = ('friends',)



#fro message
from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    msg= serializers.CharField(required=True)
    class Meta:
        model = Chat
        fields = ('msg',)

class ShowChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields=('msg','timestamp')
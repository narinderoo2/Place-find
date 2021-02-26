from django.shortcuts import render


#request sender , cancel etc..
from django.shortcuts import render

from .models import FriendList, FriendRequest,Account
from .serializers import SendSerializer,FriendsSerializer
from .models import Room

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics,status


from rest_framework.decorators import permission_classes,authentication_classes

#only fro Account profile show

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def account_view(request,*args, **kwargs):
    context = {}
    user_id = kwargs.get('user_id')
    
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return Response({"msg":"something was wrong"},status=status.HTTP_404_NOT_FOUND)
    
    if account:
        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        friends = friend_list.friends.all()
        # context['friends'] =f"{friends}"
        if friends:

            serializer = FriendsSerializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"response":"something was wrong"},status=status.HTTP_404_NOT_FOUND)

    else:
        context['response'] = 'have not request'
    return Response(context)

        

""" any user request send 
but this condition only user send request
    in case your request is accept, so next time again friend request you can send.
    (create a profile fuction, it can decide send request or not )
    """

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def send_friend_request(request,id):
    user = request.user
    contect = {}
    try:
        receiver = Account.objects.get(pk=id)
        if receiver:
            friend_request = FriendRequest.objects.filter(sender=user,reciver=receiver)
            try :
                for ps in friend_request:
                    if ps.is_active:
                        return Response({"msg":"You alredy request send"},status=status.HTTP_200_OK)
                
                friend_request = FriendRequest(sender=user, reciver=receiver)
                friend_request.save()
                return Response({"Success":"Succes"},status=status.HTTP_201_CREATED)


            except FriendRequest.DoesNotExist:
                contect['respose'] = f" Please check user id {str(e)}" 
        else:
            return Response({"Response":"Not correct"},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        contect['response'] =  "Not correct user"
    return Response(contect)


"""first user check request of other user (receve request)

    user check all request of pending request 
    pending request is (is activve True) """
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def friend_request(request, id):
    context = {}
    user = request.user
    account = Account.objects.get(pk=id)
    if account == user:
        try:
            friend_request_show = FriendRequest.objects.filter(reciver= account, is_active=True)
            print(friend_request_show)
        except FriendRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SendSerializer(friend_request_show, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"Response":"you can't view another user friend request"},status=status.HTTP_404_NOT_FOUND)
    return Response(context)


# request accept user one time one request accept, but this field work with model id not a user id
#condition apply:- is active user, so request accept
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def accept_friend_request(request, *args, **kwargs):
    user = request.user
    contect= {}
    friend_request_id = kwargs.get("friend_request")
    if friend_request_id:
        friend_request = FriendRequest.objects.get(pk=friend_request_id)
        if friend_request.reciver == user:
            if friend_request:
                notification = friend_request.accept()
                return Response({"Response":"Accpet your friend request"},status=status.HTTP_200_OK)

                #new models data save in auto
                user1,created = Room.objects.get_or_create(name1=user, name2=friend_request.sender)
                user1.save()
                contect['succes'] = 'you can send message your frieds'

            else:
                return Response({"Response":"check your argument"},status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"Response":"Not user in your friends list"},status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"Response":"this id is not correct"},status=status.HTTP_404_NOT_FOUND)

    return Response(contect)



# you have any request of unknow user you can cancel request with the help of that's logic
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def cancel_friend_request(request,*args, **kwargs):
    user = request.user
    contect = {}
    user_id = kwargs.get("user_id")
    print(user_id)
    if user_id:
        friend_request = FriendRequest.objects.get(pk=user_id)
        if friend_request.reciver == user:
            if friend_request:
                friend_request.delete()
                return Response({"Response":"Friend request delete succesfully"},status=status.HTTP_200_OK)

            else:
                contect['response'] = "Wrong"
        else:
            return Response({"Response":"This is not your request"},status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"Error":"have not your in your list"},status=status.HTTP_404_NOT_FOUND)


    return Response(contect)


# for messaage

from django.shortcuts import render
from .models import Room,Chat
from .serializers import ChatSerializer,ShowChatSerializer
from itertools import chain

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated



@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def create_or_return_chat(request, *args, **kwargs):
    user = request.user
    payload = {}
    room_id = kwargs.get("room_id")
    if room_id:
        check_room = Room.objects.get(pk=room_id)      
        if check_room.name2 == user or check_room.name1==user:
            room = Chat(room=check_room)

            serializer = ChatSerializer(room,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors)

        else:
            payload['response']='not user is correct'
    else:
        return Response({'response':'this user is not in your list'}, status=status.HTTP_404_NOT_FOUND)
    return Response(payload)



@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def show_chat(request, *args, **kwargs):
    user = request.user
    payload = {}
    room_id = kwargs.get("room_id")
    print(room_id)
    if room_id:
        check_room = Room.objects.get(pk=room_id) 
        if check_room.name2 == user or check_room.name1==user:
            chat = Chat.objects.filter(room_id = check_room)
            serializer = ShowChatSerializer(chat,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"Response":"Your are not a friends"},status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"Response":"incorrect  room is"},status=status.HTTP_404_NOT_FOUND)

    return Response(payload)

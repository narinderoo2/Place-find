from rest_framework import serializers
from .models import facility,Account,Profile


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = facility
        fields = '__all__'



#Account serializer
class AccountSeriallizer(serializers.ModelSerializer):
    
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=Account
        fields='__all__'
        extra_kwargs={
            'password':{'write_only':True}
        }

    def save(self):
        account=Account(
            email=self.validated_data['email'],
            fullname=self.validated_data['fullname'],

        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password !=password2:
            raise serializers.ValidationError({'password':"passoword must match"})

        account.set_password(password)
        account.save()
        return account


#Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'
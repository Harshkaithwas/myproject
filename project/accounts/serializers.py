from django.core.validators import MinLengthValidator

# 
from rest_framework import serializers
# 
from accounts.models import Account, AccountProfileModel



class RegistrationSerializer(serializers.ModelSerializer):
    """ serializer used for registration """

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account

        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username = self.validated_data['username']
        )
        
        password = self.validated_data['password'] 
        password2 = self.validated_data['password2']

        if password == password2:
            account.set_password(password)
            account.save()
            return account
        else:
            raise serializers.ValidationError({'password', 'Passwords must match'})


class UserDetails(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

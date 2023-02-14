from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    #override save function to check password is equal to password2 and email is unique
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error':'p1 and p2 should be same!'})

        email = self.validated_data['email']
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'error':'Email already exist!'})

        username = self.validated_data['username']
        account = User(email=email,username=username)
        account.set_password(password)
        account.save()

        return account

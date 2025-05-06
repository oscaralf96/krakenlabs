# users/serializers.py
from rest_framework import serializers
from .models import CustomUser, Website
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    website_domain = serializers.URLField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'website_domain']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        website_domain = validated_data.pop('website_domain')
        website = Website.objects.get(domain=website_domain)

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.websites.add(website)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    website_domain = serializers.URLField()

    def validate(self, data):
        website = Website.objects.get(domain=data['website_domain'])
        user = authenticate(email=data['email'], password=data['password'])

        if user and website in user.websites.all():
            return user
        raise serializers.ValidationError("Invalid credentials or unauthorized website.")


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'name', 'domain']
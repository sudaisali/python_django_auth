from django.contrib.auth import authenticate
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_mongoengine.serializers import DocumentSerializer
from mongoengine.fields import ObjectIdField
from mongoengine.errors import DoesNotExist
from django.utils.translation import gettext_lazy as _
from .models import User

class UserSerializer(DocumentSerializer):
    #id = serializers.IntegerField(read_only=False)
    user_id = ObjectIdField(source='id')
    
    class Meta:
        model = User
        fields = ( 'id','username','email',)
        read_only_fields = ('email', )
    

class SignUpSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=120,
        min_length=5)
        
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    def validate_username(self, username):
        #TODO better username validation
        regexp = "/^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$/"
        #validate with regexp
        #check if username exists
        usr = User.objects.filter(username=username)
        if usr:
            raise serializers.ValidationError(
                _("A user is already registered with this username."))
        return username

    def validate_email(self, email):
        # Check if a already uses this email
        usr = User.objects.filter(email=email)
        if usr:
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        #TODO better password constraints (length, uppercase, lowercase, special characters, etc)
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        
        return password

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        new_user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'])
        new_user.set_password(self.cleaned_data['password1'])
        new_user.save()
        return new_user


class AuthTokenSerializer(serializers.Serializer):
    
    #username = serializers.CharField(label=_("Username"))
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    
    def validate_email(self, email):
        # email validation start by checking if the email address exists in
        # the database.
        try:
            user = User.objects.get(email=email)
        except DoesNotExist:
            raise serializers.ValidationError("No user account attached to the provided email.")
        
        self.username = user.username
        return email
        
    def validate(self, attrs):
        #username = attrs.get('username')
        username = self.username
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                
                # if not user.email_is_valid:
                #     msg = _('User account email not verified.')
                #     raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


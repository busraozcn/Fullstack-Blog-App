from rest_framework import serializers
from .models import User, Address, Geo, Company, Post, Comment, Album, Photo, Todo
from django.contrib.auth.models import User as AdminUser, Permission

class GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geo
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    geo = GeoSerializer(required=False)

    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {
            'geo': {'required': False, 'allow_null': True}
        }

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False, 'allow_null': True},
            'catchPhrase': {'required': False, 'allow_null': True},
            'bs': {'required': False, 'allow_null': True}
        }

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    company = CompanySerializer(required=False)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'address': {'required': False, 'allow_null': True},
            'company': {'required': False, 'allow_null': True},
            'name': {'required': False, 'allow_null': True},
            'username': {'required': False, 'allow_null': True},
            'email': {'required': False, 'allow_null': True},
            'phone': {'required': False, 'allow_null': True},
            'website': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        company_data = validated_data.pop('company', None)

        if address_data:
            geo_data = address_data.pop('geo', None)
            geo = Geo.objects.create(**geo_data) if geo_data else None
            address = Address.objects.create(geo=geo, **address_data)
        else:
            address = None

        company = Company.objects.create(**company_data) if company_data else None

        user = User.objects.create(address=address, company=company, **validated_data)
        return user

    def update(self, instance, validated_data):
      
        address_data = validated_data.pop('address', None)
        if address_data:
            geo_data = address_data.pop('geo', None)
            if geo_data:
                geo = instance.address.geo
                for attr, value in geo_data.items():
                    setattr(geo, attr, value)
                geo.save()
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()


        company_data = validated_data.pop('company', None)
        if company_data:
            for attr, value in company_data.items():
                setattr(instance.company, attr, value)
            instance.company.save()

     
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class PhotoSerializer(serializers.ModelSerializer):
    albumId = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), source='album')

    class Meta:
        model = Photo
        fields = ['id', 'albumId', 'title', 'url', 'thumbnailUrl']
        extra_kwargs = {
            'thumbnailUrl': {'required': False, 'allow_null': True}
        }

class AlbumSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Album
        fields = ['id', 'userId', 'title', 'photos']
        extra_kwargs = {
            'photos': {'required': False}
        }

    def create(self, validated_data):
        user = validated_data.pop('userId')
        album = Album.objects.create(userId=user, **validated_data)
        return album
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
    def create(self, validated_data):
        user = validated_data.pop('userId')
        album = Album.objects.create(userId=user, **validated_data)
        return album
        
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class AdminUserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'permissions']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        user = AdminUser.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()

        if permissions:
            perms = Permission.objects.filter(codename__in=permissions)
            user.user_permissions.set(perms)
        
        return user

    def get_permissions(self, obj):
        return obj.user_permissions.values('id', 'name', 'codename')



        
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']
   
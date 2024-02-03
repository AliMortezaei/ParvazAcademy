
from django.http import QueryDict
from pkg_resources import require
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import status

from accounts.students.models import StudentProfile
from accounts.users.models import User



class RetrieveUserMixin:

    def get(self, request, *args, **kwargs):
        return self.retrive_profile(request, *args, **kwargs)

    
    @action(methods=['get'], detail=False, url_path="profile")
    def retrive_profile(self, request, *args, **kwargs):
        user_profile = self.get_queryset()
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)


class UpdateUserMixin:

    def put(self, request, *args, **kwargs):
        return self.update_profile(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update_profile(request, *args, **kwargs)
    
        
    @action(methods=['put', 'patch'], detail=False, url_path="profile")
    def update_profile(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user_profile = self.get_queryset()
        serializer = self.get_serializer(
            data=request.data , partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.update(instance=user_profile, validated_data=serializer.data, image=request.data['image'])
        return Response(data={"detail": "successfuly"} , status=status.HTTP_200_OK)


    def update(self, instance, validated_data, image):
        user_data = validated_data.pop('full_name') if "full_name" in validated_data else None
        validated_data['image'] = image
        user = instance.user
        
        instance.city = self.check(validated_data['city'], instance.city)
        instance.gender = self.check(validated_data['gender'], instance.gender)
        instance.image = self.check(validated_data['image'], instance.image)
        instance.birthday = self.check(validated_data['birthday'], instance.birthday)
        user.full_name = self.check(user_data, user.full_name)

        instance.save()
        user.save()
        
        return True

    def check(self, validate_data, data):
        if validate_data is not None and validate_data != "":
            return validate_data
        return data
        





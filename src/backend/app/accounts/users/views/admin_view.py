from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from accounts.users.models import User, UserType
from accounts.users.serializers.admin_serializer import AdminUserSeialiser, AdminUserCreateSeialiser




class AdminUserFilter(filters.FilterSet):
    """
        filter for fields registery date (date_joined)
        and user type (student, teacher, admin) 
        and users active accounts
    """    
    date_year = filters.NumberFilter(field_name='date_joined', lookup_expr='year')
    date_month = filters.NumberFilter(field_name='date_joined', lookup_expr='month')
    date_day = filters.NumberFilter(field_name='date_joined', lookup_expr='day')


    class Meta:
        model = User
        fields = ['user_type', 'date_joined','is_active']
        
        
class AdminUserViewSet(ModelViewSet):
    
    queryset = User.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminUserFilter

    #permission_classes = [IsAdminUser]


    def  get_serializer_class(self):
        if self.action == 'create':
            return AdminUserCreateSeialiser
        else:
            return AdminUserSeialiser
    
    def perform_create(self, serializer):
        data = serializer.create_validate(serializer.data)
        self.get_queryset().model.objects.create_user(
                password=data['password'],
                email=data['email'],
                phone_number=data['phone_number'],
                full_name=data['full_name'],
                user_type=data['user_type']
        )
        

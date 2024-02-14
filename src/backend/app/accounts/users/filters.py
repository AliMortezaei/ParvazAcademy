from django_filters import rest_framework as filters

from accounts.users.models import User




class AdminUserFilter(filters.FilterSet):
    """
        filter for fields registery date (date_joined)
        and user type (student, teacher, admin) 
        and users active accounts
    """    
    date_year = filters.NumberFilter(field_name='date_joined', lookup_expr='year')
    date_month = filters.NumberFilter(field_name='date_joined', lookup_expr='month')
    date_day = filters.NumberFilter(field_name='date_joined', lookup_expr='day')
    full_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['user_type', 'date_joined','is_active']
from django_filters import rest_framework as filters

from apps.courses.models import Course



class CourseFilter(filters.FilterSet):
    category__slug = filters.CharFilter(lookup_expr='icontains', label='category')
    date_course = filters.DateTimeFromToRangeFilter(field_name='date_start')
    
    class Meta:
        model = Course
        fields = ['is_public', 'is_start']
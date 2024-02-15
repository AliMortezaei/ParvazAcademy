

from drf_spectacular.utils import OpenApiResponse,extend_schema_serializer, OpenApiExample, extend_schema



def course_list_doc():
    course_list = extend_schema_serializer(
        many=True,
        examples=[OpenApiExample(
            'CourseList_1',
            value={
                "id": 1,
                "teacher": "mortezaei",
                "category": "learn fastapi",
                "slug": "lern-fastapi",
                "is_public": True,
                "is_start": True,
                "data_start": "1402-01-14",
                "numbers": 1,
                "image": "http://image.png"
            })]
        )
    return course_list

    
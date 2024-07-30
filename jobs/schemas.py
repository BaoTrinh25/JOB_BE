from drf_yasg import openapi

job_posting_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'company': openapi.Schema(type=openapi.TYPE_INTEGER),
        'career': openapi.Schema(type=openapi.TYPE_INTEGER),
        'employmenttype': openapi.Schema(type=openapi.TYPE_INTEGER),
        'area': openapi.Schema(type=openapi.TYPE_INTEGER),
        'active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'image': openapi.Schema(type=openapi.TYPE_STRING),
        'title': openapi.Schema(type=openapi.TYPE_STRING),
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, format='int32'),
        'gender': openapi.Schema(type=openapi.TYPE_INTEGER),
        'location': openapi.Schema(type=openapi.TYPE_STRING),
        'salary': openapi.Schema(type=openapi.TYPE_INTEGER, format='int32'),
        'position': openapi.Schema(type=openapi.TYPE_STRING),
        'description': openapi.Schema(type=openapi.TYPE_STRING),
        'experience': openapi.Schema(type=openapi.TYPE_STRING),
        'reported': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'deadline': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
    },
    required=['company', 'career', 'employmenttype', 'area', 'active', 'image', 'title',
    'quantity', 'gender', 'location', 'salary', 'position', 'description', 'experience', 'reported', 'deadline']
)


create_applicant_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'position': openapi.Schema(type=openapi.TYPE_STRING),
        'salary_expectation': openapi.Schema(type=openapi.TYPE_STRING),
        'experience': openapi.Schema(type=openapi.TYPE_STRING),
        'cv': openapi.Schema(type=openapi.TYPE_STRING),
    },
)

create_employer_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'companyName': openapi.Schema(type=openapi.TYPE_STRING),
        'position': openapi.Schema(type=openapi.TYPE_STRING),
        'information': openapi.Schema(type=openapi.TYPE_STRING),
        'address': openapi.Schema(type=openapi.TYPE_STRING),
        'company_type': openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

number_application = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'num_applications': openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)
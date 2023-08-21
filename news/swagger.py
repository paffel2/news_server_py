from drf_yasg import openapi

id_body = openapi.Schema("id", type=openapi.TYPE_INTEGER)


def id_param(description):
    return openapi.Parameter(
        "id", openapi.IN_QUERY, description=description, type=openapi.TYPE_INTEGER
    )


token_param = openapi.Parameter(
    "token", openapi.IN_HEADER, description="accessing token", type=openapi.TYPE_STRING
)


def image_param(name, desc):
    return openapi.Parameter(
        name,
        openapi.IN_FORM,
        description=desc,
        type=openapi.TYPE_FILE,
    )


def id_form_param(name, desc):
    return openapi.Parameter(
        name, openapi.IN_FORM, type=openapi.TYPE_INTEGER, description=desc
    )


def text_form_param(name):
    return openapi.Parameter(name, openapi.IN_FORM, type=openapi.TYPE_STRING)


def image_form_param(name, desc):
    return openapi.Parameter(name, openapi.IN_FORM, type="image", description=desc)

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_message = ''
        
        
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_message = response.data['detail']
            else:
                error_message = ' | '.join(
                    [f"{key}: {', '.join(value) if isinstance(value, list) else str(value)}"
                     for key, value in response.data.items()]
                )
        else:
            error_message = str(response.data)

        return Response({
            'success': False,
            'error': error_message
        }, status=response.status_code)

    return Response({
        'success': False,
        'error': 'Something went wrong.'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse
from drf_standardized_errors.openapi_serializers import ValidationErrorSerializer

class CustomExceptionFormatter(ExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):

        if error_response.type == 'validation_error': 
          errors = []
          for error in error_response.errors:
            error_obj_formatted = {}
            error_serializer = ValidationErrorSerializer(error)
            error_obj = error_serializer.to_representation(error)
            error_obj_formatted['field_name'] = error_obj['attr']
            error_obj_formatted['field_error'] = error_obj['detail']
            error_obj_formatted['field_type'] = error_obj['code']
            errors.append(error_obj_formatted)
          
          return {
            "message": "Some fields are incorrect or missing.",
            "type": error_response.type,
            "detail": errors
          }

        else:
          print(error_response)
          return {
            "message": error_response.errors[0].detail,
            "type": error_response.errors[0].code,
            "detail": error_response.errors[0].attr
          }
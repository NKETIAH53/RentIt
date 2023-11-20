from rest_framework.exceptions import APIException


class ProfileNotFound(APIException):
    status_code = 404
    default_detail = 'Profile does not exist.'


class NotYourProfile(APIException):
    status_code = 403
    default_detail = 'You are not authorised to edit this profile.'

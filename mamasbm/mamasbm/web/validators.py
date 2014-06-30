import json


def update_validated_field(request, data, key):
    if key in data and data[key]:
        request.validated[key] = data[key]


def validate_required_field(request, data, key):
    if key not in data or not data[key]:
        request.errors.add('body', key, '%s is a required field.' % key)
    else:
        update_validated_field(request, data, key)


def validate_put_request(request):
    data = json.loads(request.body)
    validate_required_field(request, data, 'title')
    validate_required_field(request, data, 'send_days')


def validate_post_request(request):
    data = json.loads(request.body)
    validate_required_field(request, data, 'uuid')

    update_validated_field(request, data, 'title')
    update_validated_field(request, data, 'send_days')


def validate_delete_request(request):
    data = {'uuid': request.GET.get('uuid', None)}
    validate_required_field(request, data, 'uuid')


def validate_upload_message_profiles(request):
    data = json.loads(request.body)
    validate_required_field(request, data, 'profile_uuid')
    validate_required_field(request, data, 'name')
    validate_required_field(request, data, 'csv')

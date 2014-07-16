def update_validated_field(request, data, key):
    if key in data and data[key] is not None:
        request.validated[key] = data[key]


def validate_required_field(request, data, key):
    if key in data and data[key] is not None:
        update_validated_field(request, data, key)
    else:
        request.errors.add('body', key, '%s is a required field.' % key)


def validate_get_message(request):
    validate_required_field(request, request.GET, 'uuid')
    validate_required_field(request, request.GET, 'day')
    validate_required_field(request, request.GET, 'index')

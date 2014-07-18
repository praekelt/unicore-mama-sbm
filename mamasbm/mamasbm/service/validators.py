from datetime import datetime


def update_validated_field(request, data, key):
    if key in data and data[key] is not None:
        request.validated[key] = data[key]


def validate_required_field(request, data, key):
    if key in data and data[key] is not None:
        update_validated_field(request, data, key)
    else:
        request.errors.add(
            'body', 'RequiredFieldError', '%s is a required field.' % key)


def validate_index_or_date_field(request, data):
    has_index = has_date = False

    if 'index' in data and data['index'] is not None:
        update_validated_field(request, data, 'index')
        has_index = True

    if 'date' in data and data['date'] is not None:
        try:
            date = datetime.strptime(data['date'], "%Y%m%d").date()
            request.validated['date'] = date
            has_date = True
        except ValueError:
            request.errors.add(
                'body', 'InvalidDateError',
                '`date` must be in the format `yyyymmdd`')
            return

    if not (has_index or has_date):
        request.errors.add(
            'body', 'RequiredFieldError',
            'Either `index` or `date` is required.')


def validate_get_message(request):
    validate_required_field(request, request.GET, 'uuid')
    validate_required_field(request, request.GET, 'day')
    validate_index_or_date_field(request, request.GET)

def _validate_typeof(data, expected):
    if data == None or isinstance(data, expected):
        return data
    raise ValueError("Paramater expected a type of " + str(expected)+", but got type "+str(type(data)))


def get_int_parameter_or_default(request, param_name, _default, use_post=False):
    """
        Accesses the request data to find an int parameter.
    """
    try:
        if use_post:
            return _validate_typeof(request.data[param_name], int)
        return int(request.GET[param_name])
    except KeyError:
        return _default


def get_any_parameter_or_default(request, param_name, _default, use_post=False):
    """
        Accesses the request data to find a parameter of any type.
    """
    try:
        if use_post:
            return request.data[param_name]
        return request.GET[param_name]
    except KeyError:
        return _default


def get_parameter_or_default(request, param_name, _default, use_post=False):
    """
        Accesses the request data to find a string parameter.
    """
    try:
        if use_post:
            return _validate_typeof(request.data[param_name], str)
        return request.GET[param_name]
    except KeyError:
        return _default


def get_list_parameter_or_default(request, param_name, _default, use_post=False):
    """
        Accesses the request data to find a list parameter.
    """
    try:
        if use_post:
            return _validate_typeof(request.data[param_name], list)
        return request.GET.getlist(param_name)
    except KeyError:
        return _default


def get_optionally_list_parameter_or_default(request, param_name, _default, use_post=False):
    """
        Accesses the request data to find a string paramaeter that may or may not be a list.
        The returned data is always a list.
    """
    if use_post:
        try:
            return list(request.data[param_name])
        except KeyError:
            return _default

    param1 = get_parameter_or_default(request, param_name, _default, use_post)
    if param1 is not _default:
        return [param1]
    param2 = get_list_parameter_or_default(
        request, str(param_name) + ("[]" if not use_post else ""),
        _default, use_post)
    if param2 is not _default:
        return param2

    return _default


def get_bool_parameter_or_default(request, param_name, _default, use_post=False):
    """
        Accesses the request data to find a boolean parameter. False if it does not exist
        or if the string == 'false'. True otherwise
    """
    try:
        if use_post:
            return _validate_typeof(request.data[param_name], bool)

        val = request.GET[param_name]
        if not val:
            return False
        if str(val.lower()) == "false":
            return False
        return True
    except KeyError:
        return _default


def paginate_values(page, count, query):
    if page is None or count is None:
        return query
    off = count * page
    return query[off:off+count]


def paginate(request, query):
    page = get_int_parameter_or_default(request, "page", 1) - 1
    count = get_int_parameter_or_default(request, "size", 1e9)
    return paginate_values(page, count, query)

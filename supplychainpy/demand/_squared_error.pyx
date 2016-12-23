def sum_squared_errors_i1(squared_error: list, alpha: float, gamma: float):
        cdef double sse = 0

        for sq_e in squared_error:
            for i in sq_e:
                if i['alpha'] == alpha and i['gamma'] == gamma:
                    sse += i["squared_error"]

        return {(alpha, gamma): sse}

def sum_squared_errors_i2(squared_error: list, smoothing_parameter: float):
    cdef double sse = 0

    for sq_e in squared_error:
        for i in sq_e:
            if i['alpha'] == smoothing_parameter:
                sse += i["squared_error"]

    return {smoothing_parameter: sse}

def sum_squared_errors_i0(squared_error: list, smoothing_parameter: float):
    cdef double sse = 0
    for sq_e in squared_error:
        if sq_e['alpha'] == smoothing_parameter:
            sse += sq_e["squared_error"]
    return {smoothing_parameter: sse}
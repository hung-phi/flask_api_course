from functools import wraps


def safe_run(message, error_code):
    def error_handling(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return {'message': '{}\n{}'.format(message, e)}, error_code
        return func_wrapper
    return error_handling

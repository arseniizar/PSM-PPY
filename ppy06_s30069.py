from functools import wraps
import time

current_user = {
    'username': 'admin_user',
    'roles': ['admin', 'editor']
}


def requires_role(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if role_name not in current_user['roles']:
                raise PermissionError(f"User '{current_user['username']}' lacks '{role_name}' role.")
            print(f"[Role Check] Access granted for '{role_name}'.")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{level}: Starting {func.__name__}")
            result = func(*args, **kwargs)
            print(f"{level}: Finished {func.__name__}")
            return result

        return wrapper

    return decorator


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Timer] '{func.__name__}' took {(end - start):.4f} seconds.")
        return result

    return wrapper


@requires_role('admin')
@log("INFO")
@timer
def delete_post(post_id):
    return f"Deleted post {post_id}"


@requires_role('editor')
@log("DEBUG")
@timer
def edit_post(post_id):
    return f"Edited post {post_id}"


@requires_role('viewer')
@log("WARNING")
@timer
def view_post(post_id):
    return f"Viewed post {post_id}"


def main():
    try:
        print(delete_post(42))
    except PermissionError as e:
        print(e)

    try:
        print(edit_post(7))
    except PermissionError as e:
        print(e)

    try:
        print(view_post(99))
    except PermissionError as e:
        print(e)


if __name__ == "__main__":
    main()

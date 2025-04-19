from functools import wraps
import time

current_user = {
    'username': 'admin_user',
    'roles': ['admin', 'editor']
}

posts = [
    {'id': 1, 'content': 'Welcome to the blog!'},
    {'id': 2, 'content': 'Here is a second example post.'}
]

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

@requires_role('editor')
@log("INFO")
@timer
def add_post(content):
    new_id = max(post['id'] for post in posts) + 1 if posts else 1
    posts.append({'id': new_id, 'content': content})
    return f"Added post {new_id}"

@requires_role('admin')
@log("INFO")
@timer
def delete_post(post_id):
    for i, post in enumerate(posts):
        if post['id'] == post_id:
            posts.pop(i)
            return f"Deleted post {post_id}"
    return f"Post {post_id} not found"

@requires_role('editor')
@log("DEBUG")
@timer
def edit_post(post_id, new_content):
    for post in posts:
        if post['id'] == post_id:
            post['content'] = new_content
            return f"Edited post {post_id}"
    return f"Post {post_id} not found"

@requires_role('viewer')
@log("WARNING")
@timer
def view_post(post_id):
    for post in posts:
        if post['id'] == post_id:
            return f"Post {post_id}: {post['content']}"
    return f"Post {post_id} not found"

@requires_role('viewer')
@log("WARNING")
@timer
def view_all_posts():
    if not posts:
        return "No posts available"
    lines = [f"{post['id']}: {post['content']}" for post in posts]
    return "\n".join(lines)

def switch_role():
    available = ['admin', 'editor', 'viewer']
    print("Available roles:", ", ".join(available))
    choice = input("Enter role to switch to: ").strip().lower()
    if choice in available:
        current_user['roles'] = [choice]
        print(f"Switched current user to role '{choice}'.")
    else:
        print("Invalid role.")

def main():
    actions = {
        '1': ('Add Post', add_post),
        '2': ('Delete Post', delete_post),
        '3': ('Edit Post', edit_post),
        '4': ('View Post', view_post),
        '5': ('View All Posts', view_all_posts),
        '6': ('Switch Role', switch_role),
        'q': ('Quit', None)
    }

    while True:
        print("\nAvailable Actions:")
        for key, (desc, _) in actions.items():
            print(f"{key}: {desc}")
        choice = input("Choose an action (1-6/q): ").strip().lower()

        if choice == 'q':
            print("Exiting...")
            break
        elif choice in actions:
            action = actions[choice][1]
            try:
                if choice == '1':
                    content = input("Enter post content: ").strip()
                    print(action(content))
                elif choice == '2':
                    pid = int(input("Enter Post ID to delete: ").strip())
                    print(action(pid))
                elif choice == '3':
                    pid = int(input("Enter Post ID to edit: ").strip())
                    new_content = input("Enter new content: ").strip()
                    print(action(pid, new_content))
                elif choice == '4':
                    pid = int(input("Enter Post ID to view: ").strip())
                    print(action(pid))
                elif choice == '5':
                    print(action())
                elif choice == '6':
                    action()
            except PermissionError as e:
                print(e)
            except ValueError:
                print("Invalid input. Post ID must be an integer.")
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

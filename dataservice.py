import json

def get_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

def add_blog_post(blog_post):
    blog_posts = get_blog_posts()
    id = blog_posts[-1]['id'] + 1 if blog_posts else 1
    blog_post["id"] = id
    blog_posts.append(blog_post)
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

def delete_blog_post(post_id):
    blog_posts = get_blog_posts()
    updated_posts = [post for post in blog_posts if post['id'] != post_id]
    with open('blog_posts.json', 'w') as file:
        json.dump(updated_posts, file, indent=4)


def validate_post_form(form):

    title = form.get('title', '').strip()
    content = form.get('content', '').strip()
    author = form.get('author', '').strip()

    if not title or not content or not author:
        return None, "All fields are required."

    return {'title': title, 'content': content, 'author': author}, None

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
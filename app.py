import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        with open('blog_posts.json', 'r') as file:
            blog_posts = json.load(file)

        new_post = {
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)

        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    updated_posts = [post for post in blog_posts if post['id'] != post_id]

    with open('blog_posts.json', 'w') as file:
        json.dump(updated_posts, file, indent=4)

    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    for post in blog_posts:
        if post.get('id') == post_id:
            return post
    return None


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    post = next((post for post in blog_posts if post.get('id') == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

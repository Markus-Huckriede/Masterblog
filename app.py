import json
from flask import Flask, render_template, request, redirect, url_for
import os

import dataservice

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = dataservice.get_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')

        new_post = {
            'author': author,
            'title': title,
            'content': content
        }
        dataservice.add_blog_post(new_post)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    dataservice.delete_blog_post(post_id)
    return redirect(url_for('index'))


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
        post['author'] = request.form.get('author')

        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)



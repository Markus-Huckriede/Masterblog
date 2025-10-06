import json
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
import dataservice

app = Flask(__name__)

@app.route('/')
def index():
    blog_posts = dataservice.get_blog_posts()

    for post in blog_posts:
        if 'updated_at' in post:
            dt = datetime.fromisoformat(post['updated_at'])
        else:
            dt = datetime.fromisoformat(post['created_at'])
        post['display_date'] = dt.strftime("%d/%m/%Y %H:%M")

    blog_posts.sort(
        key=lambda p: datetime.fromisoformat(p.get('updated_at') or p.get('created_at')),
        reverse=True
    )

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        post_data, error = dataservice.validate_post_form(request.form)
        if error:
            return render_template('add.html', error=error, form=request.form)

        post_data['created_at'] = datetime.now().isoformat()
        dataservice.add_blog_post(post_data)
        return redirect(url_for('index'))

    return render_template('add.html', form={})



@app.route('/delete/<int:post_id>')
def delete(post_id):
    dataservice.delete_blog_post(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = dataservice.get_blog_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)  # Post finden

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post_data, error = dataservice.validate_post_form(request.form)
        if error:
            return render_template('update.html', post=post, error=error)

        post.update(post_data)
        post['updated_at'] = datetime.now().isoformat()

        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)



if __name__ == "__main__":
    app.run(debug=True, port=5001)

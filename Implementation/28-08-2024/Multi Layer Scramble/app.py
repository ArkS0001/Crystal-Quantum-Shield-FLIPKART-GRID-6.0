# from flask import Flask, jsonify
# import request

# app = Flask(__name__)

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     # Call the function in request.py to fetch data from an external API
#     response = request.fetch_data()
#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# from flask import Flask, jsonify, request as flask_request

# app = Flask(__name__)

# # Sample data
# posts = [
#     {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
#     {"id": 2, "title": "Second Post", "content": "This is the content of the second post."},
#     {"id": 3, "title": "Third Post", "content": "This is the content of the third post."},
# ]

# # Route to fetch all posts
# @app.route('/api/posts', methods=['GET'])
# def get_posts():
#     return jsonify(posts)

# # Route to fetch a single post by ID
# @app.route('/api/posts/<int:post_id>', methods=['GET'])
# def get_post(post_id):
#     post = next((post for post in posts if post["id"] == post_id), None)
#     if post:
#         return jsonify(post)
#     else:
#         return jsonify({"error": "Post not found"}), 404

# # Route to create a new post
# @app.route('/api/posts', methods=['POST'])
# def create_post():
#     if not flask_request.json or not 'title' in flask_request.json:
#         return jsonify({"error": "Invalid input"}), 400
    
#     new_post = {
#         "id": posts[-1]["id"] + 1 if posts else 1,
#         "title": flask_request.json["title"],
#         "content": flask_request.json.get("content", "")
#     }
#     posts.append(new_post)
#     return jsonify(new_post), 201

# # Route to update an existing post
# @app.route('/api/posts/<int:post_id>', methods=['PUT'])
# def update_post(post_id):
#     post = next((post for post in posts if post["id"] == post_id), None)
#     if not post:
#         return jsonify({"error": "Post not found"}), 404
    
#     post["title"] = flask_request.json.get("title", post["title"])
#     post["content"] = flask_request.json.get("content", post["content"])
#     return jsonify(post)

# # Route to delete a post
# @app.route('/api/posts/<int:post_id>', methods=['DELETE'])
# def delete_post(post_id):
#     post = next((post for post in posts if post["id"] == post_id), None)
#     if not post:
#         return jsonify({"error": "Post not found"}), 404
    
#     posts.remove(post)
#     return jsonify({"result": "Post deleted"})

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, jsonify

app = Flask(__name__)

# Simple route to return some static data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello, this is some static data!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


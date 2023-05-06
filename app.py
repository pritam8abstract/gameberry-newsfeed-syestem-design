import time
from collections import defaultdict

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.following = set()
        self.posts = []

class Post:
    def __init__(self, content, user):
        self.content = content
        self.user = user
        self.timestamp = time.time()
        self.score = 0
        self.comments = []

class Comment:
    def __init__(self, content, user):
        self.content = content
        self.user = user
        self.timestamp = time.time()
        self.score = 0

def time_ago(timestamp):
    diff = int(time.time() - timestamp)
    if diff < 60:
        return f"{diff}s ago"
    elif diff < 3600:
        return f"{diff // 60}m ago"
    else:
        return f"{diff // 3600}h ago"

def display_post(post):
    print(f"{post.user.username}: {post.content} ({time_ago(post.timestamp)})")
    print(f"Score: {post.score}")
    print("Comments:")
    for comment in post.comments:
        display_comment(comment, 1)

def display_comment(comment, indent):
    print(" " * indent * 2, end="")
    print(f"{comment.user.username}: {comment.content} ({time_ago(comment.timestamp)})")
    print(" " * indent * 2, end="")
    print(f"Score: {comment.score}")

users = {}
session = None

def signup(username, password):
    if username in users:
        print("Username already exists.")
    else:
        users[username] = User(username, password)
        print(f"User {username} created.")

def login(username, password):
    global session
    if username not in users or users[username].password != password:
        print("Invalid username or password.")
    else:
        session = users[username]
        print(f"Logged in as {username}.")

def post(content):
    if session:
        post = Post(content, session)
        session.posts.append(post)
        print("Posted.")
    else:
        print("Please log in first.")

def follow(username):
    if session:
        if username not in users:
            print("User not found.")
        else:
            session.following.add(users[username])
            print(f"Following {username}.")
    else:
        print("Please log in first.")

def reply(post_id, content):
    if session:
        if post_id >= len(session.posts):
            print("Post not found.")
        else:
            post = session.posts[post_id]
            comment = Comment(content, session)
            post.comments.append(comment)
            print("Comment added.")
    else:
        print("Please log in first.")

def upvote_downvote(post_id, vote):
    if session:
        if post_id >= len(session.posts):
            print("Post not found.")
        else:
            post = session.posts[post_id]
            post.score += vote
            print("Vote counted.")
    else:
        print("Please log in first.")

def show_news_feed(sort_by):
    if session:
        posts = []
        for user in session.following:
            posts.extend(user.posts)
        if sort_by == "followed":
            posts.sort(key=lambda p: (p.user in session.following, p.timestamp), reverse=True)
        elif sort_by == "score":
            posts.sort(key=lambda p: p.score, reverse=True)
        elif sort_by == "comments":
            posts.sort(key=lambda p: len(p.comments), reverse=True)
        else: 
            posts.sort(key=lambda p: p.timestamp, reverse=True)

        for post in posts:
            display_post(post)
    else:
        print("Please log in first.")

while True:
    command = input("Enter command: ").split()

    if command[0] == "signup":
        signup(command[1], command[2])
    elif command[0] == "login":
        login(command[1], command[2])
    elif command[0] == "post":
        post(" ".join(command[1:]))
    elif command[0] == "follow":
        follow(command[1])
    elif command[0] == "reply":
        reply(int(command[1]), " ".join(command[2:]))
    elif command[0] == "upvote":
        upvote_downvote(int(command[1]), 1)
    elif command[0] == "downvote":
        upvote_downvote(int(command[1]), -1)
    elif command[0] == "shownewsfeed":
        show_news_feed(command[1])
    elif command[0] == "exit":
        break
    else:
        print("Invalid command.")

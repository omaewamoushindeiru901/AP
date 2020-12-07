from flask import Flask

app = Flask(__name__)

student_id = 10


@app.route(f'/api/v1/hello-world-{student_id}')
def hello_world():
    return f"Hello World {student_id}"


if __name__ == 'main':
    app.run()

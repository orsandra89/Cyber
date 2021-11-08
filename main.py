from flask import Flask, render_template
from strawberry.flask.views import GraphQLView
from api.schema import schema

app=Flask(__name__)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

@app.route('/')
def home():
    return render_template("index.html") 


if __name__ == "__main__":
    app.run(debug=True)
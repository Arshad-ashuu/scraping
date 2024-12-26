from flask import Flask, render_template, request, session
from flask_session import Session
import content_aggregator
import requests

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getparts", methods=["POST", "GET"])
def getparts():
    if request.method == "GET":
        return render_template("error.html", message="Request Method GET Not Allowed, Please Enter Part Name in previous Page")

    # Get form data
    category = request.form.get("Category_Option")
    part_name = request.form.get("partname")

    # Input validation
    if not category or not part_name:
        return render_template("error.html", message="Category and Part Name must be provided.")

    allowed_categories = ["Computer Parts", "Mobiles", "Headphones", "Furniture", "Shoes","cloths"]
    if category not in allowed_categories:
        return render_template("error.html", message=f"Invalid category: {category}. Allowed categories are: {', '.join(allowed_categories)}")

    session["category"] = category
    session["part_name"] = part_name

    try:
        # Fetch part details
        part_list = content_aggregator.get_part_details(session["part_name"], session["category"])

        if not part_list:
            return render_template("error.html", message=f'No Part Named "{session["part_name"]}" Found')

        return render_template("parts.html", part_list=part_list)

    except Exception as e:
        # Log the exception (you can use logging module here)
        return render_template("error.html", message=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)

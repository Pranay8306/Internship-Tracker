from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
CSV_FILE = "internships.csv"

def load_internships():
    internships = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                internships.append(row)
    return internships

@app.route("/")
def index():
    internships = load_internships()
    return render_template("index.html", internships=internships)

@app.route("/add", methods=["POST"])
def add_internship():
    company = request.form["company"]
    role = request.form["role"]
    eligibility = request.form["eligibility"]
    stipend = request.form["stipend"]
    deadline = request.form["deadline"]
    status = request.form["status"]

    new_entry = {
        "Company": company,
        "Role": role,
        "Eligibility": eligibility,
        "Stipend": stipend,
        "Deadline": deadline,
        "Status": status
    }

    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=new_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_entry)

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_internship():
    index_to_delete = int(request.form["index"])
    internships = load_internships()

    if 0 <= index_to_delete < len(internships):
        internships.pop(index_to_delete)

        fieldnames = ["Company", "Role", "Eligibility", "Stipend", "Deadline", "Status"]
        with open(CSV_FILE, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(internships)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

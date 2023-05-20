from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = b'_5#y2L"asdfsafsg346345F4Q8z\n\xec]/'

STUDENTS = [
    {"name": "Ran", "phone": "050-4445555"},
    {"name": "Or", "phone": "053-9995555"},
    {"name": "Binyamin", "phone": "052-43345555"}]


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")
        fav_color = request.form.get("fav_col")
        print(f"user:{user}, password:{password}")
        if user == "elad" and password == "123":
            session["logged_in_user"] = user
            session["fav_color"] = fav_color
            return redirect("/students")
        else:
            message = "Error in login"
    return render_template("index.html", message=message)

@app.route("/logout",methods=["POST"])
def logout():
    session.pop("logged_in_user", None)
    session.pop("color", None)
    return redirect("/")

@app.route("/students")
def students():
    if not session.get("logged_in_user"):
        return redirect("/")
    return render_template("students.html", students=STUDENTS, logged_in_user=session.get("logged_in_user"), color=session.get("fav_color"))


@app.route("/search")
def search():
    search = request.args.get("search")
    phone = request.args.get("phone")
    new_list = []
    print(f"search-{search} phone-{phone}")
    for student in STUDENTS:
        print(f"student-{student}")
        if search in student["name"] and phone in student["phone"]:
            new_list.append(student)
    print(f"new_list-{new_list}")
    return render_template("students.html", students=new_list, logged_in_user=session.get("logged_in_user"))


@app.errorhandler(404)
def page_not_found(error):
    # Custom logic for handling 404 errors
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=9000)

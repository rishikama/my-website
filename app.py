print("STARTING APP")
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rishikama@23048",
    database="nutriguide"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        try:

            fullname = request.form['fullname']
            username = request.form['username']
            email = request.form['email']
            phone = request.form['phone']
            age = request.form['age']
            gender = request.form['gender']
            password = request.form['password']

            sql = """
            INSERT INTO users
            (fullname, username, email, phone, age, gender, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                fullname,
                username,
                email,
                phone,
                age,
                gender,
                password
            )

            cursor.execute(sql, values)
            db.commit()

            return "Registration Successful!"

        except Exception as e:
            return f"Database Error: {str(e)}"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        sql = """
        SELECT * FROM users
        WHERE username=%s AND password=%s
        """

        cursor.execute(sql, (username, password))

        user = cursor.fetchone()

        if user:
            return redirect('/dashboard')

        else:
            return "Invalid Username or Password"
    return render_template('login.html')
@app.route('/bmi', methods=['GET', 'POST'])
def bmi():

    bmi_value = None

    if request.method == 'POST':

        weight = float(request.form['weight'])
        height = float(request.form['height'])

        bmi_value = round(weight / (height * height), 2)

    return render_template(
        'bmi.html',
        bmi=bmi_value
    )
print("ABOUT TO RUN FLASK")
@app.route('/bmr', methods=['GET', 'POST'])
def bmr():

    bmr_value = None

    if request.method == 'POST':

        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        gender = request.form['gender']

        if gender == 'male':
            bmr_value = round(
                (10 * weight) + (6.25 * height) - (5 * age) + 5,
                2
            )
        else:
            bmr_value = round(
                (10 * weight) + (6.25 * height) - (5 * age) - 161,
                2
            )

    return render_template(
        'bmr.html',
        bmr=bmr_value
    )
@app.route('/calories', methods=['GET', 'POST'])
def calories():

    calorie_value = None

    if request.method == 'POST':

        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        gender = request.form['gender']
        activity = float(request.form['activity'])

        if gender == 'male':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

        calorie_value = round(bmr * activity, 2)

    return render_template(
        'calories.html',
        calories=calorie_value
    )
@app.route('/goal', methods=['GET', 'POST'])
def goal():

    target = None
    message = ""

    if request.method == 'POST':

        calories = float(request.form['calories'])
        goal = request.form['goal']

        if goal == 'loss':
            target = calories - 500
            message = "Recommended for gradual weight loss."

        elif goal == 'gain':
            target = calories + 500
            message = "Recommended for healthy weight gain."

        else:
            target = calories
            message = "Recommended for weight maintenance."

    return render_template(
        'goal.html',
        target=target,
        message=message
    )
@app.route('/water', methods=['GET', 'POST'])
def water():

    water_value = None

    if request.method == 'POST':

        weight = float(request.form['weight'])

        water_value = round(weight * 0.033, 2)

    return render_template(
        'water.html',
        water=water_value
    )
@app.route('/recipes', methods=['GET', 'POST'])
def recipes():

    recipes_list = []

    if request.method == 'POST':

        goal = request.form['goal']

        sql = """
        SELECT * FROM recipes
        WHERE goal=%s
        """

        cursor.execute(sql, (goal,))
        recipes_list = cursor.fetchall()

    return render_template(
        'recipes.html',
        recipes=recipes_list
    )
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if request.method == 'POST':

        username = request.form['username']
        age = request.form['age']
        gender = request.form['gender']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        goal = request.form['goal']

        height_m = height / 100

        bmi = round(weight / (height_m * height_m), 2)

        if gender.lower() == 'male':
            bmr = round((10 * weight) + (6.25 * height) - (5 * int(age)) + 5, 2)
        else:
            bmr = round((10 * weight) + (6.25 * height) - (5 * int(age)) - 161, 2)

        calories = round(bmr * 1.55, 2)
        water = round(weight * 0.033, 2)

        sql = """
        INSERT INTO user_health
        (username, age, gender, weight, height,
        bmi, bmr, calories, water, goal)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            username,
            age,
            gender,
            weight,
            height,
            bmi,
            bmr,
            calories,
            water,
            goal
        )

        cursor.execute(sql, values)
        db.commit()

        return "Profile Saved Successfully!"

    return render_template('profile.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/logout')
def logout():
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

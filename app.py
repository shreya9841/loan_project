from flask import Flask, render_template_string, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# In-memory user "database" for demonstration
users_db = {}

# ============== Base CSS for consistent styling ==============
base_css = """
<style>
body {
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
    height: 100vh;
    background: linear-gradient(-45deg, #c9d6ff, #e2e2e2, #a8edea, #fed6e3);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.container {
    max-width: 450px;
    background: rgba(255, 255, 255, 0.9);
    padding: 25px 20px;
    margin: 60px auto;
    border-radius: 10px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    backdrop-filter: blur(5px);
}
h2 {
    text-align: center;
    color: #004080;
}
form {
    display: flex;
    flex-direction: column;
}
input, select {
    padding: 10px;
    margin: 8px 0;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
}
button {
    padding: 10px;
    background-color: #004080;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    margin-top: 10px;
    transition: background-color 0.3s, transform 0.2s;
}
button:hover {
    background-color: #003366;
    transform: scale(1.03);
}
.flash {
    text-align: center;
    padding: 10px;
    margin-bottom: 10px;
}
.flash.error { background-color: #f8d7da; color: #721c24; }
.flash.success { background-color: #d4edda; color: #155724; }
a { color: #004080; text-decoration: none; }
a:hover { text-decoration: underline; }
ul {
    list-style: none;
    padding-left: 0;
}
ul li::before {
    content: "✅ ";
    color: #004080;
}
</style>
"""


# ============== Templates ==============

register_html = base_css + """
<!DOCTYPE html>
<html>
<head>
    <title>Register | Loan Approval Prediction System</title>
    <style>
        body, html {
            height: 100%;
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
        }
        body {
            background: url('https://images.unsplash.com/photo-1521791055366-0d553872125f?auto=format&fit=crop&w=1740&q=80') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(5px);
            border-radius: 12px;
            padding: 30px 25px;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            text-align: center;
        }
        h1 {
            color: #004080;
            margin-bottom: 5px;
        }
        h3 {
            color: #555;
            margin-top: 0;
            font-weight: normal;
        }
        form {
            display: flex;
            flex-direction: column;
            margin-top: 15px;
        }
        input {
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 14px;
        }
        button {
            padding: 12px;
            background-color: #004080;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
            transition: background-color 0.3s, transform 0.2s;
        }
        button:hover {
            background-color: #003060;
            transform: scale(1.03);
        }
        .flash {
            text-align: center;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .flash.error { background-color: #f8d7da; color: #721c24; }
        .flash.success { background-color: #d4edda; color: #155724; }
        a { color: #004080; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Register</h1>
        <h3>Create your account to predict your loan approval</h3>
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, msg in messages %}
              <div class="flash {{ category }}">{{ msg }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        <form method="POST">
            <input type="text" name="username" placeholder="Enter Username" required>
            <input type="password" name="password" placeholder="Enter Password" required>
            <input type="password" name="confirm_password" placeholder="Confirm Password" required>
            <button type="submit">Register</button>
        </form>
        <p style="margin-top:12px;">
            Already have an account?
            <a href="/login">Login here</a>
        </p>
    </div>
</body>
</html>
"""


login_html = base_css + """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login | Loan Approval Prediction System</title>
    <style>
        * { box-sizing: border-box; }
        body, html {
            height: 100%;
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
             background: url('/static/image.png')  no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .overlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 0;
        }
        .container {
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 40px 30px;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            color: #fff;
            text-align: center;
        }
        h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        h3 {
            font-weight: 400;
            margin-bottom: 25px;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        input {
            padding: 14px;
            margin: 8px 0;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.8);
        }
        button {
            padding: 14px;
            margin-top: 15px;
            background-color: #004080;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        button:hover {
            background-color: #003060;
            transform: scale(1.03);
        }
        .flash {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            font-weight: 600;
        }
        .flash.error { background-color: #f8d7da; color: #721c24; }
        .flash.success { background-color: #d4edda; color: #155724; }
        a {
            color: #fff;
            text-decoration: underline;
            margin-top: 15px;
            display: inline-block;
        }
        a:hover { text-decoration: none; }
    </style>
</head>
<body>
<div class="overlay"></div>
<div class="container">
    <h1>Login</h1>
    <h3>Access your Loan Approval Dashboard</h3>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, msg in messages %}
          <div class="flash {{ category }}">{{ msg }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    <form method="POST">
        <input type="text" name="username" placeholder="🔑 Username" required>
        <input type="password" name="password" placeholder="🔒 Password" required>
        <button type="submit">Login</button>
    </form>
    <a href="/register">Don't have an account? Register here</a>
</div>
</body>
</html>
"""



home_html = base_css + """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard | Loan Approval Prediction System</title>
    <style>
        body, html {
            height: 100%;
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: url('/static/image2.png') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .overlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 0;
        }
        .container {
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(12px);
            border-radius: 15px;
            padding: 30px 25px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            text-align: center;
            color: #ffffff;
        }
        h2 {
            margin-top: 0;
            font-size: 28px;
            color: #ffffff;
        }
        p.quote {
            font-size: 16px;
            font-style: italic;
            margin: 20px 0;
            color: #e0e0e0;
        }
        a {
            display: inline-block;
            margin: 10px;
            padding: 12px 20px;
            background-color: #004080;
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-size: 16px;
            transition: background-color 0.3s, transform 0.2s;
        }
        a:hover {
            background-color: #003060;
            transform: scale(1.05);
        }
        .flash {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            font-weight: 600;
        }
        .flash.error { background-color: #f8d7da; color: #721c24; }
        .flash.success { background-color: #d4edda; color: #155724; }
    </style>
</head>
<body>
<div class="overlay"></div>
<div class="container">
    <h2>Welcome, {{ username }}!</h2>
    <p class="quote">"Predict today, secure your tomorrow."</p>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, msg in messages %}
          <div class="flash {{ category }}">{{ msg }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    <a href="/loan">Fill up to Predict</a>
    <a href="/logout">Logout</a>
</div>
</body>
</html>
"""

loan_form_html = base_css + """
<div class="container">
    <h2>Loan Prediction Form</h2>
    {% if prediction_result %}
      <div class="flash success">{{ prediction_result|safe }}</div>
    {% endif %}
    <form method="POST">
        <input type="text" name="name" placeholder="Full Name" required>
        <input type="number" name="age" placeholder="Age" required>
        <select name="married" required>
            <option value="">Married?</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
        </select>
        <select name="dependent" required>
            <option value="">Dependents</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3+">3+</option>
        </select>
        <select name="education" required>
            <option value="">Education</option>
            <option value="Graduate">Graduate</option>
            <option value="Not Graduate">Not Graduate</option>
        </select>
        <input type="number" name="applicant_income" placeholder="Applicant Income" required>
        <input type="number" name="coapplicant_income" placeholder="Co-applicant Income" required>
        <input type="number" name="loan_amount" placeholder="Loan Amount" required>
        <input type="number" name="loan_amount_term" placeholder="Loan Term (Months)" required>
        <select name="credit_history" required>
            <option value="">Credit History</option>
            <option value="1">Good</option>
            <option value="0">Bad/No</option>
        </select>
        <select name="property_area" required>
            <option value="">Property Area</option>
            <option value="Urban">Urban</option>
            <option value="Semiurban">Semiurban</option>
            <option value="Rural">Rural</option>
        </select>
        <button type="submit">Submit</button>
    </form>
    <p style="text-align:center; margin-top:10px;">
        <a href="/">Back to Dashboard</a>
    </p>
</div>
"""

# ============== Routes ==============

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        confirm_password = request.form.get('confirm_password').strip()

        if not username or not password or not confirm_password:
            flash("Please fill in all fields.", "error")
        elif password != confirm_password:
            flash("Passwords do not match.", "error")
        elif username in users_db:
            flash("Username already exists.", "error")
        else:
            users_db[username] = password
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
    return render_template_string(register_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if username in users_db and users_db[username] == password:
            session['username'] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "error")
    return render_template_string(login_html)

@app.route('/')
def home():
    if 'username' not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))
    return render_template_string(home_html, username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/loan', methods=['GET', 'POST'])
def loan_form():
    if 'username' not in session:
        flash("Please log in to access the loan Prediction form.", "error")
        return redirect(url_for('login'))

    prediction_result = None
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        married = request.form.get('married')
        dependent = request.form.get('dependent')
        education = request.form.get('education')
        applicant_income = request.form.get('applicant_income')
        coapplicant_income = request.form.get('coapplicant_income')
        loan_amount = request.form.get('loan_amount')
        loan_amount_term = request.form.get('loan_amount_term')
        credit_history = request.form.get('credit_history')
        property_area = request.form.get('property_area')

        prediction_result = f"Hello {name}, your loan Prediction is under review."
                             
    return render_template_string(loan_form_html, prediction_result=prediction_result)

# ============== Run App ==============
if __name__ == "__main__":
    app.run(debug=True)

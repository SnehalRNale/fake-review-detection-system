from flask import Flask, render_template, request, redirect, url_for, session, flash
from tensorflow.keras.models import load_model
import pickle
from prediction import predict
import os
from flask_pymongo import PyMongo

# Initialize Flask app and configure a secret key for session management
app = Flask(__name__)
app.secret_key = os.urandom(24)

# mongo connection string
app.config['MONGO_URI'] = 'mongodb://localhost:27017/contact-us-db'
mongo = PyMongo(app)

# Load model and tokenizer
model = load_model("LSTM.h5")
tokenizer = pickle.load(open("Data\\tokenized\\tokenizer.pkl", "rb"))

# Main page 
@app.route("/")
def main_page():
    return render_template("index.html")

# register page
@app.route('/register')
def register_page():
    return render_template('register.html')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
      
        if username == 'admin' and password == 'password':
            session['username'] = username  # Store username in session
            session['logged_in'] = True
            flash('Logged in successfully!', 'success')  # Flash a success message
            return redirect(url_for("main_page"))  # Redirect to the index page
        else:
            flash('Invalid username or password!', 'error')  # Flash an error message

    return render_template('login.html')


#Review page
@app.route("/review")
def review_page():
    if not session.get('logged_in'):
        print("User not logged in, redirecting to main page")  # Debugging log
        return redirect(url_for("main_page"))
    return render_template("review.html")

# Handle review submission
@app.route("/submit", methods=["POST"])
def submit_review():
    if not session.get('logged_in'):
        return redirect(url_for("main_page"))

    text = request.form.get("review")
    if text == "":
        result = "No review entered..."
    else:
        result = predict(text, model=model, tokenizer=tokenizer)
    
    return render_template("review.html", result=result)

#resources page
@app.route('/resources')
def resources_page():
    return render_template('resources.html')

@app.route('/thank_you')
def thank_you():
    return 'Thank you for contacting us!'

#contact us page
@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Insert data into MongoDB
        contact_info = {
            'name': name,
            'email': email,
            'message': message
        }
        mongo.db.contacts.insert_one(contact_info)  # Save to 'contacts' collection
        
        return redirect(url_for('thank_you'))
    return render_template('contact.html')

#dashboard page
@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# about us page
@app.route('/about')
def about_page():
    return render_template('about.html')
# Logout route
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("main_page"))

if __name__ == "__main__":
    app.run(debug=True)

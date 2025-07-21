from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'cle_secrete_pour_session'

# Fonction de connexion à la base de données
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Mets ton mot de passe ici
        database='bibliothéque'
    )

# Utilisateurs fictifs
users = {
    'admin': '1234',
    'user1': 'azerty'
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form.get('id')
        mot_de_passe = request.form.get('mot_de_passe')

        if identifiant in users and users[identifiant] == mot_de_passe:
            session['user'] = identifiant
            return redirect(url_for('dashboard'))
        else:
            flash('Identifiant ou mot de passe incorrect.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Veuillez vous connecter.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Déconnexion réussie.')
    return redirect(url_for('login'))

@app.route('/louer', methods=['GET', 'POST'])
def louer():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nom = request.form['nom_client']
        email = request.form['email_client']
        tel = request.form['tel_client']
        date_loc = request.form['date_location']
        date_ret = request.form['date_retour']
        prix = request.form['prix_location']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO locations 
            (id_admin,nom_client, email_client, tel_client, date_location, date_retour, prix_location, returned)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
        """, (1,nom, email, tel, date_loc, date_ret, prix, False))

        conn.commit()
        location_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return redirect(url_for('recu', location_id=location_id))

    return render_template('louer.html')

@app.route('/recu/<int:location_id>')
def recu(location_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
    rental = cursor.fetchone()

    book = {
        'title': 'Livre Loué',
        'author': 'Auteur inconnu'
    }

    cursor.close()
    conn.close()

    return render_template('reçu.html', rental={
        'borrower_name': rental['nom_client'],
        'rental_date': rental['date_location'],
        'return_date': rental['date_retour'],
        'returned': rental['returned']
    }, book=book)

if __name__ == '__main__':
    app.run(debug=True)

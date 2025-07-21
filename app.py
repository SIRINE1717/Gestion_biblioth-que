<<<<<<< HEAD
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

@app.route('/dashbrd')
def dashboard():
    if 'user' not in session:
        flash('Veuilloaez vous connecter.', 'warning')
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
=======
from flask import Flask,render_template,request,redirect,session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


app=Flask(__name__)
app.secret_key = "une_chaine_complexe_à_garder_secrete"

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bibliotheque"
) 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form)
        Identifiant = request.form.get("Identifiant")
        motdepasse = request.form["mot_de_passe"]
        cur = db.cursor(dictionary=True)

        # Vérifie si l'identifiant ET le mot de passe sont corrects
        cur.execute("SELECT * FROM admin WHERE Identifiant = %s AND MOT_DE_PASSE = %s", (Identifiant, motdepasse))
        admin = cur.fetchone()

        if admin:
            session["admin"] = admin["IDENTIFIANT"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", erreur="Identifiant ou mot de passe incorrect")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/")

    cur = db.cursor(dictionary=True)

    mot_cle = request.args.get("recherche")  # récupère ce que l'utilisateur tape

    if mot_cle:
        cur.execute("""
            SELECT * FROM livre 
            WHERE TITRE LIKE %s OR AUTEUR LIKE %s
        """, (f"%{mot_cle}%", f"%{mot_cle}%"))
    else:
        cur.execute("SELECT * FROM livre")

    livres = cur.fetchall()
    return render_template("dashboard.html", admin=session["admin"], livres=livres)

@app.route("/supprimer_livre/<int:id>")
def supprimer_livre(id):
    cur = db.cursor()
    cur.execute("DELETE FROM livre WHERE ID_LIVRE = %s", (id,))
    db.commit()
    return redirect("/dashboard")

@app.route("/modifier_livre/<int:id>", methods=["GET", "POST"])
def modifier_livre(id):
    cur = db.cursor(dictionary=True)

    if request.method == "POST":
        titre = request.form["titre"]
        auteur = request.form["auteur"]
        categorie = request.form["categorie"]
        description = request.form["description"]
        statu = request.form["statu"]
        photo = request.files["photo"]
        Anne_ecriture = request.form["Anne_ecriture"] 
        Anne_publication = request.form["Anne_publication"] 
        cur.execute("""
            UPDATE livre 
            SET titre=%s, auteur=%s, ID_CATEGORIES=%s, description=%s, STATU_=%s, photo=%s ,Anne_ecritue=%s,Anne_publication=%s
            WHERE id=%s
        """, (titre, auteur, ID_CATEGORIES, description, statu, photo,Anne_ecritue,Anne_publication, id))
        
        db.commit()
        return redirect("/dashboard")
        
    # Si GET → afficher le formulaire avec les anciennes infos
    cur.execute("SELECT * FROM livre WHERE ID_LIVRE = %s", (id,))
    livre = cur.fetchone()
    return render_template("modifier.html", livre=livre)
@app.route("/ajouter_livre", methods=["GET", "POST"])
def ajouter():
    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":
        titre = request.form.get("titre")
        auteur = request.form.get("auteur")
        id_categorie = request.form.get("categorie")
        description = request.form.get("description")
        statu_ = request.form.get("statu")
        prix = request.form.get("prix")
        anne_ecriture = request.form.get("anne_ecriture")
        annee_publication = request.form.get("annee_publication")

        photo_file = request.files["photo"]
        filename = secure_filename(photo_file.filename)
        photo_file.save(os.path.join("static", filename))
        cur = db.cursor()
        cur.execute("""
            INSERT INTO livre (session["admin_id"],titre, auteur, categorie, description, statu_, photo,Prix,ANNE_ECRITURE,Anne_publication)
            VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)
        """, ( session["admin_id"], titre, auteur, id_categorie, description, statu_, fiename,prix,anne_ecriture,Annee_publication))

        db.commit()
        return redirect("/dashboard")

    return render_template("Ajouter.html")
@app.route("/louer/<int:id>", methods=["GET", "POST"])
def louer_livre(id):
    if "admin" not in session:
        return redirect("/")

    cur = db.cursor(dictionary=True)

    if request.method == "POST":
        nom_client = request.form["nom"]
        email = request.form["email"]
        telephone = request.form["telephone"]
        date_location = request.form["date_location"]
        date_retour = request.form["date_retour"]
        prix_par_jour = float(request.form["prix_par_jour"])

        # Calcul automatique du prix total
        from datetime import datetime
        d1 = datetime.strptime(date_location, "%Y-%m-%d")
        d2 = datetime.strptime(date_retour, "%Y-%m-%d")
        nb_jours = (d2 - d1).days
        prix_total = nb_jours * prix_par_jour

        # Insérer dans la table location
        cur.execute("""
            INSERT INTO location (ID_ADMIN, NOM_CLIENT, TELEPHONE, EMAIL, DATE_LOCATION, DATE_RETOUR, PRIX)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            session["admin_id"], nom_client, telephone, email,
            date_location, date_retour, prix_total
        ))

        # Mettre à jour le statut du livre
        cur.execute("UPDATE livre SET STATU_ = %s WHERE ID_LIVRE = %s", ("Loué", id))

        db.commit()
        return redirect("/dashboard")

    # Si GET : afficher les infos du livre
    cur.execute("SELECT * FROM livre WHERE ID_LIVRE = %s", (id,))
    livre = cur.fetchone()

    return render_template("louer.html", livre=livre)



#===========


if __name__ == "__main__":
  app.run(debug=True)
>>>>>>> 25addac9586818101bf5a17585a4a7a2c0f5da3d

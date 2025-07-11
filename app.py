from flask import Flask, render_template

app = Flask(__name__)

# Route de base → dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/modifier_livre')
def modifier_livre():
    livre = {
        'id': 1,
        'titre': 'Le Livre Test',
        'auteur': 'Auteur Exemple',
        'annee': 2021,
        'exemplaires': 5,
        'image': None
    }
    return render_template('modifier_livre.html', livre=livre)

@app.route('/historique')
def historique():
    locations = [
        {
            'id': 1,
            'titre_livre': 'Le Livre Test',
            'nom_locataire': 'Ali',
            'date_location': '2025-07-10',
            'date_retour': '2025-07-20',
            'statut': 'Retourné'
        },
        {
            'id': 2,
            'titre_livre': 'Un autre livre',
            'nom_locataire': 'Fatima',
            'date_location': '2025-07-01',
            'date_retour': '2025-07-15',
            'statut': 'En cours'
        }
    ]
    return render_template('historique.html', locations=locations)

if __name__ == '__main__':
    app.run(debug=True)

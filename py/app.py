from flask import Flask, request, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Page HTML principale

@app.route('/run', methods=['POST'])
def run_script():
    # Récupérer les fichiers téléchargés
    elu_file = request.files['file_elu']
    wash_file = request.files['file_wash']

    # Lire les fichiers CSV avec pandas
    data_elu = pd.read_csv(elu_file, delimiter=';')
    data_wash = pd.read_csv(wash_file, delimiter=';')

    # Nettoyer les données
    elu_volume = pd.to_numeric(data_elu.iloc[2:, 0].str.replace(',', '.'), errors='coerce')
    elu_absorbance = pd.to_numeric(data_elu.iloc[2:, 1].str.replace(',', '.'), errors='coerce')

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.plot(elu_volume, elu_absorbance, marker='', linestyle='-', color='blue', label='Elution')
    plt.title("Courbes d'absorbance - Elution")
    plt.xlabel("Volume d'élution (ml)")
    plt.ylabel("Absorbance (mAU)")
    plt.legend()
    plt.grid(True)

    # Sauvegarder l'image dans un flux mémoire
    output = io.BytesIO()
    plt.savefig(output, format='png')
    output.seek(0)

    # Retourner l'image générée
    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

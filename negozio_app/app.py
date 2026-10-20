from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chiave_segreta_per_i_messaggi'  # Necessario per i messaggi di notifica

# Configurazione della connessione al database MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='negozio_inventario'
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM prodotti ORDER BY id DESC')
    prodotti = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', prodotti=prodotti)

@app.route('/aggiungi', methods=['POST'])
def aggiungi_prodotto():
    codice = request.form['codice_a_barre']
    nome = request.form['nome']
    descrizione = request.form['descrizione']
    prezzo = request.form['prezzo']
    quantita = request.form['quantita']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO prodotti (codice_a_barre, nome, descrizione, prezzo, quantita) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (codice, nome, descrizione, prezzo, quantita))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Prodotto aggiunto con successo!', 'success')
    except mysql.connector.Error as err:
        flash(f'Errore durante il salvataggio (possibile codice a barrette duplicato): {err}', 'danger')

    return redirect(url_for('index'))

@app.route('/elimina/<int:id>', methods=['POST'])
def elimina_prodotto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM prodotti WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Prodotto eliminato con successo!', 'warning')
    except mysql.connector.Error as err:
        flash(f'Errore durante l\'eliminazione: {err}', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
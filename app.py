
from flask import Flask,  redirect, url_for,request, render_template
import sqlite3
import hashlib

app = Flask(__name__)


# rýchly úvod do HTML elementov:
# <h1> ...text... </h1>, alebo <h2>             - heading - nadpisy
# <p> ...text... </p>                           - paragraf (normálny text)
# <a href="www.---.com"> ...text...></a>        - odkaz (v rámci textu)
# <button> ...text... </button>                 - tlačidlo s textom


# Pripojenie k databáze
def pripoj_db():
    try:
        conn = sqlite3.connect("kurzy.db")
        return conn
    except sqlite3.Error:
        return None  # Ak sa nepodarí pripojiť, vráti None

@app.route('/')
def index():
    return '''
        <h1>Výber z databázy</h1>
        <ul class="navbar">
        <li><a href="/registracia_trenera">Registrácia nového trénera</a></li>
        <li><a href="/registracia_kurzu"><button>Registrácia nového kurzu</button></a></li>
        <li><a href="/treneri_a_kurz"><button>Výpis všetkých trénerov a ich kurzov</button></a></li>
        <li><a href="/kurzy"><button>Výpis všetkých kurzov</button></a></li>
        <li><a href="/miesta"><button>Výpis všetkých miest </button></a></li>
        <li><a href="/capacita"><button>Výpis súčtu maximálnej kapacity všetkých kurzov na P</button></a></li>
        </ul>
        

        <style>
        .navbar{
        list-style-type: none;
        

        }
        h1{
        font-family: "Afacad Flux", sans-serif;
        font-weight:700;
        font-size:200px;
        }
        .navbar li{
        margin: 0 5 8 0;
        display: inline;
        float: left;
        padding:15px;
        background-color: #04AA6D;
        }
        a{
        text-decoration:none;
        display: block;
        padding: 5px;
        color:black;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
        }
        :hover li{
            background-color:rgb(2, 118, 75);
        }

        </style>
    '''




@app.route('/registracia_kurzu', methods=['GET'])
def registracia_kurzu():
    return '''
        <h1>Registrácia Kurzu</h1>
        <form action="/registracia_kurzu" method="post">
            <label>Nazov kurzu:</label><br>
            <input type="text" name="nazov" required><br><br>

            <label>Typ Sportu:</label><br>
            <input type="text" name="typ_sport" required><br><br>

            <label>Maximalny pocet ucastikov:</label><br>
            <input type="text" name="max_poc_uc" required><br><br>

            <label>ID Trenera:</label><br>
            <input type="number" name="id_tre" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>

        <style>
            

            button {
                border: none;
                background-color: white;
                color:black;
                padding: 16px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border: 2px solid #04AA6D;
                font-family: "Afacad Flux", sans-serif;
                font-weight:600; 
            }
            button:hover {
                background-color: #04AA6D;
                color: white;
            }
        </style>
    
    '''



def affine_encrypt(text, key_a, key_b):
  
    
    key_a = 5
    
   
    key_b = 8
    
    result = ""
    
    for char in text:
        
        if char.isalpha():
            
            is_upper = char.isupper()
            char = char.upper()
            
            
            x = ord(char) - ord('A')
            
           
            encrypted_value = (key_a * x + key_b) % 26
            
            
            encrypted_char = chr(encrypted_value + ord('A'))
            
            
            if not is_upper:
                encrypted_char = encrypted_char.lower()
                
            result += encrypted_char
        else:
            
            result += char
    
    return result

# API ENDPOINT NA SPRACOVANIE REGISTRÁCIE. Mapuje sa na mená elementov z formulára z predošlého requestu (pomocou request.form[...])
# Pozor - metóda je POST
@app.route('/registracia_kurzu', methods=['POST'])
def registracia_kurza():
    nazov = affine_encrypt(request.form['nazov'], 5, 8)
    typ = affine_encrypt(request.form['typ_sport'], 5, 8)
    capacita = request.form['max_poc_uc']
    id_trenera = request.form['id_tre']
    

    # Zápis do databázy
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Kurzy (Nazov_kurzu, Typ_sportu, Max_pocet_ucastnikov, ID_trenera) VALUES (?, ?, ?, ?)", 
                   (nazov, typ, capacita, id_trenera))
    conn.commit()
    conn.close()

    # Hlásenie o úspešnej registrácii
    return '''
        <h2>Tréner bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''







@app.route('/registracia_trenera', methods=['GET'])
def registracia_form():
    return '''
        <h2>Registrácia trénera</h2>
        <form action="/registracia_trenera" method="post">
            <label>Meno:</label><br>
            <input type="text" name="meno" required><br><br>

            <label>Priezvisko:</label><br>
            <input type="text" name="priezvisko" required><br><br>

            <label>Špecializácia:</label><br>
            <input type="text" name="specializacia" required><br><br>

            <label>Telefón:</label><br>
            <input type="text" name="telefon" required><br><br>

            <label>Heslo:</label><br>
            <input type="password" name="heslo" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>
    '''


# API ENDPOINT NA SPRACOVANIE REGISTRÁCIE. Mapuje sa na mená elementov z formulára z predošlého requestu (pomocou request.form[...])
# Pozor - metóda je POST
@app.route('/registracia_trenera', methods=['POST'])
def registracia_trenera():
    meno = request.form['meno']
    priezvisko = request.form['priezvisko']
    specializacia = request.form['specializacia']
    telefon = request.form['telefon']
    heslo = request.form['heslo']

    # Hashovanie hesla
    heslo_hash = hashlib.sha256(heslo.encode()).hexdigest()

    # Zápis do databázy
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Treneri (Meno, Priezvisko, Specializacia, Telefon, Heslo) VALUES (?, ?, ?, ?, ?)", 
                   (meno, priezvisko, specializacia, telefon, heslo_hash))
    conn.commit()
    conn.close()

    # Hlásenie o úspešnej registrácii
    return '''
        <h2>Tréner bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''



@app.route('/kurzy')  
def zobraz_kurzy():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()

    conn.close()

    return render_template("kurzy.html", kurzy = kurzy)




@app.route('/miesta')  
def zobraz_miesta():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Miesta")
    miesta = cursor.fetchall()

    conn.close()

    vystup = """
    <h2>Zoznam miest:</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Názov miesta</th>
            <th>Adresa</th>
        </tr>

         <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
  font-family: "Afacad Flux", sans-serif;
  font-weight:600;
}
</style>
    """

    for miesto in miesta:
        vystup += f"<tr><td>{miesto[0]}</td><td>{miesto[1]}</td><td>{miesto[2]}</td></tr>"

    vystup += "</table>"
    vystup += '<br><a href="/"><button>Späť</button></a>'
    return vystup



# PODSTRÁNKA NA ZOBRAZENIE TRÉNEROV
@app.route('/treneri_a_kurz')  # API endpoint
def zobraz_trenerov_kurz():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM VSETCI_TRENERI_A_ICH_KURZY")
    kurzy = cursor.fetchall()

    conn.close()

    # Hlavička tabuľky (prispôsob podľa štruktúry tabuľky v DB)
    vystup = """
    <h2>Zoznam kurzov:</h2>
    <table border="1">
        <tr>
            <th>ID Trenera</th>
            <th>Meno Trenera</th>
            <th>Názov kurzu</th>
        </tr>


         <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
  font-family: "Afacad Flux", sans-serif;
  font-weight:600;
}
</style>
    """

    # Naplnenie tabuľky dátami
    for trener in kurzy:
        vystup += f"<tr><td>{trener[0]}</td><td>{trener[1]}</td><td>{trener[2]}</td></tr>"

    vystup += "</table>"  # Uzavrieme tabuľku
    vystup += '<br><a href="/"><button>Späť</button></a>'  # Tlačidlo na návrat
    return vystup


@app.route('/capacita')  # API endpoint
def zobraz_capacitu():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(Max_pocet_ucastnikov) FROM Kurzy WHERE Nazov_kurzu LIKE 'P%'")
    capacita = cursor.fetchall()

    conn.close()

    # Hlavička tabuľky (prispôsob podľa štruktúry tabuľky v DB)
    vystup = """
    <h2>Zoznam kurzov:</h2>
    <table border="1">
        <tr>
            <th>Suma</th>
            
        </tr>


        <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
}
</style>
    """

    # Naplnenie tabuľky dátami
    for cap in capacita:
        vystup += f"<tr><td>{cap[0]}</td></tr>"

    vystup += "</table>"  # Uzavrieme tabuľku
    vystup += '<br><a href="/"><button>Späť</button></a>'  # Tlačidlo na návrat
    return vystup


@app.route('/404')
def zobraz_error():
    return '''
    <h1>ERROR 404 :(</h1>
    <p>Požadovaná stránka neexistuje alebo sa vyskytla chyba pri načítaní databázy.</p>
    <br><a href="/"><button>Späť</button></a>
    <style>
        h1 { color: red; }
        button {
            border: none;
            background-color: white;
            color: black;
            padding: 16px 32px;
            font-size: 16px;
            border: 2px solid #04AA6D;
            cursor: pointer;
            font-family: "Afacad Flux", sans-serif;
            font-weight:450;
        }
        button:hover {
            background-color: #04AA6D;
            color: white;
            font-family: "Afacad Flux", sans-serif;
            font-weight:450;
        }
    </style>
    '''
    vystup += '<br><a href="/"><button>Späť</button></a>'  
    return vystup


if __name__ == '__main__':
    app.run(debug=True)



from flask import Flask,  redirect, url_for,request
import sqlite3
import hashlib

app = Flask(__name__)


# rýchly úvod do HTML elementov:
# <h1> ...text... </h1>, alebo <h2>             - heading - nadpisy
# <p> ...text... </p>                           - paragraf (normálny text)
# <a href="www.---.com"> ...text...></a>        - odkaz (v rámci textu)
# <button> ...text... </button>                 - tlačidlo s textom


# Pripojenie k databáze
def pripoj_db():
    try:
        conn = sqlite3.connect("kurzy.db")
        return conn
    except sqlite3.Error:
        return None  # Ak sa nepodarí pripojiť, vráti None


@app.route('/')  # API endpoint
def index():
    # Úvodná homepage s dvoma tlačidami ako ODKAZMI na svoje stránky - volanie API nedpointu
    return '''
        <h1>Výber z databázy</h1>
        <ul class="navbar">
        <li><a href="/registracia_trenera">Registrácia nového trénera</a></li>
        <li><a href="/registracia_kurzu"><button>Registrácia nového kurzu</button></a></li>
        <li><a href="/treneri_a_kurz"><button>Výpis všetkých trénerov a ich kurzov</button></a></li>
        <li><a href="/kurzy"><button>Výpis všetkých kurzov</button></a></li>
        <li><a href="/miesta"><button>Výpis všetkých miest </button></a></li>
        <li><a href="/capacita"><button>Výpis súčtu maximálnej kapacity všetkých kurzov na P</button></a></li>
        </ul>
        

        <style>
        .navbar{
        list-style-type: none;
        

        }
        h1{
        font-family: "Afacad Flux", sans-serif;
        font-weight:700;
        font-size:200px;
        }
        .navbar li{
        margin: 0 5 8 0;
        display: inline;
        float: left;
        padding:15px;
        background-color: #04AA6D;
        }
        a{
        text-decoration:none;
        display: block;
        padding: 5px;
        color:black;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
        }
        :hover li{
            background-color:rgb(2, 118, 75);
        }

        </style>
    '''





@app.route('/registracia_kurzu', methods=['GET'])
def registracia_kurzu():
    return '''
        <h1>Registrácia Kurzu</h1>
        <form action="/registracia_kurzu" method="post">
            <label>Nazov kurzu:</label><br>
            <input type="text" name="nazov" required><br><br>

            <label>Typ Sportu:</label><br>
            <input type="text" name="typ_sport" required><br><br>

            <label>Maximalny pocet ucastikov:</label><br>
            <input type="text" name="max_poc_uc" required><br><br>

            <label>ID Trenera:</label><br>
            <input type="number" name="id_tre" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>

        <style>
            

            button {
                border: none;
                background-color: white;
                color:black;
                padding: 16px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border: 2px solid #04AA6D;
                font-family: "Afacad Flux", sans-serif;
                font-weight:600; 
            }
            button:hover {
                background-color: #04AA6D;
                color: white;
            }
        </style>
    
    '''



def affine_encrypt(text, key_a, key_b):
  
    
    key_a = 5
    
   
    key_b = 8
    
    result = ""
    
    for char in text:
        
        if char.isalpha():
            
            is_upper = char.isupper()
            char = char.upper()
            
            
            x = ord(char) - ord('A')
            
           
            encrypted_value = (key_a * x + key_b) % 26
            
            
            encrypted_char = chr(encrypted_value + ord('A'))
            
            
            if not is_upper:
                encrypted_char = encrypted_char.lower()
                
            result += encrypted_char
        else:
            
            result += char
    
    return result

# API ENDPOINT NA SPRACOVANIE REGISTRÁCIE. Mapuje sa na mená elementov z formulára z predošlého requestu (pomocou request.form[...])
# Pozor - metóda je POST
@app.route('/registracia_kurzu', methods=['POST'])
def registracia_kurza():
    nazov = affine_encrypt(request.form['nazov'], 5, 8)
    typ = affine_encrypt(request.form['typ_sport'], 5, 8)
    capacita = request.form['max_poc_uc']
    id_trenera = request.form['id_tre']
    

    # Zápis do databázy
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Kurzy (Nazov_kurzu, Typ_sportu, Max_pocet_ucastnikov, ID_trenera) VALUES (?, ?, ?, ?)", 
                   (nazov, typ, capacita, id_trenera))
    conn.commit()
    conn.close()

    # Hlásenie o úspešnej registrácii
    return '''
        <h2>Tréner bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''







@app.route('/registracia_trenera', methods=['GET'])
def registracia_form():
    return '''
        <h2>Registrácia trénera</h2>
        <form action="/registracia_trenera" method="post">
            <label>Meno:</label><br>
            <input type="text" name="meno" required><br><br>

            <label>Priezvisko:</label><br>
            <input type="text" name="priezvisko" required><br><br>

            <label>Špecializácia:</label><br>
            <input type="text" name="specializacia" required><br><br>

            <label>Telefón:</label><br>
            <input type="text" name="telefon" required><br><br>

            <label>Heslo:</label><br>
            <input type="password" name="heslo" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>
    '''


# API ENDPOINT NA SPRACOVANIE REGISTRÁCIE. Mapuje sa na mená elementov z formulára z predošlého requestu (pomocou request.form[...])
# Pozor - metóda je POST
@app.route('/registracia_trenera', methods=['POST'])
def registracia_trenera():
    meno = request.form['meno']
    priezvisko = request.form['priezvisko']
    specializacia = request.form['specializacia']
    telefon = request.form['telefon']
    heslo = request.form['heslo']

    # Hashovanie hesla
    heslo_hash = hashlib.sha256(heslo.encode()).hexdigest()

    # Zápis do databázy
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Treneri (Meno, Priezvisko, Specializacia, Telefon, Heslo) VALUES (?, ?, ?, ?, ?)", 
                   (meno, priezvisko, specializacia, telefon, heslo_hash))
    conn.commit()
    conn.close()

    # Hlásenie o úspešnej registrácii
    return '''
        <h2>Tréner bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''



@app.route('/kurzy')  
def zobraz_kurzy():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()

    conn.close()

    # Hlavička tabuľky (prispôsob podľa štruktúry tabuľky v DB)
    vystup = """
    <h2>Zoznam kurzov:</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Názov kurzu</th>
            
        </tr>


    <style>
     table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
        
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
        
}


button:hover {
  background-color: #04AA6D;
  color: white;
}
</style>
    """

    # Naplnenie tabuľky dátami
    for kurz in kurzy:
        vystup += f"<tr><td>{kurz[0]}</td><td>{kurz[1]}</td></tr>"

    vystup += "</table>"  # Uzavrieme tabuľku
    vystup += '<br><a href="/"><button>Späť</button></a>'  # Tlačidlo na návrat
    return vystup




@app.route('/miesta')  
def zobraz_miesta():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Miesta")
    miesta = cursor.fetchall()

    conn.close()

    vystup = """
    <h2>Zoznam miest:</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Názov miesta</th>
            <th>Adresa</th>
        </tr>

         <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
  font-family: "Afacad Flux", sans-serif;
  font-weight:600;
}
</style>
    """

    for miesto in miesta:
        vystup += f"<tr><td>{miesto[0]}</td><td>{miesto[1]}</td><td>{miesto[2]}</td></tr>"

    vystup += "</table>"
    vystup += '<br><a href="/"><button>Späť</button></a>'
    return vystup



# PODSTRÁNKA NA ZOBRAZENIE TRÉNEROV
@app.route('/treneri_a_kurz')  # API endpoint
def zobraz_trenerov_kurz():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM VSETCI_TRENERI_A_ICH_KURZY")
    kurzy = cursor.fetchall()

    conn.close()

    # Hlavička tabuľky (prispôsob podľa štruktúry tabuľky v DB)
    vystup = """
    <h2>Zoznam kurzov:</h2>
    <table border="1">
        <tr>
            <th>ID Trenera</th>
            <th>Meno Trenera</th>
            <th>Názov kurzu</th>
        </tr>


         <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
  font-family: "Afacad Flux", sans-serif;
  font-weight:600;
}
</style>
    """

    # Naplnenie tabuľky dátami
    for trener in kurzy:
        vystup += f"<tr><td>{trener[0]}</td><td>{trener[1]}</td><td>{trener[2]}</td></tr>"

    vystup += "</table>"  # Uzavrieme tabuľku
    vystup += '<br><a href="/"><button>Späť</button></a>'  # Tlačidlo na návrat
    return vystup


@app.route('/capacita')  # API endpoint
def zobraz_capacitu():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(Max_pocet_ucastnikov) FROM Kurzy WHERE Nazov_kurzu LIKE 'P%'")
    capacita = cursor.fetchall()

    conn.close()

    # Hlavička tabuľky (prispôsob podľa štruktúry tabuľky v DB)
    vystup = """
    <h2>Zoznam kurzov:</h2>
    <table border="1">
        <tr>
            <th>Suma</th>
            
        </tr>


        <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
}
</style>
    """

    # Naplnenie tabuľky dátami
    for cap in capacita:
        vystup += f"<tr><td>{cap[0]}</td></tr>"

    vystup += "</table>"  # Uzavrieme tabuľku
    vystup += '<br><a href="/"><button>Späť</button></a>'  # Tlačidlo na návrat
    return vystup


@app.route('/404')
def zobraz_error():
    return '''
    <h1>ERROR 404 :(</h1>
    <p>Požadovaná stránka neexistuje alebo sa vyskytla chyba pri načítaní databázy.</p>
    <br><a href="/"><button>Späť</button></a>
    <style>
        h1 { color: red; }
        button {
            border: none;
            background-color: white;
            color: black;
            padding: 16px 32px;
            font-size: 16px;
            border: 2px solid #04AA6D;
            cursor: pointer;
            font-family: "Afacad Flux", sans-serif;
            font-weight:450;
        }
        button:hover {
            background-color: #04AA6D;
            color: white;
            font-family: "Afacad Flux", sans-serif;
            font-weight:450;
        }
    </style>
    '''
    vystup += '<br><a href="/"><button>Späť</button></a>'  
    return vystup


if __name__ == '__main__':
    app.run(debug=True)



# Aplikáciu spustíte, keď do konzoly napíšete "python app.py"
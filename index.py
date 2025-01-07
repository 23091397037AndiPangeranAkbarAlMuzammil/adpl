from flask import Flask, render_template, request, redirect, url_for, session
import mariadb
from sistem_pakar import SistemPakar, gejala, penyakit


app = Flask(__name__)
app.secret_key = "your_secret_key"

# Koneksi ke database
def get_db_connection():
    # Pastikan kode di dalam fungsi ini diindentasikan dengan benar
    conn = mariadb.connect(
        user="cekkejiwaan_functiongo",
        password="1cf1c0d99219c097b5e58c142e75bbe1a61a9f71",    # Ganti dengan password yang sesuai
        host="vwisn.h.filess.io",       # Ganti dengan host jika berbeda
        database="cekkejiwaan_functiongo"  # Ganti dengan nama database yang sesuai
    )
    return conn

def save_to_db(username, umur, gender):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query untuk menyimpan data pengguna
    query = "INSERT INTO users (username, umur, gender) VALUES (%s, %s, %s)"
    values = (username, umur, gender)
    
    try:
        cursor.execute(query, values)
        conn.commit()  # Menyimpan perubahan
        
        # Ambil user_id yang baru saja dimasukkan
        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchone()[0]
        
        # Simpan user_id dalam sesi
        session["user_id"] = user_id
        print(f"Data berhasil disimpan! User ID: {user_id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()  # Menutup cursor
        conn.close()    # Menutup koneksi
        
        
# Fungsi untuk menyimpan hasil diagnosa ke dalam database
def save_diagnosis_to_db(user_id, penyakit_kode, certainty_factor):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ambil nama penyakit berdasarkan kode penyakit
    penyakit_nama = penyakit.get(penyakit_kode, "Penyakit Tidak Dikenal")

    # Mengubah certainty factor menjadi persentase
    certainty_factor_persen = certainty_factor * 100

    # Query untuk menyimpan nama penyakit dan certainty factor
    query = "INSERT INTO diagnosa (user_id, penyakit, persentase_kemungkinan) VALUES (%s, %s, %s)"

    values = (user_id, penyakit_nama, certainty_factor_persen)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("Hasil diagnosa berhasil disimpan!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()  # Menutup cursor
        conn.close()    # Menutup koneksi



# Halaman login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        umur = request.form["age"]
        gender = request.form["gender"]
        # Simpan ke sesi untuk referensi
        session["username"] = username
        session["age"] = umur
        session["gender"] = gender
        print(f"Username: {username}, Umur: {umur}, Gender: {gender}")
        
        # Ambil user_id setelah menyimpan data pengguna
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()
        if user_id:
            session["user_id"] = user_id[0]  # Simpan user_id di sesi
        conn.close()
        
        save_to_db(username, umur, gender)
        
        return redirect(url_for('diagnosa'))
    return render_template('login.html')
    
    
# Halaman diagnosa
@app.route('/diagnosa', methods=['GET', 'POST'])
def diagnosa():
    if request.method == 'POST':
        kondisi_teramati = {
            k: float(v) for k, v in request.form.items() if v  # Hanya ambil nilai yang dipilih
        }

        if not kondisi_teramati:  # Jika tidak ada input yang valid
            return render_template('diagnosa.html', gejala=gejala, error="Silakan pilih tingkat kepastian untuk setidaknya satu gejala.")
        
        sp = SistemPakar()
        # Tambahkan aturan ke sistem pakar
        # Menambahkan aturan diagnostik sesuai dengan yang ada di sistem_pakar.py
        sp.tambahkan_aturan(["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G16"], "P01", 0.81)
        sp.tambahkan_aturan(["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G15", "G16", "G18"], "P01", 0.79)
        sp.tambahkan_aturan(["G02", "G08", "G09", "G10", "G11", "G12", "G13", "G14"], "P02", 0.85)
        sp.tambahkan_aturan(["G02", "G17", "G18", "G19", "G20", "G23", "G24", "G26"], "P03", 0.93)
        sp.tambahkan_aturan(["G03", "G16", "G18", "G20", "G24", "G25"], "P03", 0.90)
        sp.tambahkan_aturan(["G03", "G17", "G19", "G20", "G24"], "P03", 0.96)
        sp.tambahkan_aturan(["G03", "G18", "G20", "G24", "G25"], "P03", 0.92)
        sp.tambahkan_aturan(["G02", "G05", "G07", "G15", "G16", "G18", "G20", "G21", "G23", "G26"], "P04", 0.78)
        sp.tambahkan_aturan(["G02", "G05", "G07", "G15", "G16", "G24", "G26"], "P04", 0.83)
        
        # Contoh aturan
        hasil = sp.diagnosa(kondisi_teramati)
        session["hasil"] = hasil

        # Simpan hasil ke database jika ada user_id
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for('login'))

        for penyakit_kode, certainty_factor in hasil.items():
            save_diagnosis_to_db(user_id, penyakit_kode, certainty_factor)

        return redirect(url_for("hasil"))
    return render_template('diagnosa.html', gejala=gejala)



# Halaman hasil diagnosa
@app.route("/hasil", methods=["GET"])
def hasil():
    hasil = session.get("hasil", {})
    if not hasil:
        return redirect(url_for("login"))
    return render_template("hasil.html", hasil=hasil, penyakit=penyakit)


if __name__ == "__main__":
    app.run(debug=True)

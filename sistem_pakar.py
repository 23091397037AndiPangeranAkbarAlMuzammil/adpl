class SistemPakar:
    def __init__(self):
        self.aturan = []  # Daftar untuk menyimpan aturan yang didefinisikan
        self.cf_hipotesis = {}  # Dictionary untuk menyimpan nilai CF untuk setiap hipotesis penyakit

    def tambahkan_aturan(self, kondisi, hipotesis, cf):
        """Menambahkan aturan baru ke sistem pakar."""
        self.aturan.append((kondisi, hipotesis, cf))

    def perbarui_cf(self, hipotesis, cf):
        """Memperbarui nilai CF untuk hipotesis."""
        if hipotesis not in self.cf_hipotesis:
            self.cf_hipotesis[hipotesis] = cf
        else:
            self.cf_hipotesis[hipotesis] = self.kombinasi_cf(self.cf_hipotesis[hipotesis], cf)

    def kombinasi_cf(self, cf1, cf2):
        """Menggabungkan dua nilai CF."""
        if cf1 * cf2 >= 0:
            cf_terkombinasi = cf1 + cf2 * (1 - abs(cf1))
        else:
            cf_terkombinasi = (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))
        return cf_terkombinasi

    def diagnosa(self, kondisi_teramati):
        """Mendiagnosa berdasarkan kondisi yang diamati."""
        self.cf_hipotesis = {}  # Reset hasil sebelumnya
        for kondisi, hipotesis, cf in self.aturan:
            min_cf = min(kondisi_teramati.get(k, 0) for k in kondisi)
            if min_cf > 0:
                self.perbarui_cf(hipotesis, min_cf * cf)
        return self.cf_hipotesis


# Inisialisasi Sistem Pakar
sp = SistemPakar()

# Definisi gejala
gejala = {
    "G01": "Perubahan Nafsu Makan",
    "G02": "Gangguan Tidur",
    "G03": "Bicara/Bergerak Lebih Lambat",
    "G04": "Kehilangan Kepercayaan Diri",
    "G05": "Merasa bersalah pada diri sendiri",
    "G06": "Berniat menyakiti diri sendiri / bunuh diri",
    "G07": "Sering Merasa Sedih",
    "G08": "Dada berdebar",
    "G09": "Sulit bernafas",
    "G10": "Merasa tercekik",
    "G11": "Nyeri dan sesak di dada",
    "G12": "Mual dan gangguan perut",
    "G13": "Pusing atau sakit kepala",
    "G14": "Rasa takut dan khawatir berlebih",
    "G15": "Mudah tersinggung/curiga",
    "G16": "Sulit konsentrasi",
    "G17": "Mendengar atau melihat yang tidak ada (halusinasi)",
    "G18": "Kurang bersosialisasi",
    "G19": "Yakin terhadap sesuatu yang tidak nyata (Delusi)",
    "G20": "Bicara yang tidak masuk akal",
    "G21": "Terlalu percaya diri",
    "G22": "Bicara cepat dan berganti-ganti topik",
    "G23": "Gelisah dan mudah marah",
    "G24": "Penurunan kemampuan berperilaku",
    "G25": "Diam membisu/ekspresi datar",
    "G26": "Senang berlebih"
}

# Definisi penyakit
penyakit = {
    "P01": "Gangguan Depresi",
    "P02": "Gangguan Kecemasan",
    "P03": "Skizofrenia",
    "P04": "Gangguan Bipolar"
}

# Aturan-aturan diagnostik
sp.tambahkan_aturan(["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G16"], "P01", 0.81)
sp.tambahkan_aturan(["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G15", "G16", "G18"], "P01", 0.79)
sp.tambahkan_aturan(["G02", "G08", "G09", "G10", "G11", "G12", "G13", "G14"], "P02", 0.85)
sp.tambahkan_aturan(["G02", "G17", "G18", "G19", "G20", "G23", "G24", "G26"], "P03", 0.93)
sp.tambahkan_aturan(["G03", "G16", "G18", "G20", "G24", "G25"], "P03", 0.90)
sp.tambahkan_aturan(["G03", "G17", "G19", "G20", "G24"], "P03", 0.96)
sp.tambahkan_aturan(["G03", "G18", "G20", "G24", "G25"], "P03", 0.92)
sp.tambahkan_aturan(["G02", "G05", "G07", "G15", "G16", "G18", "G20", "G21", "G23", "G26"], "P04", 0.78)
sp.tambahkan_aturan(["G02", "G05", "G07", "G15", "G16", "G24", "G26"], "P04", 0.83)

-- Tabel users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Pastikan ada PRIMARY KEY di sini
    username VARCHAR(100),
    umur INT,
    gender VARCHAR(10)
);

-- Tabel diagnosa
CREATE TABLE diagnosa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,  -- Kolom yang menjadi referensi
    penyakit VARCHAR(255),
    persentase_kemungkinan FLOAT,
    tanggal_diagnosa TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- Menyambungkan dengan users.id
);
CREATE DATABASE IF NOT EXISTS qendra_per_kafshe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE qendra_per_kafshe;

CREATE TABLE IF NOT EXISTS perdoruesit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emri_i_plote VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fjalekalimi VARCHAR(255) NOT NULL,
    roli ENUM('administrator', 'staf', 'veteriner', 'vullnetar', 'qytetar') DEFAULT 'qytetar',
    telefoni VARCHAR(20),
    eshte_aktiv BOOLEAN DEFAULT TRUE,
    krijuar_ne TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hapesira_strehimit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emri VARCHAR(50) NOT NULL,
    kategoria ENUM('kafas', 'dhoma', 'karantine', 'oborr') NOT NULL,
    kapaciteti INT NOT NULL,
    pershkrimi TEXT
);

CREATE TABLE IF NOT EXISTS kafshet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emri VARCHAR(50) NOT NULL,
    lloji VARCHAR(30) NOT NULL,
    raca VARCHAR(50),
    mosha_ne_muaj INT,
    gjinia ENUM('mashkull', 'femër') NOT NULL,
    pershkrimi TEXT,
    gjendja_shendetesore VARCHAR(255),
    statusi ENUM('ne_dispozicion', 'ne_kujdes', 'i_adoptuar', 'ne_karantine') DEFAULT 'ne_dispozicion',
    data_e_pranimit DATE NOT NULL,
    hapesira_id INT,
    regjistruar_nga INT,
    FOREIGN KEY (hapesira_id) REFERENCES hapesira_strehimit(id) ON DELETE SET NULL,
    FOREIGN KEY (regjistruar_nga) REFERENCES perdoruesit(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS te_dhenat_mjekesore (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kafshe_id INT NOT NULL,
    veteriner_id INT,
    lloji_rekordit VARCHAR(50) NOT NULL,
    pershkrimi TEXT NOT NULL,
    data_rekordit DATE NOT NULL,
    data_e_radhes DATE,
    FOREIGN KEY (kafshe_id) REFERENCES kafshet(id) ON DELETE CASCADE,
    FOREIGN KEY (veteriner_id) REFERENCES perdoruesit(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS adoptimet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kafshe_id INT NOT NULL,
    qytetar_id INT NOT NULL,
    statusi ENUM('ne_pritje', 'miratuar', 'refuzuar') DEFAULT 'ne_pritje',
    data_e_aplikimit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    komenti_i_stafit TEXT,
    FOREIGN KEY (kafshe_id) REFERENCES kafshet(id) ON DELETE CASCADE,
    FOREIGN KEY (qytetar_id) REFERENCES perdoruesit(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS donacionet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kontribuesi_id INT,
    lloji ENUM('financiar', 'ushqim', 'barna', 'pajisje') NOT NULL,
    vlera_ose_sasia DECIMAL(10,2) NOT NULL,
    pershkrimi TEXT,
    data_e_donacionit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kontribuesi_id) REFERENCES perdoruesit(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS detyrat_e_kujdesit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kafshe_id INT,
    i_caktuar_tek INT,
    krijuar_nga INT,
    titulli VARCHAR(100) NOT NULL,
    pershkrimi TEXT,
    statusi ENUM('per_te_bere', 'ne_proces', 'kryer') DEFAULT 'per_te_bere',
    afati_fundit DATETIME,
    FOREIGN KEY (kafshe_id) REFERENCES kafshet(id) ON DELETE CASCADE,
    FOREIGN KEY (i_caktuar_tek) REFERENCES perdoruesit(id) ON DELETE SET NULL,
    FOREIGN KEY (krijuar_nga) REFERENCES perdoruesit(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS inventari (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emri_i_artikullit VARCHAR(100) NOT NULL,
    kategoria VARCHAR(50) NOT NULL,
    sasia INT NOT NULL,
    min_sasia INT DEFAULT 5,
    njesia VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS njoftimet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perdorues_id INT NOT NULL,
    titulli VARCHAR(100) NOT NULL,
    mesazhi TEXT NOT NULL,
    eshte_lexuar BOOLEAN DEFAULT FALSE,
    krijuar_ne TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (perdorues_id) REFERENCES perdoruesit(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS raporte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    krijuar_nga INT,
    lloji_i_raportit VARCHAR(50) NOT NULL,
    detajet TEXT NOT NULL,
    krijuar_ne TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (krijuar_nga) REFERENCES perdoruesit(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS historiku_veprimeve (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perdorues_id INT,
    veprimi VARCHAR(255) NOT NULL,
    koha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (perdorues_id) REFERENCES perdoruesit(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS vizitat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    qytetar_id INT NOT NULL,
    data_e_vizites DATETIME NOT NULL,
    qellimi TEXT,
    statusi ENUM('konfirmuar', 'anuluar', 'perfunduar') DEFAULT 'konfirmuar',
    FOREIGN KEY (qytetar_id) REFERENCES perdoruesit(id) ON DELETE CASCADE
);
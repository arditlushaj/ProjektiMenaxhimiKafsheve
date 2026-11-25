INSERT INTO perdoruesit (id, emri_i_plote, email, fjalekalimi, roli, telefoni, eshte_aktiv) VALUES
(1, 'Admin Qendra', 'admin@qendra.test', '$2b$12$e8...hash_ketu...', 'administrator', '+38344111222', TRUE),
(2, 'Stafi Drejtues', 'staf@qendra.test', '$2b$12$e8...hash_ketu...', 'staf', '+38344222333', TRUE),
(3, 'Arben Krasniqi', 'veteriner@qendra.test', '$2b$12$e8...hash_ketu...', 'veteriner', '+38344333444', TRUE),
(4, 'Vullnetari 1', 'vullnetar@qendra.test', '$2b$12$e8...hash_ketu...', 'vullnetar', '+38344444555', TRUE),
(5, 'Qytetar Test', 'qytetar@qendra.test', '$2b$12$e8...hash_ketu...', 'qytetar', '+38344555666', TRUE);

INSERT INTO kafshet (id, emri, lloji, raca, mosha_ne_muaj, gjinia, pershkrimi, gjendja_shendetesore, statusi, data_e_pranimit, regjistruar_nga) VALUES
(1, 'Bela', 'qen', 'Stërqok', 12, 'femër', 'Shumë e qetë dhe miqësore', 'E vaksinuar', 'ne_dispozicion', '2026-10-01', 2),
(2, 'Miu', 'mace', 'Evropiane', 6, 'mashkull', 'Lojukare dhe e pastër', 'Shëndetplotë', 'ne_kujdes', '2026-10-05', 2),
(3, 'Rex', 'qen', 'Labrador', 24, 'mashkull', 'Qen besnik dhe energjik', 'Nën vëzhgim mjekësor', 'ne_dispozicion', '2026-10-10', 2);

INSERT INTO hapesira_strehimit (id, emri, kategoria, kapaciteti, pershkrimi) VALUES
(1, 'Kafazi A1', 'kafas', 2, 'Kafaz i brendshëm për qen të vegjël'),
(2, 'Dhoma e Maceve', 'dhoma', 5, 'Ambient i ngrohtë për macet'),
(3, 'Karantina 1', 'karantine', 3, 'Për raste të izoluara shëndetësore');

INSERT INTO te_dhenat_mjekesore (id, kafshe_id, veteriner_id, lloji_rekordit, pershkrimi, data_rekordit, data_e_radhes) VALUES
(1, 1, 3, 'vaksinim', 'Vaksina e parë kundër të thejve', '2026-10-02', '2027-04-02'),
(2, 2, 3, 'kontroll', 'Kontroll rutinor shëndetësor', '2026-10-06', NULL);

INSERT INTO detyrat_e_kujdesit (id, kafshe_id, i_caktuar_tek, krijuar_nga, titulli, pershkrimi, statusi, afati_fundit) VALUES
(1, 1, 4, 2, 'Ushqyerja e Belës', 'Ushqim i száhur në mëngjes', 'kryer', '2026-10-15 08:00:00'),
(2, NULL, 4, 2, 'Pastrimi i oborrit', 'Pastrimi i hapësirës së jashtme', 'per_te_bere', '2026-10-15 12:00:00');
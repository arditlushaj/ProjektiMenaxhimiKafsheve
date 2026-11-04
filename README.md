# Qendra për Menaxhimin e Kafshëve (Animal Shelter Management System)

Një sistem RESTful API i ndërtuar me **Python (Flask)** dhe **MariaDB / MySQL** për menaxhimin e plotë të të dhënave të një qendre për strehimin dhe adoptimin e kafshëve.

## 🚀 Karakteristikat Kryesore

- **Menaxhimi i Kafshëve:** Regjistrimi i kafshëve të reja, përditësimi i statusit (ne_dispozicion, ne_kujdes, i_adoptuar, ne_karantine), caktimi në hapësirat e strehimit dhe historiku shëndetësor.
- **Autentikimi & Rolet:** Kontroll i sigurt i hyrjes bazuar në rolet e përdoruesve: Administrator, Staf, Veteriner, Vullnetar dhe Qytetar.
- **Procesi i Adoptimit:** Menaxhimi i aplikimeve për adoptim nga qytetarët, shqyrtimi dhe miratimi apo refuzimi i tyre nga stafi.
- **Rekordet Mjekësore:** Regjistrimi i kontrolleve mjekësore, vaksinimeve dhe caktimi i datave të ardhshme nga veterinerët.
- **Inventari & Detyrat e Kujdesit:** Ndjekja e stoqeve të ushqimit e barnave, si dhe caktimi e menaxhimi i detyrave ditore për vullnetarët dhe stafin.
- **Vizitat & Donacionet:** Menaxhimi i kërkesave për vizita në qendër dhe regjistrimi i donacioneve financiare apo materiale.

## 📁 Struktura e Projektit

```text
qendra-per-kafshe/
│
├── app/                                  # Dosja kryesore e aplikacionit Flask
│   ├── models/                           # Modelet SQLAlchemy për 12 tabelat
│   ├── routes/                           # Endpoint-et e API-së (Blueprints)
│   └── services/                         # Logjika e biznesit dhe validimet
│
├── .gitignore                            # Skedarët e injoruar nga Git (venv, pycache)
├── README.md                             # Dokumentimi i projektit
├── Raporti_2_Ardit_Lushaj.docx           # Raporti Teknik 2 për dorëzim akademik
├── qendra_per_menaxhimi_e_kafsheve.sql   # Skema DDL e bazës së të dhënave (12 tabelat)
├── seed.sql                              # Të dhënat fillestare testuese
└── run.py                                # Skedari kryesor për nisjen e serverit
```

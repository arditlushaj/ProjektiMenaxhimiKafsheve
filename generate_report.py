from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.shared import Inches, Pt


OUTPUT = Path(__file__).resolve().parent / "Raporti_3_Ardit_Lushaj.docx"


def add_heading(document, text, level=1):
    heading = document.add_heading(text, level=level)
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return heading


def add_bullets(document, items):
    for item in items:
        document.add_paragraph(item, style="List Bullet")


def add_numbered(document, items):
    for item in items:
        document.add_paragraph(item, style="List Number")


document = Document()
section = document.sections[0]
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.85)
section.right_margin = Inches(0.85)

styles = document.styles
styles["Normal"].font.name = "Calibri"
styles["Normal"].font.size = Pt(11)

title = document.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("PROJEKT – PRAKTIKË PROFESIONALE | Semestri V")
run.bold = True
run.font.size = Pt(14)

subtitle = document.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("Raporti Teknik 3 – Frontend-i, integrimi dhe progresi funksional")
run.bold = True
run.font.size = Pt(18)

meta = document.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.add_run("Qendra për Kujdesin e Kafshëve\n")
meta.add_run("Student: Ardit Lushaj\n")
meta.add_run(f"Data: {date.today().isoformat()}")

document.add_page_break()

add_heading(document, "1. Përmbledhja e fazës", 1)
document.add_paragraph(
    "Në fazën 3 projekti kalon nga dizajni dhe skemat nga SQL te një prototip funksional "
    "që demonstron integrimin e UI-së me backend-in dhe databazën. Zgjedhja teknike është "
    "Flask, HTML, CSS dhe JavaScript, ndërsa SQLite përdoret si databazë demo e vetë-përmbajtur "
    "për të mundësuar ekzekutim lokal pa shërbime shtesë."
)

add_heading(document, "2. Organizimi i frontend-it", 1)
add_bullets(document, [
    "templates/: paraqitja HTML dhe struktura e faqeve.",
    "static/styles.css: dizajni responsive, komponentët vizualë dhe gjendjet e ndërfaqes.",
    "static/app.js: komunikimi me API, renderimi i listave dhe menaxhimi i formulave.",
    "routes/API: endpoint-et Flask organizohen në app/__init__.py.",
    "Databaza: inicializimi dhe operacionet SQLite ndodhen në të njëjtin modul backend.",
])
document.add_paragraph(
    "Organizimi është i arsyeshëm për një prototip monolitik të vogël: frontend-i ndahet sipas "
    "shtresave (template, stil, logjikë klienti), ndërsa backend-i mban inicializimin, API-t dhe "
    "operacionet e të dhënave."
)

add_heading(document, "3. Flow-i kryesor: aplikimi për birësim", 1)
document.add_paragraph(
    "User action → Form validation → API request → Backend logic → "
    "Database operation → API response → UI update"
)
add_numbered(document, [
    "Përdoruesi klikon 'Apliko për birësim' te karta e një kafshe në dispozicion.",
    "JavaScript hap një dialog dhe i kalon ID-në e kafshës formularit.",
    "Validimi HTML kërkon emrin, email-in dhe formatin e vlefshëm të email-it.",
    "Frontend-i dërgon POST /api/adoptions me përmbajtje JSON.",
    "Backend-i kontrollon fushat, email-in, ekzistencën e kafshës dhe statusin available.",
    "Aplikimi ruhet në tabelën adoption_applications me status pending.",
    "Backend-i kthen aplikimin e ri me HTTP 201.",
    "Frontend-i mbyll formularin, shfaq toast suksesin dhe përditëson listat.",
])
document.add_paragraph(
    "Flow-i i miratimit vazhdon me PATCH /api/adoptions/<id>. Kur statusi bëhet approved, "
    "backend-i përditëson edhe statusin e kafshës në adopted."
)

add_heading(document, "4. Flow-et funksionale të tjera", 1)
add_bullets(document, [
    "Menaxhimi i kafshëve: GET /api/animals me kërkim dhe filtër, dhe POST /api/animals për regjistrim.",
    "Detyrat e kujdesit: GET /api/tasks dhe PATCH /api/tasks/<id> për kalimin to_do → in_progress → done.",
    "Gjendjet UI: loading, empty, error, validim formulari dhe mesazhe toast.",
    "Kontrolli i integritetit: backend-i kthen gabime 400, 404 dhe 409 për input ose gjendje të pavlefshme.",
])

add_heading(document, "5. Demonstrim i backend-it dhe databazës", 1)
document.add_paragraph(
    "DB-ja demo përmban tabelat animals, adoption_applications dhe care_tasks. Të dhënat "
    "inicializohen automatikisht në qendra.db nëse tabela është bosh. Operacionet përdorin "
    "sqlite3.Row dhe parametrizim SQL, duke reduktuar rrezikun e gabimeve dhe injeksionit."
)
add_bullets(document, [
    "GET lexon, filtrojnë dhe kthen JSON.",
    "POST validon dhe kryen INSERT.",
    "PATCH kontrollon ekzistencën dhe ndryshon statusin.",
    "Miratimi i birësimit përditëson dy tabela në të njëjtën kontekst databaze.",
])

add_heading(document, "6. Code review i shkurtër", 1)
document.add_paragraph(
    "Pika kryesore e rishikuar është create_adoption(): ajo kontrollon ekzistencën e kafshës "
    "para insert-it dhe e ndalon aplikimin kur kafsha nuk është available. Kjo parandalon "
    "aplikime për kafshë të adoptuara dhe përmirëson integritetin."
)
document.add_paragraph(
    "Pika të tjera të rëndësishme: frontend-i nuk beson vetëm validimin HTML, pasi backend-i "
    "rivalidon input-et; gjendjet loading/error/empty i shmangin ekrane të zbrazëta apo përgjigje "
    "të heshtura; lidhjet SQLite mbyllen automatikisht pas request-it."
)

add_heading(document, "7. Përmirësimet e bëra në këtë fazë", 1)
add_bullets(document, [
    "Zëvendësimi i backend-it shembull me API të plotë për kafshët, birësimet dhe detyrat.",
    "Shtimi i një ndërfaqeje responsive me navigim nga skeda.",
    "Shtimi i search/filter, validimeve, loading, empty dhe error states.",
    "Shtimi i testeve automatike për health, kafshë, birësim dhe detyra.",
    "Shtimi i mbylljes së sigurtë të lidhjeve SQLite.",
    "Korrigjimi i SQL-së së demo-s dhe dokumentacionit.",
])

add_heading(document, "8. Bug-u më i vështirë dhe zgjidhja", 1)
document.add_paragraph(
    "Gjatë testeve, lidhjet SQLite mbeteshin të hapura në Windows dhe pengonin fshirjen e "
    "bazave të përkohshme testuese. Zgjidhja ishte ruajtja e lidhjes në g të Flask-ut dhe "
    "mbyllja e saj në teardown_appcontext, me mbyllje shtesë pas inicializimit."
)

add_heading(document, "9. Testimi", 1)
add_bullets(document, [
    "python -m compileall -q app test_app.py run.py main.py",
    "python -m unittest -v",
    "5 teste kalojnë: home/health, validimi i kafshëve, filtrimi, flow-i i birësimit dhe përditësimi i detyrës.",
])

add_heading(document, "10. Çfarë përfundoi dhe çfarë mbetet", 1)
add_heading(document, "Përfunduar", 2)
add_bullets(document, [
    "UI demo responsive.",
    "Flow i plotë për birësimin.",
    "API për kafshët dhe detyrat.",
    "Integrimi me databazën SQLite.",
    "Loading, empty dhe error states.",
    "Testet bazë dhe dokumentacioni.",
])
add_heading(document, "Mbetet deri në versionin beta", 2)
add_bullets(document, [
    "Autentifikimi dhe autorizimi sipas roleve.",
    "Migrimi i finalizuar nga SQLite demo te MySQL/MariaDB.",
    "Historiku mjekësor, strehimi, donacionet dhe njoftimet.",
    "Mbrojtja CSRF dhe hardening i session/cookie.",
    "Testim shtesë browser dhe validim vizual në pajisje.",
])

add_heading(document, "11. Udhëzimet për demo live", 1)
add_numbered(document, [
    "Nisni python run.py.",
    "Hapni http://127.0.0.1:5000.",
    "Kërkoni një kafshë ose zgjidhni filtër statusi.",
    "Shtoni një kafshë të re.",
    "Dërgoni një aplikim për birësim.",
    "Hapni skedën Aplikimet dhe miratoni aplikimin.",
    "Kontrolloni që statusi i kafshës ndryshon në adopted.",
    "Hapni skedën Detyrat dhe kaloni një detyrë në progres/done.",
])

document.core_properties.title = "Raporti Teknik 3 – Frontend-i, integrimi dhe progresi funksional"
document.core_properties.author = "Ardit Lushaj"
document.save(OUTPUT)
print(OUTPUT)

Tema: Sistemi për Menaxhimin e Qendrave të Kujdesit për Kafshë
Raporti 1
Ideja e projektit
Ideja është të zhvillohet një sistem për menaxhimin e qendrave të kujdesit për kafshë. Sistemi do t’i ndihmojë punonjësit dhe vullnetarët të organizojnë kujdesin e përditshëm, trajtimet veterinare, strehimin dhe procesin e birësimit. Gjithashtu, qytetarët do të mund të shohin kafshët që kërkojnë shtëpi, të aplikojnë për birësim dhe të kontaktojnë qendrën.
Kërkesat e sistemit
Sistemi duhet të mundësojë:
- Qasje për administratorët, punonjësit, veterinerët, vullnetarët dhe qytetarët.
- Regjistrimin e kafshëve me të dhëna si emri, lloji, raca, mosha, gjinia, përshkrimi dhe gjendja shëndetësore.
- Ruajtjen e historikut të vaksinimeve, kontrolleve, trajtimeve dhe barnave të kafshëve.
- Menaxhimin e vendeve të strehimit dhe caktimin e kafshëve në hapësira të përshtatshme.
- Organizimin e orareve për ushqim, pastrim, shëtitje dhe kujdes tjetër.
- Regjistrimin e punonjësve dhe vullnetarëve, si dhe caktimin e detyrave për ta.
- Publikimin e kafshëve që janë në dispozicion për birësim.
- Pranimin dhe shqyrtimin e aplikimeve për birësim nga administratori ose punonjësi përgjegjës.
- Ruajtjen e të dhënave të aplikuesit dhe komunikimin e vendimit për aplikimin.
- Regjistrimin e donacioneve dhe furnizimeve, si ushqimi, barnat dhe pajisjet.
- Dërgimin e njoftimeve për vizita veterinare, detyra dhe ndryshime në statusin e aplikimeve.
- Krijimin e raporteve për kafshët, trajtimet, birësimet dhe donacionet.
Çdo përdorues duhet të ketë ID unike. Hyrja në sistem duhet të bëhet me autentifikim, ndërsa fjalëkalimet duhet të ruhen të hash-uara. Qasja dhe funksionet duhet të varen nga roli i përdoruesit. Ndërfaqja duhet të jetë e kuptueshme dhe responsive për ekrane të ndryshme.
Veprimet e rëndësishme, si miratimi i birësimit, ndryshimi i të dhënave shëndetësore dhe administrimi i përdoruesve, duhet të kryhen vetëm nga personeli i autorizuar.
Teknikat dhe arkitektura
Frontend
- HTML
- CSS
- JavaScript
- Bootstrap
Ndërfaqja do të përfshijë faqen publike, formularin e aplikimit për birësim dhe panelet për administratorët, punonjësit, veterinerët dhe vullnetarët.
Backend
- Python
- Flask ose Django
- SQLAlchemy ose Django ORM
- Autentifikim dhe autorizim sipas roleve
- Menaxhim i kafshëve, kujdesit, aplikimeve, detyrave dhe njoftimeve
Për një projekt të përmasave të vogla ose mesatare mund të përdoret Flask. Django është alternativë e përshtatshme kur kërkohet administrim i gatshëm dhe strukturë më e plotë.
Databaza
- MySQL ose MariaDB
Modeli fillestar i databazës mund të përfshijë tabelat:
Tabela	Për çfarë shërben
users	Llogaritë e përdoruesve, email-i, fjalëkalimi i hash-uar dhe roli
animals	Të dhënat bazë dhe statusi i kafshëve
medical_records	Kontrollet, diagnozat, vaksinimet dhe trajtimet
shelter_spaces	Hapësirat e strehimit dhe kapaciteti i tyre
animal_assignments	Caktimi i kafshëve në hapësira të strehimit
care_tasks	Detyrat e ushqimit, pastrimit, shëtitjes dhe kujdesit
adoption_applications	Aplikimet dhe statusi i procesit të birësimit
adoptions	Birësimet e miratuara dhe të dhënat përkatëse
donations	Donacionet financiare ose materiale
supplies	Inventari i ushqimit, barnave dhe pajisjeve
notifications	Njoftimet për përdoruesit
approvals	Veprimet që kërkojnë shqyrtim ose miratim


Arkitektura e propozuar
Rekomandohet arkitekturë monolitike, ku sistemi ndahet në module sipas funksionalitetit:
- Menaxhimi i përdoruesve dhe roleve
- Regjistrimi i kafshëve
- Kujdesi dhe historiku mjekësor
- Strehimi dhe detyrat ditore
- Birësimet
- Donacionet dhe inventari
- Njoftimet dhe raportet
- Administrimi dhe miratimet
Faza e zhvillimit të projektit
Faza	Aktivitetet kryesore	Rezultati i pritshëm
1. Analiza e kërkesave	Përcaktimi i roleve, funksioneve dhe rregullave të sistemit	Lista e kërkesave funksionale dhe jofunksionale
2. Dizajnimi i sistemit	Përgatitja e arkitekturës, diagramit ER dhe rrjedhave të punës	Dizajni teknik dhe modeli i databazës
3. Krijimi i databazës	Krijimi i tabelave, çelësave, lidhjeve dhe kufizimeve	Databaza MySQL/MariaDB e gatshme
4. Ndërtimi i ndërfaqes	Krijimi i faqes publike, formularëve dhe paneleve sipas roleve	Ndërfaqe responsive dhe e lehtë për përdorim
5. Autentifikimi dhe rolet	Regjistrimi, hyrja, dalja dhe kontrolli i qasjes	Hyrje e sigurt dhe qasje sipas roleve
6. Menaxhimi i kafshëve	Regjistrimi dhe përditësimi i të dhënave të kafshëve	Modul për menaxhimin e kafshëve
7. Kujdesi dhe trajtimet	Regjistrimi i vizitave, vaksinimeve, barnave dhe detyrave	Historik i kujdesit për secilën kafshë
8. Birësimet	Publikimi i kafshëve dhe shqyrtimi i aplikimeve	Proces i organizuar i birësimit
9. Donacionet dhe njoftimet	Regjistrimi i donacioneve, inventarit dhe njoftimeve	Menaxhim i burimeve dhe komunikimit
10. Verifikimi dhe dokumentimi	Kontrolli i funksioneve, korrigjimi i problemeve dhe përgatitja e dokumentimit	Version i përfunduar dhe dokumentuar


Rrjedha e birësimit
1. Punonjësi regjistron kafshën dhe shënon nëse është në dispozicion për birësim.
2. Qytetari shikon profilin e kafshës dhe dërgon aplikimin.
3. Administratori ose punonjësi shqyrton aplikimin.
4. Aplikimi miratohet ose refuzohet dhe statusi ruhet në sistem.
5. Nëse miratohet, regjistrohen të dhënat e birësimit dhe përditësohet statusi i kafshës.
Orari i propozuar
- Java 1: Analiza e kërkesave, dizajni teknik dhe modeli i databazës.
- Java 2: Ndërtimi i faqeve dhe navigimit.
- Java 3: Autentifikimi, rolet dhe siguria e llogarive.
- Java 4: Regjistrimi i kafshëve, strehimi dhe detyrat e kujdesit.
- Java 5: Historiku mjekësor dhe procesi i birësimit.
- Java 6: Donacionet, inventari dhe njoftimet.
- Java 7: Integrimi i moduleve dhe përgatitja e dokumentimit.
- Java 8: Verifikimi përfundimtar dhe përmirësimet.
Ky plan mund të përshtatet sipas kohës dhe kërkesave të projektit.

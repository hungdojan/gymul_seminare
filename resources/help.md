# Navod

## Rozložení aplikace
![layout](:/layout.jpg)
1. Horní panel s možnostmi
2. Tlačítka na filtraci studentů
3. Panel se studenty
4. Panel s dny
5. Panel s předměty
6. Tlačítko pro setřídění dat


## Načtení a ukládání souborů a práce
Všechny soubory se vkládají přes <b>Soubor > Načíst studenty</b> resp. <b>Soubor > Načíst předměty</b>. Výsledky se exportují přes <b>Soubor > Exportovat soubory</b>. Práce se dá též uložit a načíst ze souborů. Načtení uložené práce funguje přes <b>Soubor > Otevřít soubor</b> a pro uložení <b>Soubor > Uložit</b> nebo <b>Uložit jako</b>.

Pro otevření práce vyberte daný JSON soubor. Jednotlivé úkony mají přidělené klávesové zkratky: <b>Ctrl+S</b> pro uložení a <b>Ctrl+O</b> pro otevření.

## Přidávání a ovládání dnů
Dny se ovládájí na 3. panelu. V horní části se nacházejí 3 tlačítka:

- Add - přidá nový den
- Filter - přerovná rozložení předmětů pro přehlednější zobrazení
- Delete - vymaže označené dny

Po přidání dnu se objevi nový widget se seznamem načtených předmětů. Pro označení předmětu stačí kliknout na příslušný předmět v daném dni. Označené dny jsou zvýrazněné žlutě.

![unfiltered days](:/unfilter_days.png)

Pro zlepšení čitelnosti byla přidána možnost seřadit k sobě předměty, které jsou označené, a to pomocí tlačítka <b>FILTER</b> (viz. obrázky).

![filtered_days](:/filtered_days.png)

Odstranění dnu je přímočaré. Po kliknutí na widget dnu (mimo tlačítka předmětu) se okraj widgetu změní v čárkovaný styl. Následně stačí kliknout na tlačítko <b>DELETE</b> a den se smaže.

![selected days](:/selected_day.png)

## Práce se studentem
Studenti jsou odlišeni barvami (červená, žlutá, zelená, modrá) podle toho, jak úspěšně byli přiřazeni do jednotlivých dnů. Červení studetni mají smůlu, pro ně se nenašla žádná kombinace. Zelení studenti mají jasno, jenom jedna kombinace byla nalezena a proto jim byla automaticky i přidelěna. Žlutí studenti mají tu výhodu, že se mohou vybrat, jak si jednotlivé předměty poskládají. Modří studenti narozdíl od žlutých mají již vybranou kombinaci.

Kliknutím levým tlačítkem myši na studenta může uživatel vybrat, v jaké dny bude student jednotlivé předměty navstěvovat. Otevře se okno, ve kterém vybere kombinaci a dá uložit.

Studentovi může uživatel upravit data, zamknout ho nebo smazat. Všechny akce se dají provést přes kontextové menu. Stačí na příslušného studenta kliknout pravým tlačítkem.

![context_menu](:/context_menu.png)

## Filtrace studentů
Studenti se dají filtrovat podle toho, v jakém jsou momentálně stavu. Pokud je tlačítko v pozici **ON**, tak to znamená, že studenti dané barvy jsou zobrazeni. V opačném případě (tlačítko je ve stavu **OFF**) jsou studenti dané barvy ignorováni.

## Správce studentů a předmětů
Do verze 0.2.0 byla přidána možnost spravovat načtené studenty a předměty. Vše najdete v horní liště pod kolonkou <b>Spravovat</b>. 

![student_control](:/student_control.png)
![subject_control](:/subject_control.png)

## Dodatečné funkce a export dat
Od verze 0.3.0 může uživatel využívat 2 nové funkce: 
- možnost provést akci zpět (<b>Ctrl+Z</b>) a vpřed (<b>Ctrl+Y</b>)
- během ovládání aplikace vzniká bokem logovací soubor <b>seminare.log</b>, který obsahuje historii akcí provedené uživatelem; tento soubor je možno použít k rekonstrukci provedenych akcí, či zaslání vývojáři v případě objevení závady v aplikaci.

Po dokončení návrhu rozvrhu a vložení studentů do jednotlivých předmětů může uživatel exportovat data.
Akce <b>Soubor > Exportovat data (Ctrl+E)</b> vygeneruje 2 **CSV** soubory s roztřízenými daty. 
# Navod

## Rozložení aplikace
![layout](:/layout.jpg)
1. Horní panel s možnostmi
2. Tlačítka na filtraci studentů
3. Panel se studenty
4. Panel s dny
5. Panel s předměty
6. Tlačítko pro setřídění dat


## Vkládání a ukládání souborů
Všechny soubory se vkládají přes <b>Soubor > Načíst studenty</b> resp. <b>Soubor > Načíst předměty</b>. Výsledky se exportují přes <b>Soubor > Exportovat soubory</b>. 
Práce je nyní také možné uložit. Před uložením je potřeba setřídit data (tlačítko <b>Sort</b> nebo klávesová zkratka <b>F5</b>). Po uložení se vytvoří JSON soubor.

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
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
Studentovi se dá nastavit mnoho věcí. Po kliknutí levým tlačítkem myši na 
> [!IMPORTANT]
> Tento projekt sloužil primárně k testování A* algoritmu.
> Struktura kódu by chtěla vylepšit aby lépe odpovídala standardu PEP 8.

# Hra Had

Jedná se o jednoduchou hru had. Jejím úkolem je dosáhnout největšího skóre jezením jablek pomocí hada.  
Had sní jablko tak, že na něj najede. Po snězení se hadův ocas prodlouží o jedno políčko a nové jablko se objeví
na neazplněném políčku. Hra končí naražením hada do překážky (Okraj okna nebo své tělo). Minimální skóre je 0
(Had narazí do zdi, aniž by snědl jediné jablko) a maximální skóre je počet řádku * počet sloupců - 1 
(To lze dosáhnout zaplněním celé hrací plochy tělem hada, které pak narazí do konce svého ocasu).  
  
Tato hra se skládá z dvou oken. Jedním je menu a druhou je hra samotná.  
Spouští se ze souboru 'main.py'.

Text k implementaci a hodnocení algorimtu: [vancafra.pdf](./vancafra.pdf)

Ukázka: [![Ukazka](https://img.youtube.com/vi/ohgrOE_7RRE/hqdefault.jpg)](https://www.youtube.com/embed/ohgrOE_7RRE)

## Okna aplikace

### Menu
Má dvě tlačítka. Pro jejich aktivaci na ně najeďte myší a klikněte levým tlačítkem myši.  
- **Manual Play** - Spustí hru, která je ovládaná hráčem (viz. *Ovládání*).
- **AI Play** - Spustí hru, která je ovládaná řídícím algoritmem (A*).

V dolní částí okna je zobrazena statistika (Data po zavření aplikace neukládá).
- **Last score** - Poslední dosažené skóre.
- **Runs** - Počet dohraných her (Počítá se každá hra, bez ohledu na skóre)
- **Score**
    - **min** - Nejmenší dosažené skóre. 
    - **max** - Největší dosažené skóre. 
    - **avg** - Průměrné dosažené skóre (Zaokrouhleno na 2 desetinná místa).
### Hra
Okno hry. Skládá se z políček ve tvaru čtverce.  
- **Typy políček**
  - *černé* - Prázdné políčko
  - *červené* - Jablko. Když hada hlava najede na jablíčko, had se prodlouží.
  - *tmavě zelené* - Hlava hada. Část hada, pro kterou se mění směr.
  - *světle zelené* - Tělo hada. Následuje hlavu hada a prodlužuje se podle počtu sebraných jablek.
- **Ovládání** (až na klávesu ESCAPE funguje jen v *manuálním módu*)
  - *ESCAPE* - Ukončí hru (Schová okno 'Hra')
  - *W / Šipka nahoru* - Had se pohne směrem nahoru (pokud nemíří dolů)
  - *S / Šipka dolů* - Had se pohne směrem dolů (pokud nemíří nahoru)
  - *A / Šipka doleva* - Had se pohne směrem doleva (pokud nemíří doprava)
  - *D / Šipka doprava* - Had se pohne směrem doprava (pokud nemíří doleva)
- **Hra řízené algoritmem** - Tento mód je ovládán řídícím algortimem, až na vyjímku ukončení hry (viz. *Ovládání*).
  Od manuálního režimu je zde navíc modrá čára, která znázorňuje cestu, kterou vybral řídící algoritmus (A*).
- **Skóre** - Jméno okna znázorňuje současné skóre. (+1 za každé sebrané jablko nebo délka hada bez hlavy)

## Soubory aplikace

### main.py
Hlavní soubor, který obstarává okno hlavního menu, ze kterého se spouští hra (pomocí 'Snake.py').
### snake.py
Soubor, který zaobaluje třídu Snake, která se stará o chod hry (viz. okno *Hra*). Využívá soubor 'astar.py'
### astar.py
Soubor, který v sobě má jedinou funkci, která pomocí A* algoritmu najde nejkratší cestu k jablku 
(Bere v potaz tělo hada a snaží se mu vyhnout).

# Svet superjunakov Stan Leeja
Projektna naloga analize podatkov za programiranje 1.

Avtor: **Nejc Zajc** \
Študijsko leto: 2019/2020 

Analiziral bom svet, ki ga je pri Marvelovih stripih ustvaril Stan Lee. To vključuje osebe, prostore, predmete, ostredotočil pa se bom na analizo oseb. Vir podatkov je [Marvel FANDOM wiki](https://marvel.fandom.com/wiki/Category:Stan_Lee/Creator), kjer so liki našteti, podrobnosti pa bom našel na posameznih straneh.

Za vsak članek z likom bom zajel *id* pod katerim je označen, njegov *tip*, *avtorje* ki so sodelovali pri njegovem ustvarjanju ter kdaj je bil *prvič omenjen*.
Poleg tega, bom pri vsaki osebi zajel še:
* *pravo ime*
* *naziv*
* *razmerje*
* *vesolje*
* *posebne moči* in *tabela podatkov* (kjer so ti podatki zapisani)


Delovne hipoteze:
- Več kot polovica likov bodo osebe.
- Razmerje "Single" se ne bo pojavilo več kot v 50%.
- Najpogostejši sodelavec Stana je Jack Kirby.
- Najpogostejša posebna moč je *Nadčloveška fizična moč* (Superhuman Strength) 


V mapi "podatki" so shranjene 4 csv datoteke, kjer so shranjeni željeni podatki. Glavni podatki so v "podatki.csv". V "avtorji.csv" so po *id*-jih shranjeni avtorji, ki so pri liku sodelovali s Stan Leejem. Stan se v te datoteki ne pojavlja, saj sem imel samo like, ki jim je pripisan. V "tabele.csv" so poleg *id*-jev še vrednosti pri posameznih atributih iz tabele. V "moci.csv" pa so naštete supermoči likov.

Dodani sta še 2 datoteki s katerima sem pridobil in uredil podatke. Datoteka "orodja.py" je minimalno preurejena datoteka prof. Pretnarja, s katero nam je pomagal pri pridobivanju in shranjevanju podatkov. Z datoteko "Pridobivanje_podatkov.py" pa sem pridobil, shranil in uredil podatke.
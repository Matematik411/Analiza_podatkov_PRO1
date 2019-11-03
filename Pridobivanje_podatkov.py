# ______________________________________________________________________
# | SVET SUPERJUNAKOV STAN LEEJA, avtor: Nejc Zajc, št. leto 2019/2020 |
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import re
import orodja
import os
# Podatki pridobljeni 20.10.2019------------------------------

# Datoteka, s katero pridobim in nato pripravim podatke za analizo.
# Za nalogo sem si izbral Svet superjunakov Stan Leeja. Podatke sem pridobil iz strani GLAVNA, kjer so našteti vsi zadetki, pripisani Stan Leeju.

# Definirana začetna stran in spremeljivke
GLAVNA = "https://marvel.fandom.com/wiki/Category:Stan_Lee/Creator"
PODATKI = "podatki"
PRIDOBIVAM = False
st_strani = 1

# Niza, ki poiščeta posamezni zadetek in link nza naslednjo stran.-----------------------------
vzorec_elementa_na_naslovni = re.compile(
    r'<a href="/wiki/(?P<id>.*)"'
    r' title=".*" class="category-page__member-link">'
    r'(?P<ime>.*)</a>'
    )

vzorec_naslednje_strani = re.compile(
    r'<link rel="next" href="(?P<link>.*)" />'
)


# Še glavna zanka, ki pridobi strani in jih shrani. Začetne strani so shranjene v mapi "naslovne", posamezne strani pa (če se nahajajo na k-ti strani) v mapi "/podatki/podatki_k".------------------------------
if PRIDOBIVAM:
    while GLAVNA != "":
        MAPA_PODATKOV = f"podatki_{st_strani}"
        MAPA_NASLOVNIH = "naslovne"
        NASLOVNA = f"naslovna_{st_strani}"
        
        path = os.path.join(MAPA_NASLOVNIH, f"{NASLOVNA}.html")
        orodja.pripravi_imenik(path)
        orodja.shrani_spletno_stran(GLAVNA, path)

        stran = orodja.vsebina_datoteke(path)

        pot = os.path.join(PODATKI, MAPA_PODATKOV)
        for zadetek in re.finditer(vzorec_elementa_na_naslovni, stran):
            nova_pot = os.path.join(pot, f"{zadetek.group(1)}.html")
            orodja.pripravi_imenik(nova_pot)
            orodja.shrani_spletno_stran(rf"https://marvel.fandom.com/wiki/{zadetek.group(1)}", nova_pot)

        GLAVNA = ""    
        for nov in re.finditer(vzorec_naslednje_strani, stran):
            GLAVNA = nov.group(1)
        
        st_strani += 1


------------------------------------------------------------------------------------------


# Najprej vsi nizi, ki jih iščem------------------------------

# Na začetku določim tip članka, saj natančneje analiziram samo osebe
niz_tipa_clanka = re.compile(
    r'title="(?P<tip>.*?)\s*Template(\s.*?)?"'
)

# Poiščem osnovni blok podatkov pri članku
niz_iskanja_bloka = re.compile(
    r'<hr class="page-header__separator">(?P<blok>.*?)'
    r'(</div>\s*</div>\s*</div>\s*</div>|</tr>\s*</tbody>\s*</table>)',
    flags=re.DOTALL
)

# Če je članek osebe, nato iz njegovega bloka izluščim podatke 
niz_lastnosti_znotraj_bloka = re.compile(
    r'<a href="/wiki/(?!Help|Category|Official|Talk|Marvel).*?" title=".*?">(?P<naziv>.*?)</a></h2>.*?'
    r'</a>\s*Real Name</h3>.*?'
    r'<div class="pi-data-value pi-font">\s*(Presumably)?\s*(<a href=".*?">)?\s*(?P<pravo_ime>.*?)(</a>)?(</div>|<sup).*?'
    r'(</a>\s*Marital Status</h3>.*?'
    r'<a href=".*?">(?P<razmerje>.*?)</a>.*?)?'
    r'</a>\s*Universe</h3>.*?'
    r'<div class="pi-data-value pi-font"><a( href=".*?")?.*?>(?P<vesolje>.*?)</a>.*?'
    r'>\s*Creator(s)?\s*(</span>)?(</h3>|</div>).*?'
    r'<div (class|style)=".*?">(?P<avtorji>.*?)</div>.*?'
    r'>First [Aa]ppearance<.*?title=".*?>(<i>)?(?P<naslov>.*?)\s*</a>.*?'
    r'title=".*?">(?P<datum>.*?)</a>',
    flags=re.DOTALL
)

# Preverim, če je v članku tabela vrednosti
niz_tabela = re.compile(
    r'<td colspan="2" style="text-align:center;.*?><i><b>Power Grid</b></i>'
    r'(?P<tabela>.*?)</td>\s*</tr>\s*</table>\s*</div>',
    flags=re.DOTALL
)

# Če tabelo najde, iz nje opberem števila
niz_podatkov_znotraj_tabele = re.compile(
    r'Power_Grid#.*?(&#160;\d|\d&#160).*?',
    flags=re.DOTALL
)

# Preverim še, če so naštete supermoči
niz_moci = re.compile(
    r'<h3><span class="mw-headline" id="Powers">Powers</span></h3>(?P<moci>.*?)'
    r'(<h\d>|<div)',
    flags=re.DOTALL
)

# In poberem še te
niz_supermoci_znotraj_moci = re.compile(
    r'<b>\s*(.*?)(:)?\s*</b>'
)

# Če pa ni oseba, poiščem samo podatke o avtorjih in prvi izdaji
niz_podatkov_pri_neosebah = re.compile(
    r'>\s*Creator(s)?\s*(</span>)?(</h3>|</div>).*?'
    r'<div (class|style)=".*?">(?P<avtorji>.*?)</div>.*?'
    r'>First [Aa]ppearance<.*?title=".*?>(<i>)?(?P<naslov>.*?)\s*</a>.*?'
    r'title=".*?">(?P<datum>.*?)</a>',
    flags=re.DOTALL
)

# Sledita funkciji, ki uredita slovarje pobranih informacij------------------------------

# Tale sprejme slovar podatkov pri osebah
def uredi_podatke(notranji):
    notranji["naziv"] = re.sub("^.*>", "", notranji["naziv"], flags=re.DOTALL)
    
    notranji["pravo_ime"] = re.sub("<.*?$", "", notranji["pravo_ime"], flags=re.DOTALL)
    
    notranji["avtorji"] = re.sub("\s*<.*?>\s*", "", notranji["avtorji"]).split(",")
    
    if "</i>" in notranji["naslov"]:
        smt = re.sub("\s*</i>.*?#\s*", ",", notranji["naslov"]).split(",")
        notranji["naslov"] = smt[0]
        notranji["izdaja"] = smt[1]
    else:
        notranji["naslov"] = notranji["naslov"]
        notranji["izdaja"] = None
    
    notranji["datum"] = list(map(str.strip,sorted(notranji["datum"].split(","))))
    notranji["leto"] = notranji["datum"][0]
    if len(notranji["datum"]) == 1:
        notranji["mesec"] = None
    else:
        notranji["mesec"] = notranji["datum"][1]
        notranji["mesec"] = re.sub("&nbsp;[\d]*", "", notranji["mesec"])
    del notranji["datum"]
    return notranji

# Naslednja pa slovar pri neosebah
def uredi_pri_neosebah(notranji):
    notranji["avtorji"] = re.sub("\s*<.*?>\s*", "", notranji["avtorji"]).split(",")
    
    if "</i>" in notranji["naslov"]:
        smt = re.sub("\s*</i>.*?#\s*", ",", notranji["naslov"]).split(",")
        notranji["naslov"] = smt[0]
        notranji["izdaja"] = smt[1]
    else:
        notranji["naslov"] = notranji["naslov"]
        notranji["izdaja"] = None
    
    notranji["datum"] = list(map(str.strip,sorted(notranji["datum"].split(","))))
    notranji["leto"] = notranji["datum"][0]
    if len(notranji["datum"]) == 1:
        notranji["mesec"] = None
    else:
        notranji["mesec"] = notranji["datum"][1]
        notranji["mesec"] = re.sub("&nbsp;[\d]*", "", notranji["mesec"])
    del notranji["datum"]
    return notranji

#------------------------------------------------------------------------------------------


# BRANJE STRANI------------------------------
# Nato se skozi shranjene spletne strani zapeljem z zanko in poiščem podatke, jih uredim in nato shranim v csv datoteke.
# Shranjujem jih po eno mapo naenkrat, če je spremenljivka DELAM na True, potem se bo vse izvedlo, sicer ne.
# Prav tako sem spremenil funkcijo zapisi_csv iz orodij, da samo dodaja datoteki in ne napise naslovne vrstice, ki sem jo napisal nato sam.
# Datoteke s csv podatki so shranjene v mapi "podatki".

# Najprej definiram nekaj spremenljivk
DELAM = False
seznam_slovarjev = []
seznam_avtorjev = []
seznam_moci = []
seznam_tabel = []
zacetni_slovar = {"id" : "", "tip" : "", "naziv" : "", "pravo_ime" : "", "razmerje" : "", "vesolje" : "", "avtorji" : [], "naslov" : [], "tabela" : [], "moci" : []}
stati = ["INT", "STR", "SPD", "DUR", "ENP", "FGT"]


# To pa zdaj naredi zgoraj opisan postopek
if DELAM:
    for k in range(1,13):
        seznam_slovarjev = []
        seznam_avtorjev = []
        seznam_moci = []
        seznam_tabel = []
        for filename in os.listdir(f"podatki/podatki_{k}"):
            dodaj = False
            slovar = dict(zacetni_slovar)
            slovar["id"] = filename[:-5]
            stran = orodja.vsebina_datoteke(f"podatki/podatki_{k}/{filename}")
            for hit in re.finditer(niz_tipa_clanka, stran):
                tip = hit.group("tip")
                if tip != "Move":
                    slovar["tip"] = tip
            for hit in re.finditer(niz_iskanja_bloka, stran):    
                blok = hit.group("blok")
            
            if tip == "Character":
                for hit in re.finditer(niz_lastnosti_znotraj_bloka, blok):
                    slovar.update(uredi_podatke(hit.groupdict()))
                for hit in re.finditer(niz_tabela, stran):
                    tabela = hit.group("tabela")
                    stevila = []
                    for hit in re.finditer(niz_podatkov_znotraj_tabele, tabela):
                        stevilo = re.sub("&#160(;)?", "", hit.group(1))
                        stevila.append(stevilo)
                    slovar["tabela"] = stevila
                for hit in re.finditer(niz_moci, stran):
                    moci = hit.group("moci")
                    vse = []
                    for hit in re.finditer(niz_supermoci_znotraj_moci, moci):
                        primer = re.sub("<.*?>", "", hit.group(1))
                        primer = re.sub("&amp;\s*", "", primer)
                        primer = re.sub("&#160", "", primer)
                        vse.append(primer)
                    slovar["moci"] = vse
            
            elif slovar["naziv"] == "":
                for hit in re.finditer(niz_podatkov_pri_neosebah, stran):
                    slovar.update(uredi_pri_neosebah(hit.groupdict()))

            for key in slovar:
                if slovar[key] == "" or slovar[key] == []:
                    slovar[key] = None


            
            osebe = slovar.pop("avtorji", None)
            if osebe is not None:
                dodaj = True
                for oseba in osebe:
                    if oseba != "Stan Lee":
                        seznam_avtorjev.append(
                            {"id": slovar["id"], "avtor" :  oseba}
                        )
            
            velikosti = slovar.pop("tabela", None)
            if velikosti is not None:
                try:
                    for a in velikosti:
                        nov = {"id" : slovar["id"]}
                        for i, a in enumerate(velikosti):
                            nov.update({stati[i] : a})
                    seznam_tabel.append(nov)
                except:
                    pass
            
            lastnosti = slovar.pop("moci", None)
            if lastnosti is not None:
                for lastnost in lastnosti:
                    seznam_moci.append(
                        {"id" : slovar["id"], "moc" : lastnost}
                    )

            if dodaj:
                seznam_slovarjev.append(slovar)



        orodja.zapisi_csv(seznam_slovarjev, ["id", "tip", "naziv", "pravo_ime", "vesolje", "razmerje", "naslov", "izdaja", "leto", "mesec"], "podatki/podatki.csv")
        orodja.zapisi_csv(seznam_avtorjev, ["id", "avtor"], "podatki/avtorji.csv")
        orodja.zapisi_csv(seznam_tabel, ["id"] + stati, "podatki/tabele.csv")
        orodja.zapisi_csv(seznam_moci, ["id", "moc"], "podatki/moci.csv")
        





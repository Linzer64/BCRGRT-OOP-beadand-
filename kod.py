from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


# 1.: osztályok és absztraktció

class Jarat(ABC):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: int):
        self._jaratszam = jaratszam
        self._celallomas = celallomas
        self._jegyar = jegyar

    @property
    def jaratszam(self):
        return self._jaratszam

    @property
    def celallomas(self):
        return self._celallomas

    @property
    def jegyar(self):
        return self._jegyar

    @abstractmethod
    def jarattipus(self) -> str:
        pass


class belfoldijarat(Jarat):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: int):
        super().__init__(jaratszam, celallomas, jegyar)

    def jarattipus(self) -> str:
        return "Belföldi"

    def __str__(self):
        return f"[{self.jarattipus()}]  Szám: {self.jaratszam}   Cél: {self.celallomas}    Ár: {self.jegyar} Ft"


class nemzetkozijarat(Jarat):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: int):
        super().__init__(jaratszam, celallomas, jegyar)

    def jarattipus(self) -> str:
        return "Nemzetközi"

    def __str__(self):
        return f"[{self.jarattipus()}]  Szám: {self.jaratszam}   Cél: {self.celallomas}    Ár: {self.jegyar} Ft"


class Legitarsasag:
    def __init__(self, nev: str):
        self._nev = nev
        self._jaratok = []

    @property
    def nev(self):
        return self._nev

    @property
    def jaratok(self):
        return self._jaratok

    def jarathozzaadas(self, jarat: Jarat):
        self._jaratok.append(jarat)

    def jaratkeres(self, jaratszam: str) -> Optional[Jarat]:
        for jarat in self._jaratok:
            if jarat.jaratszam.upper() == jaratszam.upper():
                return jarat
        return None


class jegyfoglalas:
    _id_szamlalo = 1

    def __init__(self, jarat: Jarat, utasnev: str, datum: datetime):
        self._foglalasid = jegyfoglalas._id_szamlalo
        jegyfoglalas._id_szamlalo += 1
        self._jarat = jarat
        self._utasnev = utasnev
        self._datum = datum

    @property
    def foglalasid(self):
        return self._foglalasid

    @property
    def jarat(self):
        return self._jarat

    @property
    def utasnev(self):
        return self._utasnev

    @property
    def datum(self):
        return self._datum

    def __str__(self):
        id_str = f"ID: {self._foglalasid}".ljust(8)
        utas_str = f"Utas: {self._utasnev}".ljust(25)
        jarat_str = f"Járat: {self.jarat.jaratszam} ({self.jarat.celallomas})".ljust(30)
        datum_str = f"Dátum: {self._datum.strftime("%Y-%m-%d")}".ljust(20)
        ar_str = f"Ár: {self._jarat.jegyar} Ft"
        return f" {id_str}, {utas_str}, {jarat_str}, {datum_str}, {ar_str}"


# 2. validáció és rendszerlogika

class foglalasirendszer:
    def __init__(self, legitarsasag: Legitarsasag):
        self._legitarsasag = legitarsasag
        self._foglalasok = []

    def jegyfoglalasa(self, jaratszam: str, utasnev: str, datumstr: str):
        jarat = self._legitarsasag.jaratkeres(jaratszam)
        if not jarat:
            raise ValueError(f"Hiba: A '{jaratszam}' számú járat nem található meg!")

        try:
            foglalasdatuma = datetime.strptime(datumstr, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Hiba: A dátum formátuma hibás! Kérjük adja meg a dátumot ÉÉÉÉ-HH-NN formátumban!")

        if foglalasdatuma < datetime.now():
            raise ValueError("Hiba: A foglalás dátuma a múltban van!")

        ujfoglalas =jegyfoglalas(jarat, utasnev, foglalasdatuma)
        self._foglalasok.append(ujfoglalas)
        print(f"\nSikeres foglalás! A jegy ára {jarat.jegyar} Ft (Foglalási ID: {ujfoglalas.foglalasid})")

    def foglalaslemondasa(self, foglalas_id: int):
        for foglalas in self._foglalasok:
            if foglalas.foglalasid == foglalas_id:
                self._foglalasok.remove(foglalas)
                print(F"\nA(z) {foglalas_id} ID-jú foglalás sikeresen lemondva.")
                return

        raise ValueError(f"Hiba: Nem található foglalás {foglalas_id} azonosítóval!")

    def foglalasoklistazasa(self):
        if not self._foglalasok:
            print(f"\nNincsenek aktív foglalások jelenleg.")
            return

        print(f"\nAktuális foglalások listája:")
        for f in self._foglalasok:
            print (f)

# 3.: adatok betöltése

def rendszerinicializalasa() -> foglalasirendszer:
    rizzpy = Legitarsasag("Ryair Légitársaság")

    j1 = belfoldijarat("RA-111", "Debrecen", 16000)
    j2 = nemzetkozijarat("RA-221", "London", 44500)
    j3 = nemzetkozijarat("RA-303", "Róma", 36000)

    rizzpy.jarathozzaadas(j1)
    rizzpy.jarathozzaadas(j2)
    rizzpy.jarathozzaadas(j3)

    rendszer = foglalasirendszer(rizzpy)

    rendszer._foglalasok.append(jegyfoglalas(j1,"Réti Virág", datetime(2026, 6, 11)))
    rendszer._foglalasok.append(jegyfoglalas(j1, "Mézes János" , datetime(2026, 6, 13)))
    rendszer._foglalasok.append(jegyfoglalas(j2, "Kiss Péter", datetime(2026, 7, 1)))
    rendszer._foglalasok.append(jegyfoglalas(j2, "Nagy Eszter" , datetime(2026, 7, 7)))
    rendszer._foglalasok.append(jegyfoglalas(j3, "Sátoros Géza", datetime(2026, 8, 15)))
    rendszer._foglalasok.append(jegyfoglalas(j3, "Vörös Róza", datetime(2026, 8, 23)))

    return rendszer


# 4. felhasználói interfész

def main():
    rendszer = rendszerinicializalasa()

    while True:
        print(f"\n{rendszer._legitarsasag.nev} Rendszer")
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. foglalások listázása")
        print("4. Elérhető járatok megtekintése")
        print("0. Kilépés")

        valasztas = input("Kérlek, válassz egy menüpontot:  "). strip()

        if valasztas == "1":
            print("Jegy foglalása")
            utasnev = input("Utas nave: "). strip()
            if not utasnev:
                print("Hiba: Az utas neve nem lehet üres!")
                continue
            jaratszam = input("Járat száma (Pl.: RA-404):  "). strip()
            datumstr = input("Utazás dátuma (ÉÉÉÉ-HH-NN):  "). strip()

            try:
                rendszer.jegyfoglalasa(jaratszam, utasnev, datumstr)
            except ValueError as e:
                print(e)

        elif valasztas == "2":
            print(f"\nFoglalás lemondása")
            try:
                foglalas_id = int(input("Kérlek add meg a lemondani kívánt foglalás ID-ját!"))
                rendszer.foglalaslemondasa(foglalas_id)
                
            except ValueError as e:
                if "invalid literal for int()" in str(e):
                    print("Hiba: Kérjük, a számot add meg ID-ként!")
                else:
                    print(e)

        elif valasztas == "3":
            rendszer.foglalasoklistazasa()

        elif valasztas == "4":
            print(f"\nElérhető járataink:")
            for jarat in rendszer._legitarsasag.jaratok:
                print(jarat)

        elif valasztas == "0":
            print(f"\nKöszönjük, hogy a mi rendszerünket haszálta! Viszontlátásra!")
            break
        else:
            print("\nHibás menüpont, kérjük 0 és 4 közötti számot adj meg!")


if __name__ == "__main__":
    main()

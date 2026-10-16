# anagrammi.py
# Un assistente che ti aiuta a costruire anagrammi DI SENSO COMPIUTO.
#
# Regole del gioco:
#   - puoi usare solo le lettere della frase originale;
#   - ogni lettera si può usare al massimo tante volte quante compare;
#   - non serve usarle tutte: bastano da 80 a 104 lettere;
#   - gli accenti non contano ("è" vale come "e").
#
# Il senso della frase lo decidi tu: il programma conta le lettere,
# ti dice cosa avanza e ti suggerisce parole che ci stanno.

# "import" serve a usare codice già pronto incluso in Python.
import unicodedata                 # sa togliere gli accenti dalle lettere
from collections import Counter    # sa contare quante volte compare ogni lettera

# Le costanti (in MAIUSCOLO) sono valori che non cambiano mai.
FRASE = (
    "raffaele viti marketing manager di dàmeda è in ufficio a lentate "
    "sul seveso dal lunedì al venerdì tutte le settimane del mese"
)
MINIMO_LETTERE = 80
FILE_PAROLE = "parole.txt"              # dizionario di parole comuni
FILE_SALVATAGGI = "anagrammi_trovati.txt"


def pulisci(testo):
    """Tiene solo le lettere, in minuscolo e senza accenti: 'Dàmeda è' -> 'damedae'."""
    # NFD separa la lettera dal suo accento: "à" diventa "a" + "`".
    scomposto = unicodedata.normalize("NFD", testo.lower())
    # Teniamo solo le lettere normali (a-z), scartando accenti, spazi e punteggiatura.
    return "".join(c for c in scomposto if "a" <= c <= "z")


# Counter crea una specie di tabella: {'e': 20, 'a': 12, 't': 9, ...}
LETTERE_ORIGINALI = Counter(pulisci(FRASE))
MASSIMO_LETTERE = sum(LETTERE_ORIGINALI.values())    # 104


def confronta(tentativo):
    """Restituisce due tabelle: le lettere che avanzano e quelle in eccesso."""
    usate = Counter(pulisci(tentativo))
    rimaste = LETTERE_ORIGINALI - usate   # quello che resta della frase originale
    in_eccesso = usate - LETTERE_ORIGINALI  # lettere che non ci sono (o sono troppe)
    return rimaste, in_eccesso


def ci_sta(parola, rimaste):
    """True se la parola si può scrivere con le lettere rimaste."""
    return not (Counter(pulisci(parola)) - rimaste)


def carica_parole():
    """Legge il dizionario: una parola per riga, dalla più comune alla più rara."""
    try:
        with open(FILE_PAROLE, encoding="utf-8") as file:
            return [riga.strip() for riga in file if riga.strip()]
    except FileNotFoundError:
        print(f"(Non trovo {FILE_PAROLE}: niente suggerimenti, ma il resto funziona.)")
        return []


def suggerisci(parole, rimaste, inizio="", quante=40):
    """Trova fino a 'quante' parole che ci stanno e che iniziano con 'inizio'."""
    trovate = []
    for parola in parole:
        if parola.startswith(inizio) and ci_sta(parola, rimaste):
            trovate.append(parola)
            if len(trovate) == quante:
                break
    return trovate


def mostra_stato(tentativo):
    """Stampa la frase attuale e com'è messa con le lettere."""
    rimaste, in_eccesso = confronta(tentativo)
    usate = MASSIMO_LETTERE - sum(rimaste.values())

    print()
    print("La tua frase:", tentativo if tentativo else "(vuota)")
    print(f"Lettere usate: {usate} su {MASSIMO_LETTERE}")

    if in_eccesso:
        # sorted(...elements()) mette in fila le lettere: Counter({'p':1,'o':2}) -> o o p
        print("✗ Queste lettere non ci sono o sono troppe:",
              " ".join(sorted(in_eccesso.elements())))
    elif usate < MINIMO_LETTERE:
        mancano = MINIMO_LETTERE - usate
        print(f"… Ti servono ancora almeno {mancano}", "lettera." if mancano == 1 else "lettere.")
    else:
        print("✓ ANAGRAMMA VALIDO! Se ha senso, scrivi 'salva'.")

    print("Lettere rimaste:", " ".join(sorted(rimaste.elements())) or "nessuna")


def stampa_aiuto():
    print("""
Comandi:
  scrivi una frase    → diventa la tua frase
  + parole            → aggiunge parole in fondo alla frase
  -                   → toglie l'ultima parola
  ?                   → suggerisce parole che ci stanno
  ? ini               → suggerisce parole che iniziano con "ini"
  salva               → salva la frase in anagrammi_trovati.txt
  aiuto               → mostra questi comandi
  esci                → chiude il programma""")


def main():
    parole = carica_parole()
    tentativo = ""

    print("Frase originale:")
    print(" ", FRASE)
    print(f"Costruisci una frase sensata usando da {MINIMO_LETTERE} "
          f"a {MASSIMO_LETTERE} delle sue lettere.")
    stampa_aiuto()
    mostra_stato(tentativo)

    # while True ripete all'infinito, finché non incontra "break".
    while True:
        comando = input("\n> ").strip()

        if comando == "esci":
            print("Ciao!")
            break

        elif comando == "aiuto":
            stampa_aiuto()
            continue    # "continue" salta subito al giro successivo

        elif comando.startswith("?"):
            inizio = pulisci(comando[1:])
            rimaste, _ = confronta(tentativo)
            trovate = suggerisci(parole, rimaste, inizio)
            if trovate:
                print("Parole che ci stanno:", ", ".join(trovate))
            else:
                print("Nessuna parola trovata.")
            continue

        elif comando == "salva":
            _, in_eccesso = confronta(tentativo)
            usate = len(pulisci(tentativo))
            if in_eccesso or usate < MINIMO_LETTERE:
                print("Non è ancora un anagramma valido, non lo salvo.")
            else:
                # "a" = append: aggiunge in fondo al file senza cancellare il resto.
                with open(FILE_SALVATAGGI, "a", encoding="utf-8") as file:
                    file.write(tentativo + "\n")
                print(f"Salvato in {FILE_SALVATAGGI}!")
            continue

        elif comando.startswith("+"):
            tentativo = (tentativo + " " + comando[1:].strip()).strip()

        elif comando == "-":
            # rsplit(" ", 1) taglia la frase all'ultimo spazio: tiene tutto tranne l'ultima parola.
            tentativo = tentativo.rsplit(" ", 1)[0] if " " in tentativo else ""

        elif comando:
            tentativo = comando

        mostra_stato(tentativo)


# Fa partire main() solo quando esegui direttamente: python anagrammi.py
if __name__ == "__main__":
    main()

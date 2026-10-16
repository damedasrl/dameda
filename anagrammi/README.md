# Anagrammi

Assistente in Python per costruire **anagrammi di senso compiuto** della frase:

> raffaele viti marketing manager di dàmeda è in ufficio a lentate sul seveso dal lunedì al venerdì tutte le settimane del mese

## Regole

- Si usano solo le lettere della frase originale, ognuna al massimo tante volte quante compare.
- Non serve usarle tutte: un anagramma è valido se usa **da 80 a 104 lettere**.
- Gli accenti non contano ("è" vale come "e").
- Il senso della frase lo decide chi gioca: il programma conta le lettere e suggerisce parole.

## Come si usa

Serve Python 3 (https://www.python.org/downloads/). Dalla cartella del progetto:

```bash
python anagrammi.py
```

| Comando      | Cosa fa                                        |
|--------------|------------------------------------------------|
| una frase    | diventa la tua frase                           |
| `+ parole`   | aggiunge parole in fondo                       |
| `-`          | toglie l'ultima parola                         |
| `?`          | suggerisce parole che ci stanno                |
| `? ini`      | suggerisce parole che iniziano con "ini"       |
| `salva`      | salva la frase valida in `anagrammi_trovati.txt` |
| `esci`       | chiude il programma                            |

## Esempi di anagrammi validi

- *Il marketing di Dàmeda è fedele, veloce, attento e sa vendere a tutti in mille sfumature: fa un film di stile.* (86 lettere)
- *Il marketing di Dàmeda è fedele, veloce, attento e sa vendere a tutti in mille sfumature: svela e fa a Siena un film di grande stile.* (104 lettere)

## Fonti

`parole.txt` contiene circa 6.000 parole italiane comuni, ricavate da
[FrequencyWords](https://github.com/hermitdave/FrequencyWords) di Hermit Dave
(licenza MIT) e filtrate tenendo solo quelle compatibili con le lettere della frase.

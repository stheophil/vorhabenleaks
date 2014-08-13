Ein erster roher Parser für die von [netzpolitik.org](netzpolitik.org) geleakte [Liste der Vorhaben der Bundesregierung](https://netzpolitik.org/wp-upload/2014-07-22_BuReg-Vorhabendokumentation.txt).

`2014-07-22_BuReg-Vorhabendokumentation.txt` oder hoffentlich die folgenden Dokumentationen runterladen und 

    python parse.py 2014-07-22_BuReg-Vorhabendokumentation.txt > vorhabendoku.csv

oder 

	python parse.py 2014-07-22_BuReg-Vorhabendokumentation.txt json > vorhabendoku.json

aufrufen. Wenn sich das Tool beschwert, OCR Fehler beheben und nochmal laufen lassen. (Der Text auf netzpolitik.org hat zwei relevante OCR Fehler, die sich leicht beheben lassen.)
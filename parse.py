import urllib.request as request
import re
import difflib
import json
import csv
import sys

def error(*objs):
    print("FEHLER: ", *objs, file=sys.stderr)

if len(sys.argv) < 2 or 3<len(sys.argv):
	print("Syntax: ./parse.py datei_name [csv|json]")
	exit(1)

filename = sys.argv[1]
if len(sys.argv)==3:
	format = sys.argv[2]

listErgebnis = []

with open(filename, 'r', encoding = "UTF-8") as f:
	strVorhaben = f.read()
	rngstrVorhaben = re.split("\n(?=Vorhaben\n)", strVorhaben)

	for str in rngstrVorhaben[1:]:
		str = re.sub(r"[\n]+", "\n", str) 
		lines = re.split("\n", str)

		idx_titel = -1
		idx_inhalt = -1
		idx_zustimmung = -1
		idx_termin = -1
		idx_anmerkung = -1
		for (idx, line) in enumerate(lines):
			if difflib.SequenceMatcher(None, line, 'Vorhaben').ratio() > 0.8:
				idx_titel = idx

			if difflib.SequenceMatcher(None, line, 'Inhalt').ratio() > 0.8:
				idx_inhalt = idx

			if difflib.SequenceMatcher(None, line[0:line.find(":")], 'Zustimmungsbedürftigkeit Bundesrat').ratio() > 0.8:
				idx_zustimmung = idx

			if difflib.SequenceMatcher(None, line, 'Zeitplanung Termin').ratio() > 0.8 \
				or difflib.SequenceMatcher(None, line, 'Zeitplanung').ratio() > 0.8:
				idx_termin = idx

			if difflib.SequenceMatcher(None, line, 'Anmerkungen').ratio() > 0.8:
				idx_anmerkung = idx

		if idx_titel == -1 or idx_inhalt == -1 or idx_zustimmung == -1 or idx_termin == -1 or idx_anmerkung == -1 or \
			not (idx_titel<idx_inhalt and idx_inhalt<idx_zustimmung and idx_zustimmung < idx_termin and idx_termin < idx_anmerkung):
			error("Fehler beim Parsen von: \n")
			error(str)
			continue

		vorhaben = {}
		vorhaben['titel'] = " ".join(lines[idx_titel+1:idx_inhalt]).strip()
		vorhaben['inhalt'] = " ".join(lines[idx_inhalt+1:idx_zustimmung]).strip()
		lz = lines[idx_zustimmung]
		vorhaben['zustimmung_bundesrat'] = lz[lz.find(":")+1:].strip()

		vorhaben['termine'] = []
		for termin in lines[idx_termin+1:idx_anmerkung]:

			for i, c in enumerate(reversed(termin)):
				if c.isalpha():
					if 0<i:
						idx_date = len(termin) - i
						date = termin[idx_date:]
						date = re.sub(r"\s", "", date)
						vorhaben['termine'].append( { 
										 'gremium': termin[0:idx_date].strip(), 
										 'datum': date
										 })
					break

		vorhaben['anmerkung'] = " ".join(lines[idx_anmerkung + 1]).strip()

		listErgebnis.append(vorhaben)

if format=="json":
	json.dumps(listErgebnis)
else:
	# assume csv
	writer = csv.writer(sys.stdout)
	writer.writerow(["Titel", "Inhalt", "Zustimmungsbedürftigkeit Bundesrat", "1. Termin", "Letzter Termin", "Anmerkung"])
	for vorhaben in listErgebnis:
		termin_min, termin_max = "", ""
		termine = vorhaben['termine']
		if 0 < len(termine):
			termin_min = termine[0]['datum']
			termin_max = termine[len(termine) - 1]['datum']

		writer.writerow([
			vorhaben['titel'], 
			vorhaben['inhalt'], 
			vorhaben['zustimmung_bundesrat'], 
			termin_min, 
			termin_max,
			vorhaben['anmerkung']
		])

import urllib.request as request
import re
import difflib

vorhaben = request.urlopen("https://netzpolitik.org/wp-upload/2014-07-22_BuReg-Vorhabendokumentation.txt").read().decode("UTF-8")
avorhaben = re.split("\n(?=Vorhaben\n)", vorhaben)
for v in avorhaben[1:]:
	print("================================ Vorhaben ==========================\n")
	v = re.sub(r"[\n]+", "\n", v) 
	lines = re.split("\n", v)

	titel = -1
	inhalt = -1
	zustimmung = -1
	for (idx, line) in enumerate(lines):
		if difflib.SequenceMatcher(None, line, 'Vorhaben').ratio() > 0.8:
			titel = idx

		if difflib.SequenceMatcher(None, line, 'Inhalt').ratio() > 0.8:
			inhalt = idx

		if difflib.SequenceMatcher(None, line[0:line.find(":")], 'Zustimmungsbedürftigkeit Bundesrat').ratio() > 0.8:
			zustimmung = idx

		if difflib.SequenceMatcher(None, line, 'Zeitplanung Termin').ratio() > 0.8:
			termin = idx

		if difflib.SequenceMatcher(None, line, 'Anmerkungen').ratio() > 0.8:
			anmerkungen = idx

	print("Titel: " + " ".join(lines[titel+1:inhalt]))
	print("Inhalt: " + " ".join(lines[inhalt+1:zustimmung]))
	lz = lines[zustimmung]
	print("Zustimmung Bundesrat: " + lz[lz.find(":")+1:])

	termine = lines[termin+1:anmerkungen]
	for t in termine:
		date_index = -1
		for i, c in enumerate(reversed(t)):
			if c.isalpha():
				date_index = len(t) - i
				break

		print("Termin " + t[0:date_index] + " = " + t[date_index:])

	print("\n")

print("Liste enthält %d Vorhaben der Bundesregierung\n" % (len(avorhaben)-1))
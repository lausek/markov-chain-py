Zu Simulationszwecken wird ein Unternehmensnetzwerk als EventBus dargestellto .
An dieses Unternehmensnetzwerk sind fünf Zweigstellen [i] BranchHKG, [ii] BranchCPT, [iii] BranchSFO,[iv] BranchSYD und [v] und BranchWUH angeschlossen .
Zwischen den Zweigstellen werden verschlüsselte Nachrichten ausgetauscht .
Für die Verschlüsselung stehen ein klassisches Verfahren und RSA zur Verfügung .
Die kryptographischen Algorithmen sind in austauschbaren Komponenten gekapselt .
Die Komponenten als jar sind digital signiert .
Nur Komponenten mit valider digitaler Signatur können geladen werden .
Der Schlüssel für die Verschlüsselung / Entschlüsselung sind in geeigneten Konfigurationsdateien im Format JSON zu speichern .
Bei dem Start der Applikation werden bereits definierte Channel automatisch aufgebaut .
Durch Drücken der Taste wird der Debug-Modus aktiviert oder deaktiviert .
Bei aktiviertem Debug-Modus wird bei Ausführung der Befehle encrypt message und decrypt message im Verzeichnis log eine Logdatei .
txtangelegt .
Diese Logdatei zeichnet die Schritte detailliert und nachvollziehbar auf .
Durch Drücken der Taste wird das Logfile mit dem neuesten Zeitstempel in den Ausgabebereich der GUI geladen und angezeigt .
Die Applikation wird über CQL gesteuert .
Durch Mausklick auf den Button execute in der GUI oder Drücken der Taste [F5] wird der Befehl ausgeführt .
Die verschlüsselte Meldung wird im Ausgabebereich der GUI angezeigt .
Die entschlüsselte Meldung wird im Ausgabebereich der GUI angezeigt .
Wurde die Meldung innerhalb der Zeitvorgabe entschlüsselt , wird die entschlüsselte Meldung im Ausgabebereich der GUI angezeigt .
Wurde die Meldung nicht innerhalb der Zeitvorgabe entschlüsselt , erfolgt die Meldung im Ausgabebereich der GUI .
Existiert kein Teilnehmer mit diesem Namen wird ein Datensatz in der Tabelle angelegt .
Im Ausgabebereich der GUI wird die Meldung angezeigt .
Existiert ein Teilnehmer mit diesem Namen wird die Meldung im Ausgabebereich der GUI angezeigt .
Für die Simulation werden folgende participants angelegt .
Für die bidirektionale Kommunikation bzw. das Senden von verschlüsselten Nachrichten zwischen Participant vom Typ normal ist ein Channel notwendig .
Existiert bereits ein Channel mit dem Namen wird die Fehlermeldung im Ausgabebereich der GUI angezeigt .
Existiert bereits eine Kommunikationsbeziehung zwischen participant01 und participant02 , wird die Fehlermeldung im Ausgabebereich der GUI angezeigt .
Sind participant01 und participant02 identisch , wird die Fehlermeldung im Ausgabebereichder GUI angezeigt .
Existiert kein Channel mit dem Namen und keine Kommunikationsbeziehung zwischen den beiden participant , wird ein Datensatz in der Tabelle channel angelegt und die Meldung im Ausgabebereich der GUI angezeigt .
Nach erfolgreicher Erstellung eines channel erfolgt die Meldung im Ausgabebereich der GUI , in der Tabelle channel wird ein Datensatz angelegt .
Für die Simulation werden folgende channel angelegt .
Existiert kein channel mit dem Namen, wird im Ausgabebereich der GUI die Fehlermeldung ausgegeben .
Bei Erhalt einer Nachricht wird in der Tabelle postbox des intruder ein neuer Datensatz erstellt , das Attribut message wird auf den Wert unknown gesetzt .
Der participant lädt dynamisch die zu dem Algorithmus korrespondierende Komponente und versucht innerhalb von maximal 30 Sekunden die Meldung zu entschlüsseln .
Wird innerhalb der Zeitvorgabe die Nachricht erfolgreich entschlüsselt , wird das Attribut message auf den Wert der Meldung im Klartext gesetzt .
Im Fall einer erfolgreichen Entschlüsselung wird im Ausgabebereich der GUI die Meldung angezeigt .
Im Fall einer nicht erfolgreichen Entschlüsselung wird im Ausgabebereich der GUI die Meldung angezeigt .
Existiert zwischen participant01 und participant02 kein channel , wird die Fehlermeldung im Ausgabebereich der GUI angezeigt .
Existiert zwischen participant01 und participant02 ein channel wird die Nachricht mit dem Algorithmus und keyfile verschlüsselt und über den Channel kommuniziert .
Das Versenden der Nachricht wird in der Tabelle messages protokolliert .
Der Empfänger participant02 lädt dynamisch die zu dem Algorithmus korrespondierende Komponente und entschlüsselt die Nachricht .
Nach Entschlüsselung wird in der Tabelle ein Datensatz erstellt und im Ausgabebereich der GUI die Meldung angezeigt

Dieses Dokument dient dazu, die einzelnen Zeilen des GitHub Workflows zu erklären.

    name: Automatische Bewertung des Jupyter Notebooks 
    --> Name des Workflows, welche unter GitHub Actions angezeigt wird.

    on:
    push:
        branches:
        - main 
    --> Definition des Events, welches getriggered werden muss, damit die nachfolgenden Jobs ausgeführt werden
    --> bei einem Push auf den main Branch

    jobs:
    check_cell:
    --> Name des ersten Jobs
        runs-on: ubuntu-latest
        --> Angabe auf welchem Betriebssystem der Job ausgeführt werden soll
        --> die neueste Version von Ubuntu in einer virutellen Umgebung
        permissions:
        contents: write
        --> Definition von Berechtigungen
        --> mittels write auf contents erhält der Workflow ein Schreibrecht auf das Repository (um die erstelle Textdatei auf das Repository zu pushen)

    steps:
    --> da der Job aus mehreren Abfolgen besteht, werden diese in verschiedene Steps unterteilt
      - name: Repository auschecken
        uses: actions/checkout@v3
        --> eine vorgefertigte GitHub Action, mit der der Code aus dem Repository in die virtuelle Maschine (Runner) zu laden, ohne diese  Angabe könnte der Workflow nicht auf die Daten des Repositorys zugreifen

      - name: Installiere Abhängigkeiten
        run: pip install nbformat
        --> führt den angegebenen Shell-Befehl aus, um die Python Bibliothek nbformat zu installieren, mit der Jupyter Notebooks analysiert und verarbeitet werden können; ohne diesen Befehl, könnte das darauffolgende Python Programm nicht ausgeführt werden

      - name: Suche nach Markierung im Jupyter Notebook
        run: python check_notebook_marker.py
        --> führt die Python-Datei, welche sich im Repo befindet, aus 

      - name: Pushe die result.txt ins Repository
        run: |
        --> senkrechter Strich als Shell-Befehl welcher angibt, dass nun mehrere Shell-Befehle nacheinander ausgeführt werden sollen
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          --> beide Schritte dienen der Konfiguration eine Git-Nutzes, welche den darauffolgenden Commits zugeordnet werden (ohne diese, könnten keine Commits aus das Repp erfolgen, da Git diese einem Nutzer zuweisen muss)
          git add result.txt
          --> die innerhalb der Python-Datei erstellte result.txt wird für den nächsten Commit registiert
          git commit -m "Überprüfung, ob gesuchte Zelle vorhanden ist, erfolgreich." --allow-empty
          --> erstellt einen neuen Git-Commit mit der eingegebenen Nachricht, zusätzlich wird mittels allow-empty angegeben, dass auch dann ein Commit erstellt werden darf, wenn keine Änderungen bezüglich der result.txt festzustellen sind; ohne eine Änderung an der Datei würde sonst kein Commit erstellt werden
          git pull --rebase origin main || (git rebase --abort && echo "Rebase fehlgeschlagen, führe stattdessen Merge durch")
          --> der erste Befehl versucht, die neuesten Änderungen aus dem main Branch zu pullen und in den aktuellen Stand einzuführen
          --> der zweite Befehl wir dann ausgeführt, wenn beim ersten ein Fehler auftritt, dieser bricht --rebase ab und gibt den Text wieder, dass ein normaler Merge durhcgeführt werden soll
          git pull --no-rebase
          --> hiermit wird ein normale Git-Pull ausgeführt 
          git push
          --> pusht den neu erstellten Commit mitsamt der result.txt in das Repo

      - name: Speichere result.txt als Artifact
      --> Artifacts sind Dateien, die zwischen verschiedenen Jobs oder Runs in GitHub Actions gespeichert und abgerufen werden können
        uses: actions/upload-artifact@v4
        --> Verwendung einer vorgefertigten GitHub Actions zum Hochladen des Artifacts, welches vom nächsten Job benutzt werden soll
        with:
          name: result-file
          path: result.txt

    bewerten_notebook:
        runs-on: ubuntu-latest
        permissions:
        contents: write
        needs: check_cell
        --> diese Job wird erst ausgeführt, wenn der Job mit dem Namen check_cell ausgeführt wurde

    steps:
      - name: Lade result.txt herunter
        uses: actions/download-artifact@v4
        with:
          name: result-file

      - name: Repository auschecken
        uses: actions/checkout@v3

      - name: Installiere Abhängigkeiten
        run: pip install nbformat

      - name: Führe Code aus und bewerte das Ergebnis
        run: python check_solution.py

      - name: Pushe die Bewertung.txt ins Repository
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add Bewertung.txt
          git commit -m "Ausführen und Bewerten der Lösung erfolgreich ausgeführt." --allow-empty
          git pull --rebase origin main || (git rebase --abort && echo "Rebase fehlgeschlagen, führe Merge durch")
          git pull --no-rebase
          git push

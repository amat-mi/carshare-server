# carshare-server

Django app per la gestione dei dati del CarSharing, che li recupera dal PINF e li memorizza in AMAT.

ATTENZIONE!!! Si basa su Django ma, al momento, non ne esegue alcuna istanza, ma si limita ad usarne l'ORM
tramite un management command che, richiamato da un crontab, recupera i dati e li inserisce nel database!!!

Volendo si potrebbe integrarlo "sotto" django-amat-dati...

ATTENZIONE!!! I provider di Car Sharing hanno cambiato qualcosa nelle loro API o nelle credenziali
per cui al momento, di fatto, il PINF non Ë pi˘ in grado di ottenere i dati e quindi nemmeno questo software!!!

# Installazione

## Windows

Creare un virtualenv con python3, per esempio:

    virtualenv3 c:\Users\Paolo\venv\carshare-server

Clonare i repository necessari:

    cd c:\Users\Paolo\git\AMAT
    git clone https://github.com/amat-mi/carshare-server.git
    
__ATTENZIONE!!!__ Se necessario fare git switchout sul branch opportuno!!!

Attivare il virtualenv ed installare i requirements:

    c:\Users\Paolo\venv\carshare-server\Scripts\activate.bat
    cd c:\Users\Paolo\git\AMAT\carshare-server
    pip install -r requirements.txt
    c:\Users\Paolo\venv\carshare-server\Scripts\deactivate.bat
    
## Ubuntu

Creare virtual env per il progetto:
	
    virtualenv /var/www/django/venv/carshare-server

Clonare i repository necessari:

    cd /var/www/django/projects
    git clone https://github.com/amat-mi/carshare-server.git
    
__ATTENZIONE!!!__ Se necessario fare git switchout sul branch opportuno!!!

Attivare il virtualenv ed installare i requirements:

    . /var/www/django/venv/carshare-server/bin/activate
    cd /var/www/django/projects/carshare-server
    pip install -r requirements.txt
    deactivate

Eseguire da cron ogni tot minuti, per esempio:

    crontab -e
    
    ############################################################
    # Eseguo script di scaricamento dati del Car Sharing ogni 5 minuti
    ############################################################

    2,7,12,17,22,27,32,37,42,47,52,57 * * * * /var/www/django/carshare_retrieve.sh 2>&1 >> /var/www/django/carshare_retrieve.log

ATTENZIONE!!! Dato che al momento il PINF non Ë in grado di ottenere i dati, Ë inutile eseguire questo software!!!

## License

TBD
All rights reserved Agenzia Mobilit√† Ambiente e Territorio - Milano

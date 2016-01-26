# carshare-server

Django app per la gestione dei dati del CarSharing

Eseguire da cron ogni tot minuti, per esempio:

    crontab -e
    
    ############################################################
    # Eseguo script di scaricamento dati del Car Sharing ogni 5 minuti
    ############################################################

    2,7,12,17,22,27,32,37,42,47,52,57 * * * * /var/www/django/carshare_retrieve.sh 2>&1 >> /var/www/django/carshare_retrieve.log

## License

TBD
All rights reserved Agenzia Mobilità Ambiente e Territorio - Milano

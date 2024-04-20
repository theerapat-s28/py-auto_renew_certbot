# Python Auto Renew Certbot Using Docker Compose Method

Configure hostname information in the settings.py file. This application iterates
 through the list of hostnames and checks if the SSL certificate expiry is less
 than 15 days to automatically renew the certbot using a specific compose file.
 Set up a cron job to run this application weekly.

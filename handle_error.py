import logger
import settings
import os

ERROR_LOG_FILE = os.path.join(settings.LOG_FOLDER_PATH, "cron_error.log")


def get_ssl_date_expiry_error(hostname:str) -> None:
    logger.write(ERROR_LOG_FILE, f"Failed attempt on getting expiry date for {hostname}.")


def renew_with_dockercompose_error(dc_file:str) -> None:
    logger.write(
        ERROR_LOG_FILE, 
        f"Failed attempt on renew certbot with docker-compose {dc_file}"
    )
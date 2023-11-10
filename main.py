import subprocess, os
import settings, hostname_list
import logger

import https


def main():
  # log_file = os.path.join(settings.LOG_FOLDER_PATH, "cron.log")
  
  # if not os.path.exists(log_file):
  #   logger.create_new_file(log_file)

  # logger.write(log_file, 'Hello Cron')
  print(https.ssl_days_left(hostname_list.HOSTNAMES[0]['name']))


if __name__ == "__main__":
	main()
import subprocess, os
import settings
import logger


def main():
  log_file = os.path.join(settings.LOG_FOLDER_PATH, "cron.log")
  
  if not os.path.exists(log_file):
    logger.create_new_file(log_file)

  logger.write(log_file, 'Hello Cron')


if __name__ == "__main__":
	main()
# Python modules
import subprocess, os, time

# Local modules
import settings
import handle_error
import logger
import https


def run_command_with_output(command) -> str:
    """
    Run a command and collect its output as a string.
    
    Parameters:
        command (str): The command to run.

    Returns:
        str: The output of the command as a string.
    """
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        raise Exception(e.output)


def restart_reverse_proxy(compose_file:str, service_name:str):
  '''
  Restart reverse proxy container of given docker compose file and name.

  Parameters:
    - compose_file   (str) : Docker compose file location
    - service_name (str) : Reverse proxy container name to be restart.
  '''

  try:
    subprocess.run(
      f'docker-compose -f {compose_file} stop {service_name}', 
      shell=True, 
      capture_output=True, 
      text=True, 
      check=True
    )
    subprocess.run(
      f'docker-compose -f {compose_file} up -d --force-recreate --no-deps {service_name}', 
      shell=True, 
      capture_output=True, 
      text=True, 
      check=True
    )
  except:
    error_log_file = os.path.join(settings.LOG_FOLDER_PATH, "cron_error.log")
    logger.write(error_log_file, f"Failed attempt restart reverse proxy.")


def renew_docker_certbot(compose_file:str, certbot_service_name:str) -> None:
  '''
  Run docker compose file and check the result with sentence "certbot exited with code 0"
  to confirmed the successful.

  Parameters:
    - compose_file (str) : Docker compose file location.
  '''
  command = f"docker-compose -f {compose_file} up --force-recreate --no-deps {certbot_service_name}"
  output = run_command_with_output(command)

  if "exited with code 0" not in output:
    handle_error.renew_with_dockercompose_error(compose_file)


def main():
  success_log_file = os.path.join(settings.LOG_FOLDER_PATH, "cron_success.log")
  error_log_file = os.path.join(settings.LOG_FOLDER_PATH, "cron_error.log")

  for hostname in settings.HOSTNAMES:
    name = hostname['name']
    cert_dc_file = hostname['cert_dc_file']
    cert_service_name = hostname['certbot_service_name']
    rvp_dc_file = hostname['rvp_dc_file']
    rvp_service_name = hostname['reverse_proxy_service_name']

    # Check SSL days left
    try:
      ssl_days_left = https.ssl_days_left(name)
      if ssl_days_left < 15:
        renew_docker_certbot(cert_dc_file, cert_service_name)
        time.sleep(5)
        restart_reverse_proxy(rvp_dc_file, rvp_service_name)
        time.sleep(10)
        ssl_days_left_after = https.ssl_days_left(name)
        if ssl_days_left_after > 80:
          logger.write(success_log_file, f"Successful renew SSL for {name}.")
        else:
          logger.write(error_log_file, f"SSL days after renew checking failed for {name}.")

    except:
      logger.write(error_log_file, f"Failed attempt on renew SSL for {name}.")


if __name__ == "__main__":
	main()
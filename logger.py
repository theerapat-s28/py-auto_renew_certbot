from datetime import datetime
import subprocess, csv, os


def write(file_path, message) -> None:
  '''
    Get time and user information then insert the data into given log file path.
  File to be write in csv format with header ['TIME', 'USER', 'MESSAGE']. If file
  is not exists at the first place, its will create and write to the given location.

  Parameters:
    - file_path (str) : Log file location.
    - message   (str) : Log message.
  '''

  # Check if file not exists
  if not os.path.exists(file_path):
    _create_new_file_with_header(file_path)

  now = datetime.now()
  date_time = now.strftime("%Y/%d/%m-%H:%M:%S")

  p = subprocess.run('whoami', shell=True, stdout=subprocess.PIPE, text=True)
  user = p.stdout.strip() #.strip() is removing /n (newline) from string

  with open(file_path, 'a', encoding='utf-8') as f:
    msg = [date_time, user, message]
    csv_writer = csv.writer(f)
    csv_writer.writerow(msg)


def _create_new_file_with_header(file_path) -> None:
  '''
    Create new csv file for logging with specific header.

    Parameters:
      - file_path (str) : csv file location.
  '''

  with open(file_path, 'w', encoding='utf-8') as f:
    header = ['TIME', 'USER', 'MESSAGE']
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
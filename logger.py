from datetime import datetime
import subprocess, csv


def create_new_file(file_path):
  with open(file_path, 'w', encoding='utf-8') as f:
    header = ['TIME', 'USER', 'MESSAGE']
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)

def write(file_path, message):
  now = datetime.now()
  date_time = now.strftime("%Y/%d/%m-%H:%M:%S")

  p = subprocess.run('whoami', shell=True, stdout=subprocess.PIPE, text=True)
  user = p.stdout.strip() #.strip() is removing /n (newline) from string

  with open(file_path, 'a', encoding='utf-8') as f:
    msg = [date_time, user, message]
    csv_writer = csv.writer(f)
    csv_writer.writerow(msg)
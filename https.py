import socket
import ssl
import datetime
import handle_error


def ssl_days_left(hostname) -> int:
  '''
  Return SSL expiry date left of given hostname.
  '''

  try:
    now = datetime.datetime.now()
    expiry_date = _ssl_expiry_datetime(hostname)

    diff = expiry_date - now
    return diff.days
  except ssl.SSLCertVerificationError as e:
    if 'certificate has expired' in e.strerror:
      print("@ssl_days_left() - Certificate has expired")
      return 0
    else:
      handle_error.get_ssl_date_expiry_error(hostname)
      raise Exception(f"Failed attempt getting expiry date of {hostname} in _ssl_expiry_datetime() error.")
  except Exception:
    handle_error.get_ssl_date_expiry_error(hostname)
    raise Exception(f"Failed attempt getting expiry date of {hostname} in _ssl_expiry_datetime() error.")

def _ssl_expiry_datetime(hostname) -> datetime.datetime:
  format = r'%b %d %H:%M:%S %Y %Z'

  context = ssl.create_default_context()
  context.check_hostname = False

  conn = context.wrap_socket(
      socket.socket(socket.AF_INET),
      server_hostname=hostname,
  )
  # 5 second timeout
  conn.settimeout(5.0)

  conn.connect((hostname, 443))
  ssl_info = conn.getpeercert()
  return datetime.datetime.strptime(ssl_info['notAfter'], format) # type: ignore
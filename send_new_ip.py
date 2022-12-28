def Main():
    """
    Checks to see if the public IP has changed and alerts by email if this is the case
    """
    from gmail_account import USER, PASSWORD, PROVIDER, TO
    from requests import get
    from smtplib import SMTP_SSL
    from ssl import create_default_context
    from os import path
    from datetime import datetime
    from email.mime.text import MIMEText

    ip_file = "./current_ip.txt"
    svr = "smtp.gmail.com"
    port = "465"
    ip = get("https://api.ipify.org/").text
    cur_ip = ""

    if not path.exists(ip_file):
        with open(ip_file, 'w') as ipFile:
            ipFile.write(ip)
        
        with open("ip_log", 'w') as log_file:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_file.write(f"{now}: Notifier started - IP is {ip}\n")

    with open(ip_file, 'r') as ipFile:
        cur_ip = ipFile.read()

    if ip != cur_ip:
        from_address = f"{USER}{PROVIDER}"
        to_address = [f"{TO}+server{PROVIDER}"]

        msg = MIMEText(f"Your IP has changed to {ip}")
        msg['subject'] = "new IP"
        msg['from'] = from_address
        msg['to'] = ", ".join(to_address)
        
        try:
            with SMTP_SSL(svr, port) as server:
                server.login(user=USER, password=PASSWORD)
                server.sendmail(from_addr=from_address, to_addrs=to_address, msg=msg.as_string())
        except Exception as err:
            with open("ip_log", 'a') as log_file:
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                log_file.write(f"{now}: ERROR - {err}\n")
        
        with open(ip_file, 'w') as ipFile:
            ipFile.write(ip)

        with open("ip_log", 'a') as log_file:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_file.write(f"{now}: IP changed to {ip}\n")


if __name__ == "__main__":
    from datetime import datetime

    Main()

    """
    Overwrites the last run log
    """
    with open("last_run", 'w') as run_file:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        run_file.write(f"Last run: {now}\n")

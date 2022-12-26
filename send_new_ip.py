def Main():
    from gmail_account import USER, PASSWORD, PROVIDER
    from requests import get

    from smtplib import SMTP_SSL
    from ssl import create_default_context

    from os import path

    ip_file = "./current_ip.txt"

    svr = "smtp.gmail.com"
    port = "465"

    ip = get("https://api.ipify.org/").text
    cur_ip = ""

    if not path.exists(ip_file):
        f = open(ip_file, 'w')
        f.close()

    with open(ip_file, 'r') as ipFile:
        cur_ip = ipFile.read()

    if ip != cur_ip:
        msg = f"""Subject: new IP
        Your IP has changed to {ip}"""

        cnt = create_default_context()

        with SMTP_SSL(svr, port, context=cnt) as server:
            server.login(user=USER, password=PASSWORD)
            from_address = f"{USER}{PROVIDER}"
            to_address = f"{USER}+server{PROVIDER}"

            server.sendmail(from_addr=from_address, to_addrs=to_address, msg=msg)
        
        with open(ip_file, 'w') as ipFile:
            ipFile.write(ip)

if __name__ == "__main__":
    Main()
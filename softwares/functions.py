import smbclient
from django.conf import settings

def store():
    user = settings.SMB_USER
    password = settings.SMB_PASSWD
    server_name = settings.SMB_SERVER
    domain = settings.SMB_DOMAIN
    conn = smbclient.SambaClient(server=server_name, 
                                 share="Pasta p",
                                 username=user,
                                 password=password,
                                 domain=domain)     
    

    return conn
    
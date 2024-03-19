from ldap3 import Server, Connection, SAFE_SYNC, SUBTREE

def testar_acesso_ad():
    try:
        # Conecta ao servidor AD
        server = Server('ad_ip')
        conn = Connection(server, 'domain\\user', 'senha', client_strategy=SAFE_SYNC, auto_bind=True)
        conn.search('OU=dir ,DC=domain,DC=nf', '(objectCategory=user)')
        if conn.entries:
            print("Usuários encontrados:")
            for entry in conn.entries:
                print(entry)
            return True
        else:
            print("Nenhum usuário encontrado.")
            return False
    except Exception as e:
        # Em caso de erro, retorna False
        print(f"Erro ao tentar conectar ao AD: {e}")
        return False

# Testa a função
if testar_acesso_ad():
    print("Conexão ao AD bem-sucedida!")
else:
    print("Falha ao conectar ao AD. Verifique suas credenciais ou configurações de rede.")
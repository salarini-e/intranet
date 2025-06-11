from django.db import connection
from .models import Chamado, TipoChamado, Secretaria

def debug_tutorial(extra_msg=""):
    tutorial = (
        "Mini Tutorial de Comandos Debug:\n"
        "- query: <SQL SELECT> — Executa uma consulta SQL (apenas SELECT).\n"
        "- cmd: show from <nome da secretaria do requisitante> — Lista chamados cujo requisitante pertence à secretaria informada.\n"
        "- cmd: count chamados <tipo> — Conta chamados do tipo informado (ou todos se não informado).\n"
        "- cmd: tipos — Lista todos os tipos de chamados.\n"
        "- cmd: tables (ou tabelas) — Lista todas as tabelas do banco de dados.\n"
        "- help — Mostra este tutorial.\n"
        "Exemplos:\n"
        "  query: SELECT count(*) FROM chamados_chamado WHERE status='0' LIMIT 10;\n"
        "  cmd: show from SECRETARIA DE BEM-ESTAR E PROTEÇÃO ANIMAL\n"
        "  cmd: count chamados Impressora\n"
        "  cmd: tipos\n"
        "  cmd: tables\n"
        "Digite o comando desejado e pressione 'Run Debug'."
    )
    return f"{extra_msg}<pre style='background:#f5f5f5;padding:8px;border-radius:4px;'>{tutorial}</pre>"

def debug_query_command(comando):
    sql = comando.strip()
    query_out = f"<div style='background:#f5f5f5;padding:8px;border-radius:4px;margin-bottom:8px;'><b>Query enviada:</b><br><code style='font-size:1.1em'>{sql}</code></div>"
    if not sql.lower().startswith('select'):
        return f"{query_out}<div style='color:#b00;'>Apenas comandos SELECT são permitidos por segurança.</div>"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description] if cursor.description else []
        if not rows:
            result_main = "<i>Nenhum resultado encontrado.</i>"
        else:
            result_main = "<pre style='background:#fff;border:1px solid #ccc;padding:8px;overflow-x:auto;'>"
            if columns:
                result_main += "| " + " | ".join(columns) + " |\n"
                result_main += "|-" + "-|-".join('-'*len(c) for c in columns) + "-|\n"
            for row in rows:
                result_main += "| " + " | ".join(str(col) for col in row) + " |\n"
            result_main += "</pre>"
        return f"{query_out}{result_main}"
    except Exception as e:
        return f"{query_out}<div style='color:#b00;'>Erro ao executar query: {e}</div>"

def debug_show_from_command(cmd):
    cmd_out = f"<div style='background:#f5f5f5;padding:8px;border-radius:4px;margin-bottom:8px;'><b>Comando enviado:</b><br><code style='font-size:1.1em'>{cmd}</code></div>"
    secretaria_nome = cmd[10:].strip()
    secretaria = Secretaria.objects.filter(nome__iexact=secretaria_nome).first()
    if not secretaria:
        return f"{cmd_out}<div style='color:#b00;'>Secretaria '{secretaria_nome}' não encontrada.</div>"
    chamados = Chamado.objects.filter(requisitante__setor__secretaria=secretaria)
    if chamados.exists():
        result = "<pre style='background:#fff;border:1px solid #ccc;padding:8px;overflow-x:auto;'>"
        result += "| Protocolo | Assunto | Status |\n"
        result += "|-----------|---------|--------|\n"
        for chamado in chamados[:20]:
            result += f"| {chamado.n_protocolo} | {chamado.assunto} | {chamado.get_status_display()} |\n"
        if chamados.count() > 20:
            result += f"... e mais {chamados.count() - 20} chamados.\n"
        result += "</pre>"
        return f"{cmd_out}{result}"
    else:
        return f"{cmd_out}<i>Nenhum chamado encontrado para a secretaria '{secretaria_nome}'.</i>"

def debug_count_chamados_command(cmd):
    cmd_out = f"<div style='background:#f5f5f5;padding:8px;border-radius:4px;margin-bottom:8px;'><b>Comando enviado:</b><br><code style='font-size:1.1em'>{cmd}</code></div>"
    tipo_nome = cmd[14:].strip()
    if tipo_nome:
        tipo = TipoChamado.objects.filter(nome__iexact=tipo_nome).first()
        if tipo:
            count = Chamado.objects.filter(tipo=tipo).count()
            return f"{cmd_out}Total de chamados do tipo '<b>{tipo.nome}</b>': <b>{count}</b>"
        else:
            return f"{cmd_out}<div style='color:#b00;'>Tipo '{tipo_nome}' não encontrado.</div>"
    else:
        tipos = TipoChamado.objects.all()
        result = "<pre style='background:#fff;border:1px solid #ccc;padding:8px;overflow-x:auto;'>"
        result += "| Tipo | Quantidade |\n"
        result += "|------|------------|\n"
        for tipo in tipos:
            count = Chamado.objects.filter(tipo=tipo).count()
            result += f"| {tipo.nome} | {count} |\n"
        result += "</pre>"
        return f"{cmd_out}{result}"

def debug_tipos_command(cmd):
    cmd_out = f"<div style='background:#f5f5f5;padding:8px;border-radius:4px;margin-bottom:8px;'><b>Comando enviado:</b><br><code style='font-size:1.1em'>{cmd}</code></div>"
    tipos = TipoChamado.objects.all()
    result = "<pre style='background:#fff;border:1px solid #ccc;padding:8px;overflow-x:auto;'>"
    result += "| Nome | Sigla |\n"
    result += "|------|-------|\n"
    for t in tipos:
        result += f"| {t.nome} | {t.sigla} |\n"
    result += "</pre>"
    return f"{cmd_out}{result}"

def debug_tables_command(cmd):
    cmd_out = f"<div style='background:#f5f5f5;padding:8px;border-radius:4px;margin-bottom:8px;'><b>Comando enviado:</b><br><code style='font-size:1.1em'>{cmd}</code></div>"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = [t[0] for t in cursor.fetchall()]
        # Agrupar por app (prefixo antes do primeiro "_")
        from collections import defaultdict
        grouped = defaultdict(list)
        for table in tables:
            if "_" in table:
                app, rest = table.split("_", 1)
            else:
                app, rest = "outros", table
            grouped[app].append(table)
        # Montar HTML vertical agrupado
        result = "<div style='margin-top:8px;'><b>Tabelas do banco de dados agrupadas por app:</b></div>"
        result += "<div style='margin-top:8px;'>"
        for app in sorted(grouped.keys()):
            result += f"<div style='margin-bottom:8px;'><span style='font-weight:bold;color:#007AFF'>{app}</span><ul style='margin:0 0 0 16px;padding:0;'>"
            for table in sorted(grouped[app]):
                result += f"<li style='font-family:monospace;font-size:1em;padding:2px 0;'>{table}</li>"
            result += "</ul></div>"
        result += "</div>"
        return f"{cmd_out}{result}"
    except Exception as e:
        return f"{cmd_out}<div style='color:#b00;'>Erro ao executar SHOW TABLES: {e}</div>"

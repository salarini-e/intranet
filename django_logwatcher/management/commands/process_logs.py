import os
import re
from django.core.management.base import BaseCommand
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import make_aware
import datetime
from django_logwatcher.models import ApacheAccessLog, ApacheErrorLog

distro = 'apache2'
LOG_FILE = f"/var/log/{distro}/access.log"  # Ajuste conforme necessário
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<url>.*?) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\S+)'
)


ERROR_LOG_FILE = f"/var/log/{distro}/error.log"  # Ajuste conforme necessário
ERROR_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>[A-Za-z]{3} [A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2}\.\d{6} \d{4})\] \[(?P<module>[^\]]+)\] \[pid (?P<pid>\d+)\] \[(?P<level>[^\]]+)\] \[client (?P<client>[^\]]+)\] (?P<message>.+)$')

def process_log_file(file_path):
    with open(file_path, "r") as file:
        logs = []
        for line in file:
            match = LOG_PATTERN.match(line)
            if match:
                data = match.groupdict()
                # Ajuste do timestamp para considerar o fuso horário
                timestamp_str = data["timestamp"]
                # Remove espaços extras no fuso horário
                timestamp_str = timestamp_str.replace(" :", ":")  # Corrige o espaço extra
                timestamp = datetime.datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
                data["timestamp"] = make_aware(timestamp)
                data["size"] = int(data["size"]) if data["size"].isdigit() else 0
                logs.append(data)
            else:
                print("Linha não correspondida:", line)  # Para depuração
        return logs

def parse_log_line(line):
    match = ERROR_LOG_PATTERN.match(line)
    if match:
        data = match.groupdict()
        timestamp = datetime.datetime.strptime(data["timestamp"], "%a %b %d %H:%M:%S.%f %Y")
        data["timestamp"] = make_aware(timestamp)
        data["pid"] = int(data["pid"])
        # Dividir client para extrair o IP e port, se necessário
        data["client_ip"] = data["client"]
        data["client_port"] = None  # Defina como None, ou se tiver informações, extraia o que precisar
        return data
    return None


def read_logs():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                log_entry = parse_log_line(line)
                if log_entry:
                    logs.append(log_entry)
    return logs

def log_view(request):
    logs = read_logs()
    return render(request, "logs.html", {"logs": logs})


def parse_error_log_line(line):
    match = ERROR_LOG_PATTERN.match(line)
    if match:
        data = match.groupdict()
        # Converte o timestamp para o formato datetime
        timestamp = datetime.datetime.strptime(data["timestamp"], "%a %b %d %H:%M:%S.%f %Y")
        data["timestamp"] = make_aware(timestamp)  # Torna o timestamp ciente do fuso horário
        data["pid"] = int(data["pid"])  # Converte o pid para inteiro
        return data
    return None


def read_error_logs():
    logs = []
    if os.path.exists(ERROR_LOG_FILE):
        with open(ERROR_LOG_FILE, "r") as f:
            for line in f:
                log_entry = parse_error_log_line(line)
                if log_entry:
                    logs.append(log_entry)
    return logs

def process_error_logs():
    logs = read_error_logs()
    bulk_data = []
    for log in logs:
        bulk_data.append(
            ApacheErrorLog(
                timestamp=log["timestamp"],
                level=log["level"],
                pid=log["pid"],
                client_ip=log["client_ip"],
                client_port=log["client_port"],
                message=log["message"]
            )
        )
    if bulk_data:
        ApacheErrorLog.objects.bulk_create(bulk_data)

class Command(BaseCommand):
    help = "Process Apache logs and store in database"
    print(LOG_FILE)
    # with open("/var/log/apache2/access.log", "r") as file:
    #     for line in file:
    #         print(line)

    def handle(self, *args, **kwargs):
        logs = process_log_file(LOG_FILE)
        print(f"Logs lidos: {len(logs)}")
        for log in logs:
            print(f"Inserindo log de acesso: {log}")
            ApacheAccessLog.objects.get_or_create(
                ip=log["ip"],
                timestamp=log["timestamp"],
                method=log["method"],
                url=log["url"],
                protocol=log["protocol"],
                status=log["status"],
                size=log["size"]
            )
        self.stdout.write(self.style.SUCCESS("Logs de acessos processados com sucesso!"))
        process_error_logs()
        self.stdout.write(self.style.SUCCESS("Logs de errors processados com sucesso!"))

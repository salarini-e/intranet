#!/bin/bash

# Configurações do MySQL
MYSQL_USER="backup"
MYSQL_PASS='1Py%$chvA2QT5n0%z0'
MYSQL_HOST="192.168.1.220"

# Lista dos bancos a serem backupados
DATABASES=(
    "arqdeop"
    "arquivo_dps"
    "casa_do_trabalhador"
    "cevest"
    "cevest_novo"
    "cevest_temporario"    
    "cultura"
    "desenvolve_nf_atual"
    "enfermagem"
    "intranet"
    "mapoteca"
    "obras"
    "oficina_escola"
    "protocolo_informacao"
    "scvp"
    "senhas_facil"
    "senhas_facil_b"    
    "tributos"
    "turismo"    
)

# Diretório base para salvar os backups
BACKUP_DIR="/home/sistemas/db_backup"
LOG_FILE="$BACKUP_DIR/backup_log.txt"

# Criar o diretório base, se não existir
mkdir -p "$BACKUP_DIR"

# Iniciar o log
initial_time="Iniciado em: $(date +'%H:%M:%S')"

# Variáveis para controle de falhas
FAILED_BACKUPS=""

# Loop pelos bancos da lista
for DB in "${DATABASES[@]}"; do
    # Criar um diretório para o banco de dados, se ainda não existir
    DB_DIR="$BACKUP_DIR/$DB"
    mkdir -p "$DB_DIR"

    # Adicionar data ao nome do arquivo de backup
    DATE=$(date +'%Y-%m-%d_%H-%M-%S')
    BACKUP_FILE="$DB_DIR/${DB}_$DATE.sql"

    # Executar o mysqldump e salvar o backup
    echo "Fazendo backup do banco de dados: $DB..."
    mysqldump -u "$MYSQL_USER" -p"$MYSQL_PASS" -h "$MYSQL_HOST" "$DB" > "$BACKUP_FILE"

    # Verificar se o backup foi concluído com sucesso
    if [ $? -eq 0 ]; then
        echo "[$(date +'%H:%M:%S')] SUCESSO"
    else
        echo "[$(date +'%H:%M:%S')] ERRO"
        FAILED_BACKUPS="$FAILED_BACKUPS $DB"
    fi
done

# Resumo do backup
if [ -z "$FAILED_BACKUPS" ]; then
    echo "[$(date +'%d/%m/%Y')] SUCESSO" >> "$LOG_FILE"
    echo "--------------------------------------------------------" >> "$LOG_FILE"
    echo "$initial_time" >> "$LOG_FILE"
    echo "Finalizado em: $(date +'%H:%M:%S')" >> "$LOG_FILE"
    echo "--------------------------------------------------------" >> "$LOG_FILE"
else    
    echo "[$(date +'%d/%m/%Y')] ERROR" >> "$LOG_FILE"
    echo "--------------------------------------------------------" >> "$LOG_FILE"
    echo "$initial_time" >> "$LOG_FILE"
    echo "Backup finalizado em: $(date +'%H:%M:%S')" >> "$LOG_FILE"
    echo "-" >> "$LOG_FILE"
    echo "Falhas: $FAILED_BACKUPS" >> "$LOG_FILE"
    echo "--------------------------------------------------------" >> "$LOG_FILE"
fi

echo "Backup completo! Consulte o log em: $LOG_FILE"
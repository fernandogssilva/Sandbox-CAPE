
# Vou criar um script bash completo para instalação do CAPE Sandbox
# Este script será salvo como um arquivo que o usuário poderá executar

cape_install_script = """#!/bin/bash

#############################################################################
# Script de Instalação Completa do CAPE Sandbox v2
# Desenvolvido para Ubuntu 22.04 LTS
# Autor: Especialista em Sandbox CAPE
# Data: $(date +%Y-%m-%d)
#############################################################################

# Cores para output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Função para log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then 
    log_error "Este script precisa ser executado como root (sudo)"
    exit 1
fi

# Obter o username real (não root)
if [ -n "$SUDO_USER" ]; then
    REAL_USER=$SUDO_USER
else
    log_error "Execute com sudo, não como root direto"
    exit 1
fi

log_info "Script iniciado em $(date)"
log_info "Usuário detectado: $REAL_USER"

#############################################################################
# ETAPA 1: Atualização do Sistema
#############################################################################
log_step "ETAPA 1: Atualizando sistema base..."

apt update -y
apt upgrade -y
apt install -y wget curl git vim nano software-properties-common

log_info "Sistema atualizado com sucesso"

#############################################################################
# ETAPA 2: Download dos Scripts de Instalação
#############################################################################
log_step "ETAPA 2: Baixando scripts de instalação..."

cd /tmp

# Download do script CAPE
if [ ! -f cape2.sh ]; then
    wget https://raw.githubusercontent.com/kevoreilly/CAPEv2/master/installer/cape2.sh
    chmod +x cape2.sh
    log_info "Script cape2.sh baixado"
else
    log_warn "cape2.sh já existe, pulando download"
fi

# Download do script KVM
if [ ! -f kvm-qemu.sh ]; then
    wget https://raw.githubusercontent.com/doomedraven/Tools/master/Virtualization/kvm-qemu.sh
    chmod +x kvm-qemu.sh
    log_info "Script kvm-qemu.sh baixado"
else
    log_warn "kvm-qemu.sh já existe, pulando download"
fi

#############################################################################
# ETAPA 3: Instalação do CAPE
#############################################################################
log_step "ETAPA 3: Instalando CAPE Sandbox..."

log_info "Configurando senha do PostgreSQL..."
# Você pode alterar esta senha
export PASSWD="CAPESecurePass2025"

log_info "Iniciando instalação do CAPE (isso pode levar 10-15 minutos)..."
./cape2.sh all cape | tee /var/log/cape-install.log

if [ $? -eq 0 ]; then
    log_info "CAPE instalado com sucesso"
else
    log_error "Erro na instalação do CAPE. Verifique /var/log/cape-install.log"
    exit 1
fi

#############################################################################
# ETAPA 4: Configuração do KVM
#############################################################################
log_step "ETAPA 4: Configurando ambiente de virtualização KVM..."

log_info "Substituindo placeholders <WOOT> no script KVM..."
# Para ambiente de laboratório, usando valor genérico
# Em produção, use valores reais de hardware (acpidump/acpiextract)
sed -i 's/<WOOT>/b33f/g' kvm-qemu.sh

log_info "Instalando KVM (isso pode levar 10-15 minutos)..."
./kvm-qemu.sh all $REAL_USER | tee /var/log/kvm-install.log

if [ $? -eq 0 ]; then
    log_info "KVM instalado com sucesso"
else
    log_error "Erro na instalação do KVM. Verifique /var/log/kvm-install.log"
    exit 1
fi

log_info "Primeiro reboot necessário. Reiniciando em 5 segundos..."
sleep 5
reboot

"""

# Salvar o script
with open('cape_install_part1.sh', 'w') as f:
    f.write(cape_install_script)

print("Script parte 1 criado: cape_install_part1.sh")
print("="*70)

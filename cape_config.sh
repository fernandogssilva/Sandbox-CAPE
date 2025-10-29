#!/bin/bash

#############################################################################
# Script de Configuração do CAPE Sandbox
# Configure os arquivos principais do CAPE após instalação
#############################################################################

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[ERROR]${NC} Execute com sudo"
    exit 1
fi

#############################################################################
# Configuração Interativa
#############################################################################

echo "=========================================================================="
log_step "CAPE Sandbox - Configuração Interativa"
echo "=========================================================================="
echo ""

# Obter IP do host
HOST_IP=$(ip route get 1.1.1.1 | grep -oP 'src \K\S+')
log_info "IP do host detectado: $HOST_IP"
echo ""

# Obter informações do guest
read -p "Nome da VM guest (ex: win10-malware): " VM_NAME
read -p "IP da VM guest (ex: 192.168.122.100): " VM_IP
read -p "Nome do snapshot (ex: snapshot1): " SNAPSHOT_NAME
read -p "Arquitetura do guest (win10x64/win10x86/win7x64): " VM_ARCH

echo ""
log_step "Configurando arquivos do CAPE..."

#############################################################################
# Configurar cuckoo.conf
#############################################################################
log_info "Configurando cuckoo.conf..."

cat > /tmp/cuckoo_patch.conf << EOF
[cuckoo]
machinery = kvm
memory_dump = yes
terminate_processes = yes
reschedule = yes

[resultserver]
ip = $HOST_IP
port = 2042

[processing]
analysis_size_limit = 134217728
resolve_dns = yes

[database]
connection = postgresql://cape:SENHA_AQUI@localhost:5432/cape
timeout = 60
EOF

# Backup do original
cp /opt/CAPEv2/conf/cuckoo.conf /opt/CAPEv2/conf/cuckoo.conf.bak

log_info "Edite manualmente: /opt/CAPEv2/conf/cuckoo.conf"
log_info "Use as configurações de /tmp/cuckoo_patch.conf como referência"

#############################################################################
# Configurar kvm.conf
#############################################################################
log_info "Configurando kvm.conf..."

cat > /tmp/kvm_patch.conf << EOF
[kvm]
machines = $VM_NAME

[$VM_NAME]
label = $VM_NAME
platform = windows
ip = $VM_IP
snapshot = $SNAPSHOT_NAME
interface = virbr0
resultserver_ip = $HOST_IP
resultserver_port = 2042
arch = $VM_ARCH
tags = 
EOF

cp /opt/CAPEv2/conf/kvm.conf /opt/CAPEv2/conf/kvm.conf.bak

cat /tmp/kvm_patch.conf > /opt/CAPEv2/conf/kvm.conf
chown cape:cape /opt/CAPEv2/conf/kvm.conf

log_info "kvm.conf configurado com sucesso"

#############################################################################
# Configurar routing.conf
#############################################################################
log_info "Configurando routing.conf..."

cat > /tmp/routing_patch.conf << EOF
[routing]
route = internet
internet = eth0
rt_table = 

[vpn]
enabled = no

[tor]
enabled = no

[inetsim]
enabled = no
EOF

cp /opt/CAPEv2/conf/routing.conf /opt/CAPEv2/conf/routing.conf.bak

log_info "Edite manualmente: /opt/CAPEv2/conf/routing.conf"
log_info "Use as configurações de /tmp/routing_patch.conf como referência"

#############################################################################
# Configurar auxiliary.conf
#############################################################################
log_info "Configurando auxiliary.conf..."

cat > /tmp/auxiliary_patch.conf << EOF
[sniffer]
enabled = yes
tcpdump = /usr/bin/tcpdump
interface = virbr0

[mitm]
enabled = no

[services]
enabled = no
EOF

log_info "Edite manualmente: /opt/CAPEv2/conf/auxiliary.conf conforme necessidade"

#############################################################################
# Configurar processing.conf
#############################################################################
log_info "Configurando processing.conf..."

log_info "Habilite os módulos de processamento desejados em:"
log_info "/opt/CAPEv2/conf/processing.conf"

#############################################################################
# Configurar reporting.conf
#############################################################################
log_info "Configurando reporting.conf..."

log_info "Habilite os módulos de relatório desejados em:"
log_info "/opt/CAPEv2/conf/reporting.conf"

#############################################################################
# Ajustar permissões
#############################################################################
log_step "Ajustando permissões..."

chown -R cape:cape /opt/CAPEv2/
chmod -R 755 /opt/CAPEv2/

log_info "Permissões ajustadas"

#############################################################################
# Configurar rooter
#############################################################################
log_step "Configurando rooter para roteamento de rede..."

log_info "Iniciando serviço rooter..."
systemctl enable cape-rooter.service
systemctl start cape-rooter.service

#############################################################################
# Sumário
#############################################################################
echo ""
echo "=========================================================================="
log_step "CONFIGURAÇÃO CONCLUÍDA"
echo "=========================================================================="
echo ""
log_info "Arquivos de configuração:"
echo "  - /opt/CAPEv2/conf/cuckoo.conf (revise resultserver IP: $HOST_IP)"
echo "  - /opt/CAPEv2/conf/kvm.conf (configurado: $VM_NAME @ $VM_IP)"
echo "  - /opt/CAPEv2/conf/routing.conf (revise interface de internet)"
echo "  - /opt/CAPEv2/conf/auxiliary.conf (revise módulos auxiliares)"
echo ""
log_info "Backups criados com extensão .bak"
echo ""
log_info "Para iniciar CAPE:"
echo "  sudo -u cape poetry run python3 /opt/CAPEv2/cuckoo.py"
echo ""
log_info "Para iniciar interface web:"
echo "  cd /opt/CAPEv2/web"
echo "  sudo -u cape poetry run python3 manage.py migrate"
echo "  sudo -u cape poetry run python3 manage.py runserver 0.0.0.0:8000"
echo ""
log_info "Acesse: http://$HOST_IP:8000"
echo "=========================================================================="

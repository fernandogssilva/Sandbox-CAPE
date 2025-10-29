#!/bin/bash

#############################################################################
# Script de Instalação Completa do CAPE Sandbox v2 - PARTE 2
# Execute este script APÓS o primeiro reboot
# Desenvolvido para Ubuntu 22.04 LTS
#############################################################################

# Cores para output
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

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

if [ "$EUID" -ne 0 ]; then 
    log_error "Este script precisa ser executado como root (sudo)"
    exit 1
fi

if [ -n "$SUDO_USER" ]; then
    REAL_USER=$SUDO_USER
else
    log_error "Execute com sudo, não como root direto"
    exit 1
fi

#############################################################################
# ETAPA 5: Instalação do Virtual Machine Manager
#############################################################################
log_step "ETAPA 5: Instalando Virtual Machine Manager..."

cd /tmp

if [ ! -f kvm-qemu.sh ]; then
    wget https://raw.githubusercontent.com/doomedraven/Tools/master/Virtualization/kvm-qemu.sh
    chmod +x kvm-qemu.sh
fi

./kvm-qemu.sh virtmanager $REAL_USER | tee /var/log/virt-manager-install.log

if [ $? -eq 0 ]; then
    log_info "Virtual Machine Manager instalado com sucesso"
else
    log_error "Erro na instalação do Virt-Manager"
    exit 1
fi

#############################################################################
# ETAPA 6: Instalação de Dependências Python com Poetry
#############################################################################
log_step "ETAPA 6: Instalando dependências Python com Poetry..."

# Instalar dbus-x11 para evitar erros
apt install -y dbus-x11

cd /opt/CAPEv2

log_info "Instalando dependências via Poetry (pode levar alguns minutos)..."
sudo -u cape poetry install

if [ $? -ne 0 ]; then
    log_error "Erro na instalação de dependências via Poetry"
    exit 1
fi

log_info "Verificando ambiente virtual Poetry..."
sudo -u cape poetry env list

#############################################################################
# ETAPA 7: Instalação de Dependências Adicionais
#############################################################################
log_step "ETAPA 7: Instalando dependências Python adicionais..."

# Instalar peepdf
log_info "Instalando peepdf..."
sudo -u cape poetry run pip3 install https://github.com/CAPESandbox/peepdf/archive/20eda78d7d77fc5b3b652ffc2d8a5b0af796e3dd.zip#egg=peepdf==0.4.2

# Instalar batch_deobfuscator
log_info "Instalando batch_deobfuscator..."
sudo -u cape poetry run pip3 install -U git+https://github.com/DissectMalware/batch_deobfuscator

# Instalar httpreplay
log_info "Instalando httpreplay..."
sudo -u cape poetry run pip3 install -U git+https://github.com/CAPESandbox/httpreplay

# Instalar dependências opcionais
log_info "Instalando dependências opcionais..."
sudo -u cape poetry run pip install -r extra/optional_dependencies.txt 2>/dev/null || log_warn "Algumas dependências opcionais falharam (normal)"

#############################################################################
# ETAPA 8: Baixar Assinaturas da Comunidade
#############################################################################
log_step "ETAPA 8: Baixando assinaturas e módulos da comunidade..."

cd /opt/CAPEv2/utils
sudo -u cape poetry run python3 community.py -cr

log_info "Assinaturas baixadas com sucesso"

#############################################################################
# ETAPA 9: Configuração Inicial
#############################################################################
log_step "ETAPA 9: Configurando CAPE..."

log_info "Criando backup dos arquivos de configuração..."
cp -r /opt/CAPEv2/conf /opt/CAPEv2/conf.backup.$(date +%Y%m%d_%H%M%S)

log_info "Configurações básicas aplicadas"
log_info "IMPORTANTE: Você precisará configurar manualmente:"
log_info "  - /opt/CAPEv2/conf/cuckoo.conf (machinery, resultserver)"
log_info "  - /opt/CAPEv2/conf/kvm.conf (máquinas virtuais)"
log_info "  - /opt/CAPEv2/conf/routing.conf (internet, vpn)"

#############################################################################
# ETAPA 10: Configuração dos Serviços
#############################################################################
log_step "ETAPA 10: Verificando serviços systemd..."

systemctl status cape.service --no-pager || log_warn "Serviço cape.service não está ativo"
systemctl status cape-processor.service --no-pager || log_warn "Serviço cape-processor.service não está ativo"
systemctl status cape-web.service --no-pager || log_warn "Serviço cape-web.service não está ativo"
systemctl status cape-rooter.service --no-pager || log_warn "Serviço cape-rooter.service não está ativo"

log_info "Para iniciar os serviços manualmente:"
log_info "  sudo systemctl start cape.service"
log_info "  sudo systemctl start cape-processor.service"
log_info "  sudo systemctl start cape-web.service"
log_info "  sudo systemctl start cape-rooter.service"

#############################################################################
# FINALIZAÇÃO
#############################################################################
log_step "INSTALAÇÃO CONCLUÍDA!"

echo ""
echo "=========================================================================="
log_info "CAPE Sandbox instalado com sucesso!"
echo "=========================================================================="
echo ""
log_info "PRÓXIMOS PASSOS:"
echo ""
echo "1. Configure uma máquina virtual Windows guest (Windows 10 21H2 recomendado)"
echo "2. Instale Python 3.x (32-bit) no guest"
echo "3. Instale o agente: /opt/CAPEv2/agent/agent.py no guest"
echo "4. Configure o guest para iniciar automaticamente (snapshot)"
echo "5. Configure /opt/CAPEv2/conf/kvm.conf com as informações do guest"
echo "6. Configure /opt/CAPEv2/conf/routing.conf para internet"
echo ""
log_info "COMANDOS ÚTEIS:"
echo ""
echo "Iniciar CAPE manualmente:"
echo "  cd /opt/CAPEv2"
echo "  sudo -u cape poetry run python3 cuckoo.py"
echo ""
echo "Iniciar interface web:"
echo "  cd /opt/CAPEv2/web"
echo "  sudo -u cape poetry run python3 manage.py runserver 0.0.0.0:8000"
echo ""
echo "Submeter amostra de malware:"
echo "  cd /opt/CAPEv2/utils"
echo "  sudo -u cape poetry run python3 submit.py /caminho/para/malware.exe"
echo ""
echo "Ver logs dos serviços:"
echo "  journalctl -u cape.service -f"
echo ""
log_info "Documentação completa: https://capev2.readthedocs.io"
echo "=========================================================================="
echo ""

log_info "Segundo reboot recomendado. Execute: sudo reboot"

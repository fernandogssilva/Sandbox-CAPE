
# Criar script final de teste e submissão de malware

cape_test_submit = """#!/bin/bash

#############################################################################
# Script de Teste e Submissão de Malware - CAPE Sandbox
# Teste a funcionalidade do CAPE e submeta amostras
#############################################################################

RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
CYAN='\\033[0;36m'
NC='\\033[0m'

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

log_cmd() {
    echo -e "${CYAN}[CMD]${NC} $1"
}

echo "=========================================================================="
echo "  CAPE Sandbox - Teste e Submissão de Malware"
echo "=========================================================================="
echo ""

#############################################################################
# Menu Principal
#############################################################################

show_menu() {
    echo ""
    echo "=========================================================================="
    echo "  MENU PRINCIPAL"
    echo "=========================================================================="
    echo ""
    echo "1. Verificar Status dos Serviços CAPE"
    echo "2. Iniciar CAPE manualmente"
    echo "3. Iniciar Interface Web"
    echo "4. Submeter Amostra de Malware (CLI)"
    echo "5. Verificar Análises em Andamento"
    echo "6. Ver Logs do CAPE"
    echo "7. Parar Serviços CAPE"
    echo "8. Reiniciar Serviços CAPE"
    echo "9. Comandos Úteis (Referência)"
    echo "0. Sair"
    echo ""
    echo "=========================================================================="
    read -p "Escolha uma opção: " choice
    echo ""
    
    case $choice in
        1) check_services ;;
        2) start_cape_manual ;;
        3) start_web_interface ;;
        4) submit_malware ;;
        5) check_running_analyses ;;
        6) view_logs ;;
        7) stop_services ;;
        8) restart_services ;;
        9) show_useful_commands ;;
        0) exit 0 ;;
        *) log_error "Opção inválida!"; show_menu ;;
    esac
}

#############################################################################
# Funções
#############################################################################

check_services() {
    log_step "Verificando status dos serviços CAPE..."
    echo ""
    
    systemctl status cape.service --no-pager | head -n 10
    echo ""
    systemctl status cape-processor.service --no-pager | head -n 10
    echo ""
    systemctl status cape-web.service --no-pager | head -n 10
    echo ""
    systemctl status cape-rooter.service --no-pager | head -n 10
    
    echo ""
    log_info "Verificação concluída"
    read -p "Pressione ENTER para continuar..."
    show_menu
}

start_cape_manual() {
    log_step "Iniciando CAPE manualmente..."
    log_warn "CAPE será iniciado em modo interativo. Use Ctrl+C para parar."
    echo ""
    log_cmd "sudo -u cape poetry run python3 /opt/CAPEv2/cuckoo.py"
    echo ""
    read -p "Deseja continuar? (s/n): " confirm
    
    if [ "$confirm" = "s" ]; then
        cd /opt/CAPEv2
        sudo -u cape poetry run python3 cuckoo.py
    fi
    
    show_menu
}

start_web_interface() {
    log_step "Iniciando Interface Web..."
    echo ""
    log_info "A interface web estará disponível em:"
    HOST_IP=$(ip route get 1.1.1.1 | grep -oP 'src \\K\\S+' 2>/dev/null || echo "SEU_IP")
    echo ""
    echo "  http://$HOST_IP:8000"
    echo "  http://localhost:8000"
    echo ""
    log_warn "Use Ctrl+C para parar o servidor web"
    echo ""
    log_cmd "cd /opt/CAPEv2/web && sudo -u cape poetry run python3 manage.py runserver 0.0.0.0:8000"
    echo ""
    read -p "Deseja continuar? (s/n): " confirm
    
    if [ "$confirm" = "s" ]; then
        cd /opt/CAPEv2/web
        sudo -u cape poetry run python3 manage.py migrate
        sudo -u cape poetry run python3 manage.py runserver 0.0.0.0:8000
    fi
    
    show_menu
}

submit_malware() {
    log_step "Submeter Amostra de Malware"
    echo ""
    read -p "Caminho completo da amostra: " malware_path
    
    if [ ! -f "$malware_path" ]; then
        log_error "Arquivo não encontrado: $malware_path"
        read -p "Pressione ENTER para continuar..."
        show_menu
        return
    fi
    
    echo ""
    log_info "Opções de submissão:"
    echo "1. Submissão básica"
    echo "2. Submissão com timeout customizado"
    echo "3. Submissão com pacote específico"
    echo "4. Submissão com opções avançadas"
    read -p "Escolha: " submit_choice
    echo ""
    
    case $submit_choice in
        1)
            log_cmd "sudo -u cape poetry run python3 /opt/CAPEv2/utils/submit.py $malware_path"
            cd /opt/CAPEv2/utils
            sudo -u cape poetry run python3 submit.py "$malware_path"
            ;;
        2)
            read -p "Timeout em segundos (padrão 120): " timeout
            log_cmd "sudo -u cape poetry run python3 /opt/CAPEv2/utils/submit.py --timeout $timeout $malware_path"
            cd /opt/CAPEv2/utils
            sudo -u cape poetry run python3 submit.py --timeout "$timeout" "$malware_path"
            ;;
        3)
            read -p "Nome do pacote (ex: exe, dll, pdf, doc): " package
            log_cmd "sudo -u cape poetry run python3 /opt/CAPEv2/utils/submit.py --package $package $malware_path"
            cd /opt/CAPEv2/utils
            sudo -u cape poetry run python3 submit.py --package "$package" "$malware_path"
            ;;
        4)
            read -p "Opções adicionais (ex: --memory --enforce-timeout): " options
            log_cmd "sudo -u cape poetry run python3 /opt/CAPEv2/utils/submit.py $options $malware_path"
            cd /opt/CAPEv2/utils
            sudo -u cape poetry run python3 submit.py $options "$malware_path"
            ;;
    esac
    
    echo ""
    log_info "Amostra submetida! Aguarde a análise ser processada."
    read -p "Pressione ENTER para continuar..."
    show_menu
}

check_running_analyses() {
    log_step "Verificando análises em andamento..."
    echo ""
    log_info "Consultando banco de dados PostgreSQL..."
    
    sudo -u postgres psql -d cape -c "SELECT id, target, status, added_on FROM tasks ORDER BY id DESC LIMIT 10;" 2>/dev/null || {
        log_warn "Não foi possível conectar ao banco de dados"
        log_info "Verifique os logs em /opt/CAPEv2/log/"
    }
    
    echo ""
    read -p "Pressione ENTER para continuar..."
    show_menu
}

view_logs() {
    log_step "Visualizar Logs do CAPE"
    echo ""
    echo "1. Log do CAPE principal"
    echo "2. Log do Processor"
    echo "3. Log do Web"
    echo "4. Log do Rooter"
    echo "5. Todos os logs (tail)"
    read -p "Escolha: " log_choice
    echo ""
    
    case $log_choice in
        1) journalctl -u cape.service -f ;;
        2) journalctl -u cape-processor.service -f ;;
        3) journalctl -u cape-web.service -f ;;
        4) journalctl -u cape-rooter.service -f ;;
        5) 
            tail -f /opt/CAPEv2/log/cuckoo.log &
            tail -f /opt/CAPEv2/log/process.log
            ;;
    esac
    
    show_menu
}

stop_services() {
    log_step "Parando serviços CAPE..."
    sudo systemctl stop cape.service
    sudo systemctl stop cape-processor.service
    sudo systemctl stop cape-web.service
    sudo systemctl stop cape-rooter.service
    log_info "Serviços parados"
    read -p "Pressione ENTER para continuar..."
    show_menu
}

restart_services() {
    log_step "Reiniciando serviços CAPE..."
    sudo systemctl restart cape.service
    sudo systemctl restart cape-processor.service
    sudo systemctl restart cape-web.service
    sudo systemctl restart cape-rooter.service
    log_info "Serviços reiniciados"
    read -p "Pressione ENTER para continuar..."
    show_menu
}

show_useful_commands() {
    echo ""
    echo "=========================================================================="
    log_step "COMANDOS ÚTEIS - REFERÊNCIA RÁPIDA"
    echo "=========================================================================="
    echo ""
    
    cat << 'EOF'
# INICIAR CAPE MANUALMENTE
cd /opt/CAPEv2
sudo -u cape poetry run python3 cuckoo.py

# INICIAR INTERFACE WEB
cd /opt/CAPEv2/web
sudo -u cape poetry run python3 manage.py runserver 0.0.0.0:8000

# SUBMETER MALWARE (BÁSICO)
cd /opt/CAPEv2/utils
sudo -u cape poetry run python3 submit.py /caminho/para/malware.exe

# SUBMETER MALWARE (COM OPÇÕES)
sudo -u cape poetry run python3 submit.py --timeout 300 --memory /caminho/para/malware.exe

# SUBMETER MALWARE (PRIORIDADE ALTA)
sudo -u cape poetry run python3 submit.py --priority 3 /caminho/para/malware.exe

# SUBMETER URL
sudo -u cape poetry run python3 submit.py --url http://site-malicioso.com

# SUBMETER COM PACOTE ESPECÍFICO
sudo -u cape poetry run python3 submit.py --package exe /caminho/para/malware.exe
sudo -u cape poetry run python3 submit.py --package dll /caminho/para/malware.dll
sudo -u cape poetry run python3 submit.py --package pdf /caminho/para/malware.pdf

# SUBMETER COM MÁQUINA ESPECÍFICA
sudo -u cape poetry run python3 submit.py --machine win10-malware /caminho/para/malware.exe

# VER STATUS DOS SERVIÇOS
systemctl status cape.service
systemctl status cape-processor.service
systemctl status cape-web.service
systemctl status cape-rooter.service

# VER LOGS EM TEMPO REAL
journalctl -u cape.service -f
tail -f /opt/CAPEv2/log/cuckoo.log

# REINICIAR SERVIÇOS
sudo systemctl restart cape.service
sudo systemctl restart cape-processor.service

# CONSULTAR BANCO DE DADOS
sudo -u postgres psql -d cape -c "SELECT * FROM tasks ORDER BY id DESC LIMIT 5;"

# LIMPAR ANÁLISES ANTIGAS
sudo -u cape poetry run python3 /opt/CAPEv2/utils/clean.py

# ATUALIZAR ASSINATURAS DA COMUNIDADE
cd /opt/CAPEv2/utils
sudo -u cape poetry run python3 community.py -cr

# ATUALIZAR CAPE (GIT PULL)
cd /opt/CAPEv2
sudo -u cape git pull origin master
sudo -u cape poetry install

# API REST (SUBMETER VIA CURL)
curl -F file=@/caminho/para/malware.exe http://localhost:8000/api/tasks/create/file/

# API REST (OBTER RELATÓRIO)
curl http://localhost:8000/api/tasks/report/1/json/

# VERIFICAR VMs DISPONÍVEIS
virsh list --all

# INICIAR VM MANUALMENTE
virsh start nome-da-vm

# RESTAURAR SNAPSHOT DA VM
virsh snapshot-revert nome-da-vm snapshot1

# VERIFICAR CONECTIVIDADE COM GUEST
ping IP_DO_GUEST
curl http://IP_DO_GUEST:8000
EOF
    
    echo ""
    echo "=========================================================================="
    log_info "Documentação completa: https://capev2.readthedocs.io"
    echo "=========================================================================="
    echo ""
    read -p "Pressione ENTER para voltar ao menu..."
    show_menu
}

#############################################################################
# Executar Menu Principal
#############################################################################

show_menu
"""

with open('cape_test_submit.sh', 'w') as f:
    f.write(cape_test_submit)

print("Script de teste e submissão criado: cape_test_submit.sh")
print("="*70)


# Criar arquivo README com instruções completas

readme_content = """# CAPE Sandbox - Instalação Completa e Funcional
## Scripts de Instalação Automatizada para Análise de Malware

---

## 📋 Sumário

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Arquivos Incluídos](#arquivos-incluídos)
3. [Passo a Passo de Instalação](#passo-a-passo-de-instalação)
4. [Configuração do Guest Windows](#configuração-do-guest-windows)
5. [Teste e Submissão de Malware](#teste-e-submissão-de-malware)
6. [Troubleshooting](#troubleshooting)
7. [Comandos Úteis](#comandos-úteis)

---

## 🖥️ Requisitos do Sistema

### Host (Servidor CAPE)
- **Sistema Operacional**: Ubuntu 22.04 LTS Desktop 64-bit (recomendado)
- **CPU**: 4+ cores (com suporte a virtualização VT-x/AMD-V)
- **RAM**: 8 GB mínimo (16 GB recomendado)
- **Armazenamento**: 100 GB+ de espaço livre
- **Rede**: Conexão com internet estável

### Guest (Máquina Virtual de Análise)
- **Sistema Operacional**: Windows 10 21H2 64-bit (recomendado) ou Windows 7
- **RAM**: 2-4 GB
- **Armazenamento**: 40-60 GB
- **Python**: Versão 3.x 32-bit (IMPORTANTE: 32-bit, não 64-bit!)

---

## 📦 Arquivos Incluídos

| Arquivo | Descrição |
|---------|-----------|
| `cape_install_part1.sh` | Instalação inicial do CAPE e KVM (Parte 1) |
| `cape_install_part2.sh` | Instalação de dependências e configuração (Parte 2) |
| `cape_config.sh` | Configuração interativa dos arquivos do CAPE |
| `windows_guest_setup.ps1` | Script PowerShell para configurar o guest Windows |
| `cape_test_submit.sh` | Interface interativa para teste e submissão de malware |
| `README.md` | Este arquivo de documentação |

---

## 🚀 Passo a Passo de Instalação

### Etapa 1: Preparação do Host

1. **Instale o Ubuntu 22.04 LTS Desktop**
   - Baixe a ISO oficial: https://ubuntu.com/download/desktop
   - Instale em hardware físico ou VM (com virtualização aninhada habilitada)

2. **Habilite virtualização na BIOS/UEFI**
   - Para Intel: Habilite VT-x
   - Para AMD: Habilite AMD-V

3. **Verifique suporte a virtualização:**
   ```bash
   egrep -c '(vmx|svm)' /proc/cpuinfo
   # Se retornar > 0, virtualização está habilitada
   ```

---

### Etapa 2: Instalação do CAPE (Parte 1)

1. **Baixe os scripts para /tmp:**
   ```bash
   cd /tmp
   # Cole aqui os scripts fornecidos
   ```

2. **Dê permissão de execução:**
   ```bash
   chmod +x cape_install_part1.sh
   chmod +x cape_install_part2.sh
   chmod +x cape_config.sh
   chmod +x cape_test_submit.sh
   ```

3. **Execute a Parte 1:**
   ```bash
   sudo ./cape_install_part1.sh
   ```

   Este script irá:
   - Atualizar o sistema
   - Baixar scripts oficiais do CAPE
   - Instalar CAPE e todas as dependências
   - Instalar KVM (hipervisor)
   - **Reiniciar automaticamente o sistema**

4. **Aguarde o reboot automático** (~10-15 minutos de instalação)

---

### Etapa 3: Instalação do CAPE (Parte 2)

1. **Após o reboot, execute a Parte 2:**
   ```bash
   cd /tmp
   sudo ./cape_install_part2.sh
   ```

   Este script irá:
   - Instalar Virtual Machine Manager (GUI para KVM)
   - Instalar dependências Python com Poetry
   - Instalar bibliotecas adicionais (peepdf, httpreplay, etc.)
   - Baixar assinaturas da comunidade
   - Configurar serviços systemd

2. **Aguarde a conclusão** (~15-20 minutos)

3. **Reboot recomendado:**
   ```bash
   sudo reboot
   ```

---

### Etapa 4: Criação da VM Guest Windows

1. **Abra o Virtual Machine Manager:**
   ```bash
   virt-manager
   ```

2. **Crie uma nova VM:**
   - Clique em "Create a new virtual machine"
   - Escolha ISO do Windows 10 21H2
   - Memória: 4096 MB (4 GB)
   - Disco: 60 GB
   - Nome: `win10-malware` (ou outro nome)
   - Rede: Default NAT (virbr0)

3. **Instale o Windows normalmente**

4. **Anote o IP da VM:**
   ```bash
   # No Windows, abra CMD e execute:
   ipconfig
   # Anote o IPv4 (ex: 192.168.122.100)
   ```

---

### Etapa 5: Configuração do Guest Windows

1. **Copie o script PowerShell para o Windows guest:**
   - Método 1: Pasta compartilhada
   - Método 2: Montar um CD virtual com o arquivo
   - Método 3: Servidor HTTP temporário no host

2. **No Windows guest, execute como Administrador:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File windows_guest_setup.ps1
   ```

   Este script irá:
   - Desabilitar UAC
   - Desabilitar Windows Firewall
   - Desabilitar Windows Update
   - Desabilitar Windows Defender
   - Desabilitar Teredo

3. **Instale Python 3.x 32-bit:**
   - Download: https://www.python.org/downloads/
   - **IMPORTANTE**: Baixe a versão 32-bit (x86)
   - Marque "Add Python to PATH" durante instalação

4. **Instale Pillow:**
   ```cmd
   python -m pip install --upgrade pip
   pip install Pillow==9.5.0
   ```

5. **Copie o agent.py do host:**
   ```bash
   # No host Ubuntu:
   cd /opt/CAPEv2/agent
   python3 -m http.server 8080
   ```

   ```powershell
   # No Windows guest:
   # Abra navegador e acesse: http://IP_DO_HOST:8080
   # Baixe agent.py e renomeie para agent.pyw
   # Salve em: C:\\Users\\Public\\Downloads\\agent.pyw
   ```

6. **Configure agent.pyw para iniciar automaticamente:**
   - Abra "Task Scheduler" (Agendador de Tarefas)
   - Create Basic Task → Nome: `agent` (ou qualquer nome discreto)
   - Trigger: "When I log on"
   - Action: "Start a program" → `C:\\Users\\Public\\Downloads\\agent.pyw`
   - Propriedades → Marque "Run with highest privileges"

7. **Teste o agent:**
   - Execute agent.pyw manualmente (minimize a janela)
   - No host, teste:
     ```bash
     curl http://IP_DO_GUEST:8000
     # Deve retornar algo como: "CAPE Agent running"
     ```

8. **Crie um snapshot:**
   - No virt-manager, com o agent rodando:
   - Clique na VM → Snapshots → Create new snapshot
   - Nome: `snapshot1`
   - Descrição: "Clean system with agent running"

---

### Etapa 6: Configuração do CAPE

1. **Execute o script de configuração:**
   ```bash
   sudo ./cape_config.sh
   ```

2. **Forneça as informações quando solicitado:**
   - Nome da VM: `win10-malware`
   - IP da VM: `192.168.122.100`
   - Nome do snapshot: `snapshot1`
   - Arquitetura: `win10x64`

3. **Revise os arquivos de configuração:**
   ```bash
   sudo nano /opt/CAPEv2/conf/cuckoo.conf
   sudo nano /opt/CAPEv2/conf/kvm.conf
   sudo nano /opt/CAPEv2/conf/routing.conf
   ```

---

## 🧪 Teste e Submissão de Malware

### Método 1: Interface Interativa (Recomendado)

```bash
sudo ./cape_test_submit.sh
```

Este script oferece um menu interativo com as seguintes opções:
- Verificar status dos serviços
- Iniciar CAPE manualmente
- Iniciar interface web
- Submeter amostra de malware
- Verificar análises em andamento
- Ver logs
- Parar/reiniciar serviços
- Comandos úteis

### Método 2: Interface Web

1. **Inicie os serviços:**
   ```bash
   sudo systemctl start cape.service
   sudo systemctl start cape-web.service
   ```

2. **Acesse no navegador:**
   ```
   http://IP_DO_HOST:8000
   ```

3. **Submeta uma amostra:**
   - Clique em "Submit"
   - Faça upload do arquivo malicioso
   - Configure opções (timeout, priority, etc.)
   - Clique em "Analyze"

### Método 3: Linha de Comando

```bash
cd /opt/CAPEv2/utils
sudo -u cape poetry run python3 submit.py /caminho/para/malware.exe
```

**Opções avançadas:**
```bash
# Com timeout customizado
sudo -u cape poetry run python3 submit.py --timeout 300 malware.exe

# Com dump de memória
sudo -u cape poetry run python3 submit.py --memory malware.exe

# Com prioridade alta
sudo -u cape poetry run python3 submit.py --priority 3 malware.exe

# Analisar URL
sudo -u cape poetry run python3 submit.py --url http://site-malicioso.com

# Pacote específico
sudo -u cape poetry run python3 submit.py --package pdf malware.pdf
```

### Método 4: API REST

```bash
# Submeter arquivo via API
curl -F file=@malware.exe http://localhost:8000/api/tasks/create/file/

# Obter relatório JSON
curl http://localhost:8000/api/tasks/report/1/json/

# Listar todas as tarefas
curl http://localhost:8000/api/tasks/list/
```

---

## 🔧 Troubleshooting

### Problema: ResultServer não consegue bind na porta 2042

**Solução:**
```bash
# CAPE já está rodando como serviço
sudo systemctl stop cape.service
# Agora tente iniciar manualmente
sudo -u cape poetry run python3 /opt/CAPEv2/cuckoo.py
```

### Problema: Guest não consegue se comunicar com o host

**Solução:**
```bash
# Verifique se a interface virbr0 está ativa
ip addr show virbr0

# Verifique firewall
sudo ufw status
sudo ufw allow 2042/tcp

# Teste ping do host para o guest
ping IP_DO_GUEST

# Teste conectividade com o agent
curl http://IP_DO_GUEST:8000
```

### Problema: Agent não inicia no guest

**Solução:**
1. Verifique se Python 32-bit está instalado (não 64-bit)
2. Execute agent.pyw manualmente para ver erros
3. Verifique Task Scheduler → propriedades da tarefa → "Run with highest privileges"
4. Verifique firewall do Windows (deve estar desabilitado)

### Problema: Análise fica "pending" indefinidamente

**Solução:**
```bash
# Verifique se a VM está rodando
virsh list --all

# Verifique snapshot
virsh snapshot-list nome-da-vm

# Restaure snapshot manualmente
virsh snapshot-revert nome-da-vm snapshot1

# Reinicie o serviço CAPE
sudo systemctl restart cape.service
```

### Problema: Erro de permissão ao executar cuckoo.py

**Solução:**
```bash
# Certifique-se de executar como usuário 'cape'
sudo -u cape poetry run python3 /opt/CAPEv2/cuckoo.py

# Ajuste permissões se necessário
sudo chown -R cape:cape /opt/CAPEv2/
```

---

## 📚 Comandos Úteis

### Gerenciamento de Serviços

```bash
# Status dos serviços
systemctl status cape.service
systemctl status cape-processor.service
systemctl status cape-web.service

# Iniciar serviços
sudo systemctl start cape.service
sudo systemctl start cape-web.service

# Parar serviços
sudo systemctl stop cape.service

# Reiniciar serviços
sudo systemctl restart cape.service

# Habilitar serviços no boot
sudo systemctl enable cape.service
```

### Logs

```bash
# Ver logs em tempo real
journalctl -u cape.service -f

# Ver logs do arquivo
tail -f /opt/CAPEv2/log/cuckoo.log

# Ver últimas 100 linhas
tail -n 100 /opt/CAPEv2/log/cuckoo.log
```

### Banco de Dados

```bash
# Conectar ao PostgreSQL
sudo -u postgres psql -d cape

# Ver últimas tarefas
sudo -u postgres psql -d cape -c "SELECT id, target, status FROM tasks ORDER BY id DESC LIMIT 10;"

# Contar tarefas por status
sudo -u postgres psql -d cape -c "SELECT status, COUNT(*) FROM tasks GROUP BY status;"
```

### Gerenciamento de VMs

```bash
# Listar VMs
virsh list --all

# Iniciar VM
virsh start nome-da-vm

# Parar VM
virsh shutdown nome-da-vm

# Forçar parada
virsh destroy nome-da-vm

# Listar snapshots
virsh snapshot-list nome-da-vm

# Restaurar snapshot
virsh snapshot-revert nome-da-vm snapshot1

# Ver configuração da VM
virsh dumpxml nome-da-vm
```

### Atualização

```bash
# Atualizar CAPE
cd /opt/CAPEv2
sudo -u cape git pull origin master
sudo -u cape poetry install

# Atualizar assinaturas
cd /opt/CAPEv2/utils
sudo -u cape poetry run python3 community.py -cr
```

### Limpeza

```bash
# Limpar análises antigas
sudo -u cape poetry run python3 /opt/CAPEv2/utils/clean.py

# Limpar logs antigos
sudo find /opt/CAPEv2/log -type f -mtime +30 -delete
```

---

## 📖 Recursos Adicionais

- **Documentação Oficial**: https://capev2.readthedocs.io
- **GitHub**: https://github.com/kevoreilly/CAPEv2
- **Instância Demo**: https://capesandbox.com
- **Comunidade**: https://github.com/kevoreilly/CAPEv2/discussions

---

## ⚠️ Avisos de Segurança

1. **NUNCA execute malware fora do ambiente sandbox**
2. **Isole a rede do CAPE** da sua rede de produção
3. **Use CAPE apenas em ambientes controlados** (laboratório, pesquisa)
4. **Mantenha backups** regulares das configurações
5. **Atualize regularmente** o CAPE e assinaturas
6. **Monitore o uso de recursos** (CPU, RAM, disco)
7. **Implemente controle de acesso** à interface web em produção

---

## 📝 Notas Finais

- Este conjunto de scripts automatiza a instalação completa do CAPE Sandbox
- Todos os scripts foram desenvolvidos com base na documentação oficial
- Para ambientes de produção, considere:
  - Usar valores reais de hardware (ACPIDUMP) no lugar de `<WOOT>`
  - Implementar autenticação na interface web
  - Configurar SSL/TLS
  - Usar firewall para restringir acesso
  - Implementar rotação de logs
  - Monitoramento com Prometheus/Grafana

---

**Desenvolvido por**: Especialista em Sandbox CAPE  
**Data**: Outubro 2025  
**Versão**: 1.0  
**Licença**: Open Source (MIT)
"""

with open('README.md', 'w') as f:
    f.write(readme_content)

print("README completo criado: README.md")
print("="*70)
print("\nTodos os scripts foram criados com sucesso!")
print("\nArquivos gerados:")
print("  1. cape_install_part1.sh - Instalação inicial")
print("  2. cape_install_part2.sh - Instalação de dependências")
print("  3. cape_config.sh - Configuração interativa")
print("  4. windows_guest_setup.ps1 - Setup do Windows guest")
print("  5. cape_test_submit.sh - Interface de teste e submissão")
print("  6. README.md - Documentação completa")

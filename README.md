# Sandbox-CAPE - Hyper-V
Por se tratar de um ambiente de execução de malware, é imprescindível isolar totalmente a máquina virtual guest para evitar qualquer tipo de movimentação lateral ou acesso à rede/produtos em produção. Para isso, siga as orientações:
Crie uma rede virtual dedicada exclusivamente às máquinas virtuais CAPE, utilizando NAT ou VLAN separada, sem filtros abertos que permitam contato com outras máquinas na rede.
Configure firewall avançado no host para bloquear todo tráfego da VM guest que não seja estritamente necessário, evitando conexões externas não autorizadas.
Desative compartilhamento de pastas, dispositivos, clipboard e redirecionamentos no software de virtualização.
Configure DNS e gateway internos ou internos restritos para evitar resolução/exposição externa.
Utilize snapshots para restaurar o estado limpo do guest e garantir análises isoladas e seguras.
Realize monitoramento ativo do tráfego, recursos e logs para identificar tentativas de movimentação lateral ou comportamento inesperado.
Essas configurações tornam seu ambiente seguro, mitigando riscos inerentes à análise de malware em sandbox.

## Para que Serve

- Analisar em segurança arquivos e códigos suspeitos de malware
- Automatizar processo de execução, monitoramento e coleta de dados do malware
- Fornecer ambiente isolado para evitar infectar sistemas produtivos
- Gerar relatórios detalhados para auxiliar equipes de segurança, forense e incident response
- Facilitar o gerenciamento e a análise colaborativa via interface web ou API REST

### 2. Criar e Configurar Máquina Virtual Guest no Hypervisor

- Crie VM Windows 10 21H2 (BIOS Legacy, desative Secure Boot)
- Configure memória (mín. 4GB), CPUs virtuais (mín. 4 cores)
- Configure rede NAT e IP estático compatível
- Execute em VM o script PowerShell para desabilitar funções que atrapalham análise

###Descrição	da Execução

cape_install_part1.sh	Bash Script	Instalação inicial do CAPE e KVM	sudo 
  ./cape_install_part1.sh	Primeira etapa

cape_install_part2.sh	Bash Script	Instalação de dependências e serviços	sudo 
  ./cape_install_part2.sh	Após reboot da Parte 1

cape_config.sh	Bash Script	Configuração interativa dos arquivos do CAPE	sudo 
  ./cape_config.sh	Após criar e configurar guest

windows_guest_setup.ps1	PowerShell	Script para configuração automática do guest Windows	
powershell -ExecutionPolicy Bypass -File windows_guest_setup.ps1	Dentro da VM Windows

cape_test_submit.sh	Bash Script	Interface interativa para testar serviços e enviar malware	
sudo ./cape_test_submit.sh	


### Configurar CAPE no Host

Execute o script de configuração interativa:
powershell -ExecutionPolicy Bypass -File windows_guest_setup.ps1

### Preparar Host e Instalar CAPE
Execute os scripts bash:
  chmod +x *.sh
  sudo ./cape_install_part1.sh

Aguarde reboot automático
  sudo ./cape_install_part2.sh

powershell -ExecutionPolicy Bypass -File windows_guest_setup.ps1

text

- Instale Python 32-bit, Pillow e configure agente CAPE para inicialização automática.

### Configurar CAPE no Host

Execute o script de configuração interativa:
  sudo ./cape_config.sh

Informe nome da VM, IP, snapshot etc.

### Submeter Amostras e Monitorar
Use o menu interativo para enviar amostras, iniciar/monitorar serviços, iniciar interface web etc.:
  sudo ./cape_test_submit.sh

Ou acesse interface web via navegador em `http://IP_DO_HOST:8000` para gerenciamento visual e submissão.
Também é possível submeter por linha de comando ou API REST.

---

## Avisos de Segurança

- Use sempre em ambiente controlado e isolado.
- Faça snapshots regulares antes da análise.
- Desative redes não essenciais no guest para evitar vazamento.
- Atualize periodicamente CAPE e assinaturas.

---

## Links úteis

- Documentação oficial: [https://capev2.readthedocs.io](https://capev2.readthedocs.io/)
- Repositório oficial: [https://github.com/kevoreilly/CAPEv2](https://github.com/kevoreilly/CAPEv2)

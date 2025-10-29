# Sandbox-CAPE
Por se tratar de um ambiente de execução de malware, é imprescindível isolar totalmente a máquina virtual guest para evitar qualquer tipo de movimentação lateral ou acesso à rede/produtos em produção. Para isso, siga as orientações:

Crie uma rede virtual dedicada exclusivamente às máquinas virtuais CAPE, utilizando NAT ou VLAN separada, sem filtros abertos que permitam contato com outras máquinas na rede.

Configure firewall avançado no host para bloquear todo tráfego da VM guest que não seja estritamente necessário, evitando conexões externas não autorizadas.

Desative compartilhamento de pastas, dispositivos, clipboard e redirecionamentos no software de virtualização.

Configure DNS e gateway internos ou internos restritos para evitar resolução/exposição externa.

Utilize snapshots para restaurar o estado limpo do guest e garantir análises isoladas e seguras.

Realize monitoramento ativo do tráfego, recursos e logs para identificar tentativas de movimentação lateral ou comportamento inesperado.

Essas configurações tornam seu ambiente seguro, mitigando riscos inerentes à análise de malware em sandbox.

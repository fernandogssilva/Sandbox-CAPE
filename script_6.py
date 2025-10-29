
# Criar um resumo dos arquivos em CSV para facilitar visualização

import csv

scripts_info = [
    {
        'Arquivo': 'cape_install_part1.sh',
        'Tipo': 'Bash Script',
        'Descrição': 'Instalação inicial do CAPE e KVM',
        'Execução': 'sudo ./cape_install_part1.sh',
        'Quando Usar': 'Primeira etapa - instala CAPE e hipervisor',
        'Duração': '~15 minutos + reboot'
    },
    {
        'Arquivo': 'cape_install_part2.sh',
        'Tipo': 'Bash Script',
        'Descrição': 'Instalação de dependências Python e configuração',
        'Execução': 'sudo ./cape_install_part2.sh',
        'Quando Usar': 'Após primeiro reboot da Parte 1',
        'Duração': '~20 minutos'
    },
    {
        'Arquivo': 'cape_config.sh',
        'Tipo': 'Bash Script',
        'Descrição': 'Configuração interativa dos arquivos do CAPE',
        'Execução': 'sudo ./cape_config.sh',
        'Quando Usar': 'Após criar e configurar o guest Windows',
        'Duração': '~5 minutos'
    },
    {
        'Arquivo': 'windows_guest_setup.ps1',
        'Tipo': 'PowerShell Script',
        'Descrição': 'Configuração automática do Windows guest',
        'Execução': 'powershell -ExecutionPolicy Bypass -File windows_guest_setup.ps1',
        'Quando Usar': 'Dentro da VM Windows após instalação',
        'Duração': '~2 minutos'
    },
    {
        'Arquivo': 'cape_test_submit.sh',
        'Tipo': 'Bash Script',
        'Descrição': 'Interface interativa para teste e submissão de malware',
        'Execução': 'sudo ./cape_test_submit.sh',
        'Quando Usar': 'Para gerenciar e submeter amostras de malware',
        'Duração': 'Interativo'
    },
    {
        'Arquivo': 'README.md',
        'Tipo': 'Documentação',
        'Descrição': 'Guia completo de instalação e uso',
        'Execução': 'Leitura',
        'Quando Usar': 'Referência durante toda instalação',
        'Duração': 'N/A'
    }
]

# Salvar em CSV
with open('scripts_resumo.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Arquivo', 'Tipo', 'Descrição', 'Execução', 'Quando Usar', 'Duração'])
    writer.writeheader()
    writer.writerows(scripts_info)

print("Resumo dos scripts criado: scripts_resumo.csv")
print("="*70)

# Exibir tabela
print("\nRESUMO DOS SCRIPTS GERADOS\n")
print(f"{'Arquivo':<30} {'Tipo':<20} {'Duração':<20}")
print("="*70)
for script in scripts_info:
    print(f"{script['Arquivo']:<30} {script['Tipo']:<20} {script['Duração']:<20}")

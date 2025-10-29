
# Criar script para configuração do guest Windows

windows_guest_setup = """# Script PowerShell para Configuração do Guest Windows
# Execute este script no Windows guest (VM de análise de malware)
# Autor: Especialista em Sandbox CAPE

Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "CAPE Sandbox - Configuração do Guest Windows" -ForegroundColor Cyan
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está rodando como Administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[ERRO] Este script precisa ser executado como Administrador!" -ForegroundColor Red
    exit 1
}

Write-Host "[STEP 1] Desabilitando UAC..." -ForegroundColor Yellow
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "EnableLUA" -Value 0
Write-Host "[OK] UAC desabilitado" -ForegroundColor Green

Write-Host "[STEP 2] Desabilitando Windows Firewall..." -ForegroundColor Yellow
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
Write-Host "[OK] Firewall desabilitado" -ForegroundColor Green

Write-Host "[STEP 3] Desabilitando Windows Update..." -ForegroundColor Yellow
Stop-Service -Name wuauserv -Force
Set-Service -Name wuauserv -StartupType Disabled
Write-Host "[OK] Windows Update desabilitado" -ForegroundColor Green

Write-Host "[STEP 4] Desabilitando Windows Defender..." -ForegroundColor Yellow
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableIOAVProtection $true
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -DisableBlockAtFirstSeen $true
Set-MpPreference -DisableScriptScanning $true
Write-Host "[OK] Windows Defender desabilitado" -ForegroundColor Green

Write-Host "[STEP 5] Desabilitando Teredo..." -ForegroundColor Yellow
netsh interface teredo set state disabled
Write-Host "[OK] Teredo desabilitado" -ForegroundColor Green

Write-Host "[STEP 6] Configurando Rede..." -ForegroundColor Yellow
Write-Host "[INFO] Configure manualmente:" -ForegroundColor Cyan
Write-Host "  IP: 192.168.122.X (conforme seu kvm.conf)" -ForegroundColor White
Write-Host "  Máscara: 255.255.255.0" -ForegroundColor White
Write-Host "  Gateway: 192.168.122.1" -ForegroundColor White
Write-Host "  DNS: 8.8.8.8 e 8.8.4.4" -ForegroundColor White

Write-Host ""
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "PRÓXIMOS PASSOS MANUAIS:" -ForegroundColor Cyan
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Instale Python 3.x (32-bit) - IMPORTANTE: Versão 32-bit!" -ForegroundColor Yellow
Write-Host "   Download: https://www.python.org/downloads/" -ForegroundColor White
Write-Host "   Marque a opção 'Add Python to PATH' durante instalação" -ForegroundColor White
Write-Host ""
Write-Host "2. Após instalar Python, execute no CMD (como Admin):" -ForegroundColor Yellow
Write-Host "   python -m pip install --upgrade pip" -ForegroundColor White
Write-Host "   pip install Pillow==9.5.0" -ForegroundColor White
Write-Host ""
Write-Host "3. Copie agent.py do host CAPE:" -ForegroundColor Yellow
Write-Host "   Localização no host: /opt/CAPEv2/agent/agent.py" -ForegroundColor White
Write-Host "   Copie para: C:\\Users\\Public\\Downloads\\agent.pyw" -ForegroundColor White
Write-Host ""
Write-Host "4. Configure agent.pyw para iniciar automaticamente:" -ForegroundColor Yellow
Write-Host "   - Abra Task Scheduler (Agendador de Tarefas)" -ForegroundColor White
Write-Host "   - Create Basic Task" -ForegroundColor White
Write-Host "   - Trigger: When I log on" -ForegroundColor White
Write-Host "   - Action: Start a program -> agent.pyw" -ForegroundColor White
Write-Host "   - Marque 'Run with highest privileges'" -ForegroundColor White
Write-Host ""
Write-Host "5. Instale softwares adicionais (OPCIONAL):" -ForegroundColor Yellow
Write-Host "   - Microsoft Office 2010/2016 (32-bit)" -ForegroundColor White
Write-Host "   - Adobe Reader" -ForegroundColor White
Write-Host "   - Navegadores (Firefox, Chrome)" -ForegroundColor White
Write-Host "   IMPORTANTE: Desabilite atualizações automáticas!" -ForegroundColor White
Write-Host ""
Write-Host "6. Teste o agent:" -ForegroundColor Yellow
Write-Host "   - Inicie agent.pyw" -ForegroundColor White
Write-Host "   - Do host, teste: curl http://IP_DO_GUEST:8000" -ForegroundColor White
Write-Host "   - Você deve ver: 'CAPE Agent running'" -ForegroundColor White
Write-Host ""
Write-Host "7. Crie snapshot no virt-manager:" -ForegroundColor Yellow
Write-Host "   - Nome: snapshot1" -ForegroundColor White
Write-Host "   - Com o agent rodando e minimizado!" -ForegroundColor White
Write-Host ""
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "[INFO] Reinicie o Windows após completar todos os passos!" -ForegroundColor Green
Write-Host "=========================================================================" -ForegroundColor Cyan
"""

with open('windows_guest_setup.ps1', 'w') as f:
    f.write(windows_guest_setup)

print("Script de configuração do Windows guest criado: windows_guest_setup.ps1")
print("="*70)

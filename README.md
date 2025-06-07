# 🎵 YouTube Downloader Termux

Um downloader avançado de YouTube com interface interativa em português, desenvolvido especialmente para Android/Termux e sistemas Linux.

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Linux-orange.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

</div>

## 📋 Índice

- [Características](#-características)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Configurações](#-configurações)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Dependências](#-dependências)
- [Troubleshooting](#-troubleshooting)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Autor](#-autor)
- [Changelog](#-changelog)

## ✨ Características

### 🎯 Funcionalidades Principais
- **Download de Áudio**: MP3, AAC, M4A, OPUS, VORBIS com qualidades configuráveis
- **Download de Vídeo**: MP4, MKV, WEBM em resoluções até 4K
- **Reprodutor Integrado**: Player MPV para música online e offline
- **Interface Interativa**: Menu colorido e intuitivo em português com Rich Console
- **Gerenciamento de Playlists**: Download seletivo de itens específicos
- **Sistema de Cookies**: Suporte completo para TikTok e X/Twitter

### 🔧 Recursos Avançados
- **Downloads Simultâneos**: Configurável de 1 a 8 downloads paralelos
- **Histórico Inteligente**: Rastreamento de downloads e reprodução online
- **Sistema de Notificações**: Sons personalizáveis após conclusão de downloads
- **Gerenciamento de Legendas**: Download automático em múltiplos idiomas
- **Organização Automática**: Criação de subpastas por canal/playlist
- **Proxy Support**: Configuração de proxy para contornar bloqueios regionais
- **Temas Personalizáveis**: 6 esquemas de cores (cyan, green, yellow, blue, magenta, red)
- **Auto-Update**: Atualização automática de dependências e script via GitHub
- **Validação de Arquivos**: Verificação de sobrescrita e integridade

### 🎨 Interface Visual
- **Rich Console**: Interface colorida e responsiva com painéis informativos
- **Progress Bars**: Barras de progresso em tempo real durante downloads
- **Questionary Menus**: Navegação intuitiva com seleção por checkbox e radio
- **Logging Avançado**: Sistema de logs com diferentes níveis (INFO, WARNING, ERROR)
- **Feedback Visual**: Mensagens contextuais e indicadores de status

## 🔧 Pré-requisitos

### Sistemas Suportados
- **Android (Termux)**: 7.0+ (API 24+)
- **Linux**: Debian, Ubuntu, Linux Mint, Arch Linux, Manjaro, Fedora, RHEL, CentOS
- **Python**: 3.7+
- **Armazenamento**: 500MB+ livres
- **Internet**: Conexão estável

### Gerenciadores de Pacotes
- **Termux**: pkg
- **Debian/Ubuntu**: apt
- **Arch Linux**: pacman + yay (para AUR)
- **Fedora/RHEL**: dnf/yum

## 📦 Instalação

### 1. Preparar Ambiente Termux/Linux
```bash
# Para Termux (Android)
pkg update && pkg upgrade -y
pkg install python git -y
termux-setup-storage  # Opcional para acesso ao armazenamento

# Para Debian/Ubuntu/Linux Mint
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y

# Para Arch Linux/Manjaro
sudo pacman -Syu
sudo pacman -S python python-pip git base-devel
# Instalar yay (AUR helper) se não tiver
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..

# Para Fedora/RHEL/CentOS
sudo dnf update -y
sudo dnf install python3 python3-pip git -y
```

### 2. Clonar Repositório
```bash
# Clonar projeto
git clone https://github.com/Reyzn24/youtube_downloader_linux_termux.git
cd youtube_downloader_linux_termux

# Tornar executável
chmod +x beta1.py
```

### 3. Executar Aplicação
```bash
# A aplicação instala automaticamente as dependências na primeira execução
python beta1.py

# Ou python3 no Linux
python3 beta1.py
```

### 4. Instalação Manual de Dependências (se necessário)
```bash
# Dependências do sistema (Termux)
pkg install ffmpeg mpv -y

# Dependências do sistema (Debian/Ubuntu/Linux Mint)
sudo apt install ffmpeg mpv -y

# Dependências do sistema (Arch Linux/Manjaro)
sudo pacman -S ffmpeg mpv

# Dependências do sistema (Fedora/RHEL/CentOS)
sudo dnf install ffmpeg mpv -y

# Dependências Python (Universal)
pip install yt-dlp rich yaspin mutagen requests

# Para questionary (recomendado AUR no Arch Linux)
# Debian/Ubuntu/Termux/Fedora
pip install questionary

# Arch Linux/Manjaro (RECOMENDADO via AUR)
yay -S python-questionary
# OU alternativa via pip (menos estável)
pip install questionary

# Verificar instalação do questionary
python -c "import questionary; print('Questionary instalado com sucesso!')"
```

## 🚀 Uso

### Execução Básica
```bash
python beta1.py
```

### Menu Principal
```
┌─────────────────────────────────────────┐
│          YouTube Downloader v1.0.0      │
│                                         │
│ Autor: Reyzn24                          │
│ Última Atualização: 2025-06-07 00:17    │
│                                         │
│ Áudio: mp3 | Vídeo: mp4 | Tema: cyan    │
└─────────────────────────────────────────┘

? Escolha uma opção:
❯ Download (música e vídeo)
  Download de Playlist (escolher itens)
  Reproduzir Música (online ou offline)
  Atualizar
  Configurações
  Sair
```

### 1. Download de Música
- Selecione "Download (música e vídeo)" → "Música"
- Insira URL do YouTube/plataforma suportada
- O sistema usa automaticamente as configurações padrão (MP3 320kbps)
- Verificação automática de arquivos existentes com opção de sobrescrita

### 2. Download de Vídeo
- Selecione "Download (música e vídeo)" → "Vídeo"  
- Insira URL do YouTube/plataforma suportada
- Utiliza configurações padrão (MP4 com qualidade configurada)
- Suporte a legendas automáticas em múltiplos idiomas

### 3. Download de Playlist Seletivo
- Selecione "Download de Playlist (escolher itens)"
- Insira URL da playlist
- Use checkbox para selecionar itens específicos
- Escolha formato (áudio ou vídeo) para download em lote

### 4. Reprodutor de Música
#### Música Online
- Stream direto do YouTube sem download
- Histórico inteligente de reprodução
- Integração com player MPV

#### Música Offline
- Reprodução de arquivos baixados
- Navegação por pastas organizadas
- Suporte a múltiplos formatos de áudio

#### Reproduzir Todas
- Playlist automática de toda a biblioteca
- Reprodução sequencial com MPV

## ⚙️ Configurações

### Estrutura de Pastas
```
~/Yt-dlp/
├── config.json          # Configurações do usuário
├── cookies.txt           # Cookies para sites restritos
├── log.txt              # Logs de atividade
├── history_online.json  # Histórico de reprodução
└── .deps_installed      # Flag de dependências
```

### Configurações Disponíveis

#### 📁 **Pastas**
- **Pasta de Áudio**: `~/Music` (padrão)
- **Pasta de Vídeo**: `~/Movies` (padrão)

#### 🎵 **Áudio e Vídeo**
- **Formatos de Áudio**: MP3, AAC, M4A, OPUS, VORBIS
- **Formatos de Vídeo**: MP4, MKV, WEBM
- **Qualidades de Áudio**: 320kb, 192kb, 128kb, 96kb

#### 📥 **Download**
- **Legendas**: Ativar/Desativar download automático
- **Idiomas de Legendas**: pt, en, es (configurável)
- **Downloads Simultâneos**: 1-8 (padrão: 1)
- **Criar Subpastas**: Organização por canal/playlist
- **Exclusão Automática**: Remover arquivos temporários

#### 🍪 **Cookies**
- **TikTok**: Validação de cookies para vídeos privados
- **X/Twitter**: Suporte para conteúdo restrito
- **Gerenciamento**: Import/Export/Backup de cookies

#### 🎨 **Personalização**
- **Temas**: cyan, green, yellow, blue, magenta, red
- **Notificações**: Som personalizado após downloads
- **Proxy**: Configuração para contornar bloqueios

### Arquivo de Configuração (config.json)
```json
{
    "audio_path": "~/Music",
    "video_path": "~/Movies",
    "default_audio_format": "mp3",
    "default_video_format": "mp4",
    "default_audio_quality": "320kb",
    "auto_delete_temp": true,
    "download_subtitles": true,
    "subtitle_languages": ["pt", "en", "es"],
    "create_subfolders": true,
    "max_concurrent_downloads": 1,
    "proxy_url": "",
    "theme_color": "cyan",
    "notification_sound": true,
    "notification_sound_file": "/system/media/audio/ui/Effect_Tick.ogg"
}
```

## 🏗️ Estrutura do Projeto

### Arquitetura do Código
```
beta1.py
├── Classes Principais
│   ├── Logger              # Sistema de logging avançado
│   ├── DownloaderConfig    # Gerenciamento de configurações
│   ├── DependencyManager  # Gerenciamento de dependências
│   ├── Downloader         # Core de download e reprodução
│   └── Menu               # Interface do usuário
│
├── Funcionalidades
│   ├── Downloads           # Áudio/Vídeo/Playlist
│   ├── Reprodutor         # Online/Offline com MPV
│   ├── Configurações      # Sistema completo de customização
│   ├── Cookies            # Autenticação TikTok/X/Twitter
│   ├── Histórico          # Rastreamento inteligente
│   └── Atualizações       # Auto-update via GitHub
│
└── Utilitários
    ├── Validação de paths  # validate_path()
    ├── Limpeza automática  # cleanup_temp_files()
    ├── Notificações       # play_notification()
    └── Interface Rich     # Console styling
```

### Classes Detalhadas

#### 🗂️ **Logger**
```python
# Responsável por logging centralizado e contextual
- log(message, level, context, exc)
- Suporte a níveis: INFO, WARNING, ERROR
- Output simultâneo para arquivo (~/Yt-dlp/log.txt) e console
- Timestamp automático e formatação colorida
- Tratamento de exceções integrado
```

#### ⚙️ **DownloaderConfig**
```python
# Gerenciamento completo de configurações persistentes
- load_config() / save_config() - Carregamento e salvamento JSON
- configure_paths() - Interface interativa de configuração
- cookies_menu() - Gerenciamento completo de cookies
- history_menu() - Controle de histórico de reprodução
- _validate_tiktok_cookie() / _validate_x_cookie() - Validação em tempo real
- 18+ configurações personalizáveis com valores padrão
```

#### 📦 **DependencyManager**
```python
# Instalação e atualização automática multiplataforma
- check_dependencies() - Verificação inicial com flag de controle
- install_dependency() - Instalação individual com progress bar
- update_all_dependencies() - Atualização em massa
- Suporte automático: Termux, Debian, Arch, Fedora
- dependency_installed() - Verificação inteligente por módulo/comando
```

#### 🎵 **Downloader**  
```python
# Core de funcionalidades com recursos avançados
- download_audio() / download_video() - Downloads com validação
- play_music_menu() - Interface completa do reprodutor
- handle_playlist() - Processamento seletivo de playlists
- progress_hook() - Barras de progresso em tempo real
- _file_exists() - Verificação de duplicatas
- _interactive_overwrite() - Prompt de sobrescrita
- get_title_from_url() - Extração de metadados
- save_online_history() / get_online_history() - Histórico inteligente
```

#### 🖥️ **Menu**
```python
# Interface principal com navegação intuitiva
- main_menu() - Menu principal com painel informativo
- download_menu() - Interface de downloads simplificada
- update_menu() - Sistema de atualizações (deps + script)
- download_playlist_menu() - Seleção de itens por checkbox
- display_header() - Cabeçalho dinâmico com configurações
- update_script_from_github() - Auto-update com backup
```

## 📚 Dependências

### Dependências Python
| Pacote | Versão | Descrição |
|--------|--------|-----------|
| `yt-dlp` | Latest | Downloader principal |
| `rich` | Latest | Interface colorida |
| `questionary` | Latest | Menus interativos |
| `yaspin` | Latest | Spinners de loading |
| `mutagen` | Latest | Manipulação de metadados |
| `requests` | Latest | Requisições HTTP |

### Dependências do Sistema
| Pacote | Descrição |
|--------|-----------|
| `ffmpeg` | Processamento de áudio/vídeo |
| `mpv` | Reprodutor de mídia |
| `python` | Interpretador Python 3.7+ |

### Instalação Automática
```python
# O script verifica e instala automaticamente:
dependencies = {
    'yt-dlp': 'pip install --upgrade yt-dlp',
    'ffmpeg': {
        'termux': 'pkg install -y ffmpeg',
        'debian': 'sudo apt install -y ffmpeg', 
        'arch': 'sudo pacman -S ffmpeg',
        'fedora': 'sudo dnf install -y ffmpeg'
    },
    'mutagen': 'pip install --upgrade mutagen',
    'yaspin': 'pip install --upgrade yaspin',
    'rich': 'pip install --upgrade rich',
    'questionary': {
        'default': 'pip install --upgrade questionary',
        'arch_aur': 'yay -S python-questionary',  # RECOMENDADO
        'arch_pip': 'pip install --upgrade questionary'  # Alternativa
    },
    'mpv': {
        'termux': 'pkg install -y mpv',
        'debian': 'sudo apt install -y mpv',
        'arch': 'sudo pacman -S mpv', 
        'fedora': 'sudo dnf install -y mpv'
    },
    'requests': 'pip install --upgrade requests'
}

# Detecção automática de distro Linux
def detect_linux_distro():
    if os.path.exists('/data/data/com.termux'):
        return 'termux'
    elif os.path.exists('/etc/arch-release'):
        return 'arch'
    elif os.path.exists('/etc/debian_version'):
        return 'debian'
    elif os.path.exists('/etc/fedora-release'):
        return 'fedora'
    else:
        return 'unknown'
```

## 🐛 Troubleshooting

### ⚠️ Problemas Específicos do Arch Linux

#### **Questionary no Arch Linux**
```bash
# MÉTODO RECOMENDADO: AUR (mais estável)
yay -S python-questionary

# Verificar se funcionou
python -c "import questionary; print('✅ Questionary AUR OK!')"

# Se yay não estiver instalado
sudo pacman -S base-devel git
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si && cd ..

# ALTERNATIVA: pip (pode ter conflitos)
pip install questionary --user
# OU globalmente
sudo pip install questionary

# Se ainda houver problemas
pip uninstall questionary
yay -R python-questionary
yay -S python-questionary
```

#### **Conflitos de Pacotes Python**
```bash
# Limpar cache do pip
pip cache purge

# Reinstalar dependências problemáticas
pip uninstall yt-dlp rich yaspin mutagen requests
pip install --upgrade --force-reinstall yt-dlp rich yaspin mutagen requests

# Usar ambiente virtual (recomendado)
python -m venv ~/youtube-downloader-env
source ~/youtube-downloader-env/bin/activate
pip install yt-dlp rich yaspin mutagen requests questionary
```

### Problemas Comuns

#### ❌ **Erro de Dependências**
```bash
# Termux
pkg install python ffmpeg mpv -y
pip install yt-dlp rich yaspin mutagen requests questionary

# Debian/Ubuntu/Linux Mint
sudo apt install python3 python3-pip ffmpeg mpv -y
pip install yt-dlp rich yaspin mutagen requests questionary

# Arch Linux/Manjaro
sudo pacman -S python python-pip ffmpeg mpv
pip install yt-dlp rich yaspin mutagen requests
# Para questionary (MÉTODO RECOMENDADO via AUR)
yay -S python-questionary
# Verificar instalação
python -c "import questionary; print('✅ Questionary (AUR) funcionando!')"
# OU via pip (alternativa menos estável)
pip install questionary

# Troubleshooting Arch específico
# Se yay não estiver instalado:
# git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si

# Fedora/RHEL/CentOS  
sudo dnf install python3 python3-pip ffmpeg mpv -y
pip install yt-dlp rich yaspin mutagen requests questionary
```

#### ❌ **Erro de Permissões**
```bash
# Configurar storage do Termux
termux-setup-storage

# Verificar permissões das pastas
ls -la ~/Music ~/Movies
```

#### ❌ **Erro de Network**
```bash
# Verificar conexão
ping google.com

# Configurar proxy se necessário
# Menu: Configurações > Proxy
```

#### ❌ **Erro do MPV**
```bash
# Termux
pkg uninstall mpv && pkg install mpv -y

# Debian/Ubuntu/Linux Mint
sudo apt remove mpv && sudo apt install mpv -y

# Arch Linux/Manjaro
sudo pacman -R mpv && sudo pacman -S mpv

# Fedora/RHEL/CentOS
sudo dnf remove mpv && sudo dnf install mpv -y

# Verificar instalação
mpv --version
```

#### ❌ **Cookies Inválidos**
```bash
# Menu: Configurações > Cookies > Validar Cookies
# Reimportar cookies se necessário
```

### Logs de Debug
```bash
# Verificar logs detalhados
cat ~/Yt-dlp/log.txt

# Limpar logs
echo "" > ~/Yt-dlp/log.txt
```

### Reset Completo
```bash
# Remover configurações
rm -rf ~/Yt-dlp/

# Limpar cache Python (todas as distros)
find ~/.cache -name "*python*" -type d -exec rm -rf {} + 2>/dev/null

# Arch Linux: Limpar cache do pacman
sudo pacman -Scc

# Debian/Ubuntu: Limpar cache apt
sudo apt clean && sudo apt autoremove

# Executar novamente o aplicativo
python beta1.py
```

## ⚡ Performance & Otimizações

### Configurações Recomendadas por Distro

#### **Termux (Android)**
```json
{
    "max_concurrent_downloads": 1,
    "auto_delete_temp": true,
    "default_audio_quality": "192kb",
    "create_subfolders": false
}
```

#### **Arch Linux (Desktop)**
```json
{
    "max_concurrent_downloads": 3,
    "auto_delete_temp": false,
    "default_audio_quality": "320kb",
    "create_subfolders": true,
    "notification_sound": true
}
```

#### **Debian/Ubuntu (Server/Desktop)**
```json
{
    "max_concurrent_downloads": 2,
    "auto_delete_temp": true,
    "default_audio_quality": "256kb",
    "proxy_url": "",
    "download_subtitles": true
}
```

### Melhorias de Performance
```bash
# Arch Linux: Usar repositórios paralelos
sudo nano /etc/pacman.conf
# Descomentar: #ParallelDownloads = 5

# Todos os sistemas: Cache DNS
echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf

# FFmpeg com aceleração de hardware (se disponível)
ffmpeg -hwaccels  # Verificar acelerações disponíveis
```

## 🔧 Compatibilidade

### Sistemas Testados
| Sistema | Versão | Status | Observações |
|---------|--------|--------|-------------|
| **Termux** | Android 7+ | ✅ Completo | Funcionalidade completa |
| **Arch Linux** | Rolling | ✅ Completo | Requer yay para questionary |
| **Manjaro** | 21.3+ | ✅ Completo | Baseado em Arch |
| **Ubuntu** | 20.04+ | ✅ Completo | LTS recomendado |
| **Debian** | 11+ | ✅ Completo | Stable/Testing |
| **Linux Mint** | 20+ | ✅ Completo | Baseado em Ubuntu |
| **Fedora** | 35+ | ✅ Completo | Versões recentes |
| **CentOS** | 8+ | ⚠️ Parcial | Requer EPEL |
| **openSUSE** | 15.4+ | ⚠️ Não testado | Deve funcionar |

### Requisitos Mínimos
- **Python**: 3.7 ou superior
- **RAM**: 512MB livres
- **Armazenamento**: 100MB + espaço para downloads
- **Internet**: Conexão estável

### Versões Python Suportadas
```bash
# Verificar versão do Python
python --version  # ou python3 --version

# Versões testadas
✅ Python 3.7.x
✅ Python 3.8.x  
✅ Python 3.9.x
✅ Python 3.10.x
✅ Python 3.11.x
✅ Python 3.12.x
✅ Python 3.13.x
```

## ❓ FAQ (Perguntas Frequentes)

### **Q: Por que usar yay no Arch Linux para questionary?**
**A:** O pacote `python-questionary` do AUR é compilado específicamente para Arch Linux, evitando conflitos de dependências que podem ocorrer com a instalação via pip. É mais estável e integrado ao sistema de pacotes do Arch.

### **Q: Posso usar o script sem MPV?**
**A:** Não, o MPV é essencial para a funcionalidade de reprodução. O script pode funcionar parcialmente apenas para downloads, mas muitas funcionalidades ficarão indisponíveis.

### **Q: Como acelerar downloads?**
**A:** Configure `max_concurrent_downloads` no arquivo `config.json`. Valores recomendados: Termux (1), Desktop (2-3), Servidor (3-5).

### **Q: Cookies são obrigatórios?**
**A:** Não para YouTube, mas são necessários para TikTok e X/Twitter. Configure via menu "Configurações > Cookies".

### **Q: O script funciona com playlists longas?**
**A:** Sim, mas recomenda-se usar a seleção interativa para playlists com mais de 50 itens para evitar timeouts.

### **Q: Como resolver "ModuleNotFoundError"?**
**A:** Execute: `pip install --upgrade [nome_do_modulo]` ou use o menu "Atualizações > Dependências".

### **Q: Posso usar em servidor sem interface gráfica?**
**A:** Sim, o script funciona completamente via terminal/SSH. Apenas certifique-se de que MPV está configurado corretamente.

## 🤝 Contribuindo

### Como Contribuir
1. **Fork** o repositório
2. **Clone** sua fork
3. **Crie** uma branch para sua feature
4. **Commit** suas mudanças
5. **Push** para a branch
6. **Abra** um Pull Request

### Diretrizes de Desenvolvimento
- **Linguagem**: Use português para comentários e mensagens
- **Compatibilidade**: Mantenha suporte ao Python 3.7+
- **Testes**: Teste em pelo menos 2 distribuições (Termux + Desktop Linux)
- **Documentação**: Documente novas funcionalidades no README
- **Código**: Siga PEP 8 para formatação Python
- **Commits**: Use mensagens descritivas em português

### Ambiente de Desenvolvimento
```bash
# Clonar repositório
git clone https://github.com/Reyzn24/youtube_downloader_linux_termux.git
cd youtube_downloader_linux_termux

# Criar branch para feature
git checkout -b feature/nova-funcionalidade

# Ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt  # Se existir
pip install pylint black pytest

# Executar testes
python -m pytest tests/  # Se existir pasta tests/
python minimal_test.py   # Teste básico

# Verificar código
pylint beta1.py
black beta1.py --diff
```

### Reportar Bugs
- **Issues**: Use as [Issues do GitHub](https://github.com/Reyzn24/youtube_downloader_linux_termux/issues)
- **Logs**: Inclua conteúdo de `~/Yt-dlp/log.txt`
- **Sistema**: Mencione distribuição Linux e versão Python
- **Reprodução**: Descreva passos detalhados para reproduzir
- **Screenshots**: Inclua capturas de tela se relevante

### Sugestões de Melhorias
- **Interface**: Melhorias na UI/UX
- **Performance**: Otimizações de velocidade
- **Funcionalidades**: Novos recursos
- **Compatibilidade**: Suporte a novas distribuições
- **Localização**: Traduções para outros idiomas

## 🙏 Agradecimentos

### Projetos e Bibliotecas Utilizadas
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - O coração do downloader
- **[Rich](https://github.com/Textualize/rich)** - Interface console moderna
- **[Questionary](https://github.com/tmbo/questionary)** - Menus interativos elegantes
- **[MPV](https://mpv.io/)** - Reprodutor de mídia robusto
- **[FFmpeg](https://ffmpeg.org/)** - Processamento de áudio/vídeo
- **[Yaspin](https://github.com/pavdmyt/yaspin)** - Spinners de loading
- **[Mutagen](https://github.com/quodlibet/mutagen)** - Manipulação de metadados

### Comunidades
- **Termux Community** - Suporte e feedback
- **Arch Linux Community** - Testes e otimizações
- **Python Brasil** - Inspiração e boas práticas
- **AUR Maintainers** - Manutenção de pacotes

### Contribuidores
- **@Reyzn24** - Desenvolvimento principal
- **Comunidade GitHub** - Issues, PRs e feedback
- **Beta Testers** - Testes em diferentes distribuições

## 📚 Recursos Adicionais

### Documentação Técnica
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp#readme)
- [Rich Documentation](https://rich.readthedocs.io/)
- [MPV Manual](https://mpv.io/manual/stable/)
- [Python argparse](https://docs.python.org/3/library/argparse.html)

### Tutoriais Relacionados
- [Termux Setup Guide](https://termux.com/)
- [Arch Linux Installation](https://wiki.archlinux.org/title/Installation_guide)
- [AUR Helper Comparison](https://wiki.archlinux.org/title/AUR_helpers)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

### Ferramentas Complementares
```bash
# YouTube-DL GUI alternatives
youtube-dl-gui
tartube
youtube-dlg

# Audio converters
soundconverter
audacity
ffmpeg

# Video players
vlc
smplayer
kodi
```

## 📄 Licença

```
MIT License

Copyright (c) 2025 Reyzn24

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Autor

**Reyzn24**
- GitHub: [@Reyzn24](https://github.com/Reyzn24)
- Projeto: [youtube_downloader_linux_termux](https://github.com/Reyzn24/youtube_downloader_linux_termux)

## 📈 Changelog

### v1.0.0 (2025-06-07) - Versão Estável
#### ✨ Funcionalidades Principais
- **Sistema completo de download** - Áudio/Vídeo em múltiplos formatos
- **Reprodutor integrado** - MPV com controles personalizados
- **Interface multilíngue** - Português brasileiro completo
- **Gerenciamento de playlists** - Seleção interativa e batch downloads
- **Sistema de cookies** - Suporte TikTok/X/Twitter com validação
- **Downloads paralelos** - Configurável por distribuição (1-5 simultâneos)
- **Histórico inteligente** - Rastreamento automático de reproduções
- **Notificações personalizadas** - Sons configuráveis por tema
- **6 temas de cores** - cyan, green, yellow, blue, magenta, red
- **Auto-update system** - GitHub integration com backup automático

#### 🐛 Correções Críticas
- **Validação robusta de paths** - Prevenção de crashes por paths inválidos
- **Tratamento de erros avançado** - Recovery automático e logs detalhados
- **Limpeza automática** - Remoção de arquivos temporários órfãos
- **Compatibilidade universal** - Android/Termux + 6 distribuições Linux
- **Memory leak fixes** - Otimização de uso de memória
- **Encoding fixes** - Suporte completo a caracteres especiais

#### 🔧 Melhorias Técnicas
- **Rich Console Interface** - UI responsiva com progress bars
- **Questionary Menus** - Navegação intuitiva com autocomplete
- **Sistema de logging** - Logs estruturados com rotação automática
- **Configurações persistentes** - JSON schema com validação
- **Dependency manager** - Instalação automática multi-distro
- **Error recovery** - Sistema robusto de recuperação de falhas

#### 🛠️ DevOps & Manutenção
- **Multi-distro support** - Termux, Arch, Debian, Ubuntu, Fedora, CentOS
- **Package managers** - pkg, apt, pacman+yay, dnf/yum
- **Virtual environment** - Suporte completo a venv
- **Testing framework** - Scripts de teste automatizados
- **Documentation** - README completo com 500+ linhas
- **CI/CD ready** - Estrutura preparada para automação

#### 🎯 Estatísticas da Versão
- **Linhas de código**: 1,764 (beta1.py)
- **Classes implementadas**: 5 principais
- **Métodos únicos**: 50+
- **Dependências**: 7 Python + 3 sistema
- **Distribuições suportadas**: 7
- **Idiomas suportados**: Português (expandível)
- **Formatos de áudio**: MP3, AAC, FLAC, OGG
- **Formatos de vídeo**: MP4, WEBM, MKV
- **Qualidades suportadas**: 144p até 4K/8K

### Versões Anteriores
```
v0.9.x - Beta testing (internal)
v0.8.x - Alpha development (internal)  
v0.7.x - Proof of concept (internal)
```

### Roadmap Futuro
#### v1.1.0 (Planejado)
- [ ] Suporte a mais plataformas (Spotify, SoundCloud)
- [ ] Interface gráfica opcional (Tkinter/PyQt)
- [ ] Batch processing melhorado
- [ ] Plugin system
- [ ] Sync com cloud storage

#### v1.2.0 (Futuro)
- [ ] Web interface (Flask/FastAPI)
- [ ] Mobile app companion
- [ ] AI-powered recommendations
- [ ] Multi-language support
- [ ] Advanced scheduling

---

<div align="center">

**🎵 Desenvolvido com ❤️ para a comunidade Termux**

[⬆ Voltar ao topo](#-youtube-downloader-termux)

</div>


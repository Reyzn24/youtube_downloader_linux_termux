#!/usr/bin/env python3

"""
YouTube Downloader
Autor: Reyzn24
Versão: 1.0.0
Última Atualização: 2025-06-03 10:16:00
"""

import os
import sys
import json
import time
import threading
import subprocess
from datetime import datetime
from typing import Optional, Dict, List, Union
import yt_dlp
from yaspin import yaspin
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import requests
from concurrent.futures import ThreadPoolExecutor
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import glob
import questionary
from questionary import Style

# Limpa o arquivo de log na inicialização do programa
LOG_FILE_PATH = "/sdcard/Yt-dlp/log.txt"
try:
    os.makedirs("/sdcard/Yt-dlp", exist_ok=True)
    with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("")  # Limpa o conteúdo do arquivo
except Exception as e:
    # Se não for possível limpar o log, mostra aviso mas continua a execução
    print(f"Aviso: Não foi possível limpar o arquivo de log: {e}")

VERSION = "1.0.0"
AUTHOR = "Reyzn24"
LAST_UPDATED = "2025-06-07 00:17:00"

HISTORY_FILE_ONLINE = "/sdcard/Yt-dlp/history_online.json"

custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),     # Estilo para o símbolo de pergunta
    ('question', 'bold'),             # Estilo para o texto da pergunta
    ('answer', 'fg:#f44336 bold'),    # Estilo para a resposta
    ('pointer', 'fg:#673ab7 bold'),   # Estilo para o indicador de seleção
    ('highlighted', 'fg:#673ab7 bold'), # Estilo para itens destacados
    ('selected', 'fg:#cc5454'),       # Estilo para itens selecionados
    ('separator', 'fg:#673ab7'),      # Estilo para separadores
    ('instruction', 'fg:#535353'),    # Estilo para instruções
    ('text', ''),                     # Estilo para texto normal
    ('disabled', 'fg:#858585 italic') # Estilo para itens desabilitados
])

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cleanup_temp_files(directory, base_filename):
    patterns = [
        f"{base_filename}.*webm",
        f"{base_filename}.*mkv",
        f"{base_filename}.*temp",
        f"{base_filename}.*part",
        f"{base_filename}.f*",
    ]
    for pattern in patterns:
        for file in glob.glob(os.path.join(directory, pattern)):
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error removing temporary file {file}: {str(e)}")

class Logger:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.console = Console()
    def log(self, message: str, level: str = "INFO", context: str = None, exc: Exception = None):
        """
        Log a message with optional context and exception details.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ctx = f"[{context}]" if context else ""
        exc_msg = f" | Exception: {exc}" if exc else ""
        log_entry = f"[{timestamp}] [{level}]{ctx} {message}{exc_msg}\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as log_exc:
            # Exibe erro no console caso não consiga escrever no arquivo de log
            self.console.print(f"[bold red]ERRO DE LOG:[/] Não foi possível escrever no arquivo: {log_exc}")
            self.console.print(f"[bold red]ENTRADA PERDIDA:[/] {log_entry.strip()}")
        if level in ["ERROR", "WARNING"]:
            style = "bold red" if level == "ERROR" else "bold yellow"
            self.console.print(f"\n[{style}]{level}:[/] {ctx} {message}{exc_msg}")

class DownloaderConfig:
    def __init__(self):
        self.base_dir = "/sdcard/Yt-dlp"
        self.config_file = f"{self.base_dir}/config.json"
        self.cookie_file = f"{self.base_dir}/cookies.txt"
        self.log_file = f"{self.base_dir}/log.txt"
        self.audio_path = ""
        self.video_path = ""
        self.default_audio_format = "mp3"
        self.default_video_format = "mp4"
        self.default_audio_quality = "320kb"
        self.default_video_quality = "1080p"
        self.auto_delete_temp = True
        self.max_concurrent_downloads = 1
        self.set_max_concurrent_downloads(self.max_concurrent_downloads)
        self.download_subtitles = True
        self.subtitle_languages = ["en", "es"]
        self.create_subfolders = True
        self.max_concurrent_downloads = 1
        self.set_max_concurrent_downloads(self.max_concurrent_downloads)
        self.proxy_url = ""
        self.theme_color = "cyan"
        self.notification_sound = True
        self.notification_sound_file = "/system/media/audio/ui/Effect_Tick.ogg"  # Som de notificação padrão
        self.logger = Logger(self.log_file)
        self.create_base_dirs()
        self.load_config()
    def set_max_concurrent_downloads(self, value: int):
            """
            Define o número máximo de downloads simultâneos, garantindo que esteja dentro de um intervalo válido.
            """
            self.max_concurrent_downloads = max(1, min(8, value))  # Limita entre 1 e 8
    def create_base_dirs(self):
        os.makedirs(self.base_dir, exist_ok=True)
        self.logger.log("Diretório base criado/verificado")
    def load_config(self):
        default_config = {
            'audio_path': '/sdcard/Music',
            'video_path': '/sdcard/Movies',
            'default_audio_format': 'mp3',
            'default_video_format': 'mp4',
            'default_audio_quality': '320kb',
            'default_video_quality': '1080p',
            'auto_delete_temp': True,
            'download_subtitles': True,
            'subtitle_languages': ["en", "es"],
            'create_subfolders': True,
            'max_concurrent_downloads': 1,
            'proxy_url': '',
            'theme_color': 'cyan',
            'notification_sound': True,
            'notification_sound_file': "/system/media/audio/ui/Effect_Tick.ogg"
        }
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if config.get("default_audio_quality") == "320":
                        config["default_audio_quality"] = "320kb"
                    for key, value in default_config.items():
                        setattr(self, key, config.get(key, value))
                self.logger.log("Configuração carregada com sucesso", context="Config")
            else:
                for key, value in default_config.items():
                    setattr(self, key, value)
                self.save_config()
                self.logger.log("Novo arquivo de configuração criado com valores padrão", context="Config")
        except Exception as e:
            self.logger.log(f"Erro ao carregar configuração: {str(e)}", "ERROR", context="Config", exc=e)
    def save_config(self):
        config = {
            'audio_path': self.audio_path,
            'video_path': self.video_path,
            'default_audio_format': self.default_audio_format,
            'default_video_format': self.default_video_format,
            'default_audio_quality': self.default_audio_quality,
            'default_video_quality': self.default_video_quality,
            'auto_delete_temp': self.auto_delete_temp,
            'download_subtitles': self.download_subtitles,
            'subtitle_languages': self.subtitle_languages,
            'create_subfolders': self.create_subfolders,
            'max_concurrent_downloads': self.max_concurrent_downloads,
            'proxy_url': self.proxy_url,
            'theme_color': self.theme_color,
            'notification_sound': self.notification_sound,
            'notification_sound_file': self.notification_sound_file
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.logger.log("Configuração salva com sucesso", context="Config")
        except Exception as e:
            self.logger.log(f"Erro ao salvar configuração: {str(e)}", "ERROR", context="Config", exc=e)
    def configure_paths(self):
        while True:
            clear_screen()
            subtitle_status = "ON" if self.download_subtitles else "OFF"
            notification_status = "ON" if self.notification_sound else "OFF"
            audio_format = self.default_audio_format
            video_format = self.default_video_format
            
            console.print(Panel.fit(
                f"[bold {self.theme_color}]Configurações[/]\n" +
                f"[bold {self.theme_color}]Áudio: {audio_format} | Vídeo: {video_format} | Legendas: {subtitle_status} | Notificações: {notification_status}[/]",
                border_style=self.theme_color
            ))
            choice = questionary.select(
                "Escolha uma categoria de configuração:",
                choices=[
                    {"name": "Pastas", "value": "folders"},
                    {"name": "Áudio e Vídeo", "value": "audio_video"},
                    {"name": "Download", "value": "download"},
                    {"name": "Cookies", "value": "cookies"},
                    {"name": "Tema", "value": "theme"},
                    {"name": "Proxy", "value": "proxy"},
                    {"name": "Geral", "value": "general"},
                    {"name": "Histórico", "value": "history"},
                    {"name": "Salvar e Voltar", "value": "save"}
                ],
                style=custom_style
            ).ask()
            if choice == "save":
                self.save_config()
                break
            elif choice == "history":
                self.history_menu()
            elif choice == "cookies":
                self.cookies_menu()
            elif choice == "download":
                self._submenu_download()
            else:
                self._handle_config_category(choice)
    def _handle_config_category(self, category):
        if category == "folders":
            self._submenu_folders()
        elif category == "audio_video":
            self._submenu_audio_video()
        elif category == "theme":
            self._submenu_theme()
        elif category == "proxy":
            self._submenu_proxy()
        elif category == "general":
            self._submenu_general()
        else:
            # Usa o submenu geral como fallback para categorias desconhecidas
            self._submenu_general()
    def _submenu_folders(self):
        while True:
            clear_screen()
            console.print(Panel.fit(
                f"[bold {self.theme_color}]Configurações de Pastas[/]\n" +
                f"[bold {self.theme_color}]Pasta de Áudio: {self.audio_path} | " +
                f"Pasta de Vídeo: {self.video_path}[/]",
                border_style=self.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Pasta de Áudio", "value": "audio_path"},
                    {"name": "Pasta de Vídeo", "value": "video_path"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "back":
                break
            elif choice == "audio_path":
                path = questionary.text(
                    f"Digite o novo caminho para downloads de áudio (atualmente: {self.audio_path}):",
                    default=self.audio_path,
                    style=custom_style
                ).ask()
                if path:
                    self.audio_path = path
            elif choice == "video_path":
                path = questionary.text(
                    f"Digite o novo caminho para downloads de vídeo (atualmente: {self.video_path}):",
                    default=self.video_path,
                    style=custom_style
                ).ask()
                if path:
                    self.video_path = path
    def _submenu_audio_video(self):
        while True:
            clear_screen()
            console.print(Panel.fit(
                f"[bold {self.theme_color}]Configurações de Áudio e Vídeo[/]\n" +
                f"[bold {self.theme_color}]Formato de Áudio: {self.default_audio_format} | " +
                f"Formato de Vídeo: {self.default_video_format} | " +
                f"Qualidade de Áudio: {self.default_audio_quality} | " +
                f"Qualidade de Vídeo: {self.default_video_quality}[/]",
                border_style=self.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Formato de Áudio Padrão", "value": "audio_format"},
                    {"name": "Formato de Vídeo Padrão", "value": "video_format"},
                    {"name": "Qualidade de Áudio", "value": "audio_quality"},
                    {"name": "Qualidade de Vídeo", "value": "video_quality"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "back":
                break
            else:
                self._handle_config_choice(choice)
    def _submenu_download(self):
        while True:
            clear_screen()
            subtitle_status = "ON" if self.download_subtitles else "OFF"
            concurrent_status = f"{self.max_concurrent_downloads}"
            subfolder_status = "ON" if self.create_subfolders else "OFF"
            
            console.print(Panel.fit(
                f"[bold {self.theme_color}]Configurações de Download[/]\n" +
                f"[bold {self.theme_color}]Legendas: {subtitle_status} | " +
                f"Downloads Simultâneos: {concurrent_status} | " +
                f"Subpastas: {subfolder_status}[/]",
                border_style=self.theme_color
            ))
            
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Baixar Legendas", "value": "subtitles"},
                    {"name": f"Idiomas de Legendas ({', '.join(self.subtitle_languages)})", "value": "sub_languages"},
                    {"name": "Downloads Simultâneos", "value": "concurrent"},
                    {"name": "Criar Subpastas", "value": "subfolders"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "back":
                break
            else:
                self._handle_config_choice(choice)
    def _submenu_theme(self):
        clear_screen()
        console.print(Panel.fit(
            f"[bold {self.theme_color}]Configurações de Tema[/]\n" +
            f"[bold {self.theme_color}]Tema Atual: {self.theme_color}[/]",
            border_style=self.theme_color
        ))
        theme_choice = questionary.select(
            f"Escolha a cor do tema (atualmente: {self.theme_color}):",
            choices=["cyan", "green", "yellow", "blue", "magenta", "red"],
            default=self.theme_color,
            style=custom_style
        ).ask()
        if theme_choice:
            self.theme_color = theme_choice
    def _submenu_proxy(self):
        clear_screen()
        proxy_status = self.proxy_url or "desativado"
        console.print(Panel.fit(
            f"[bold {self.theme_color}]Configurações de Proxy[/]\n" +
            f"[bold {self.theme_color}]Proxy: {proxy_status}[/]",
            border_style=self.theme_color
        ))
        proxy = questionary.text(
            f"URL do Proxy (deixe em branco para desativar) (atualmente: {self.proxy_url or 'desativado'}):",
            default=self.proxy_url,
            style=custom_style
        ).ask()
        self.proxy_url = proxy
    def _submenu_general(self):
        while True:
            clear_screen()
            auto_delete_status = "ON" if self.auto_delete_temp else "OFF"
            notification_status = "ON" if self.notification_sound else "OFF"
            
            console.print(Panel.fit(
                f"[bold {self.theme_color}]Configurações Gerais[/]\n" +
                f"[bold {self.theme_color}]Excluir Arquivos Temporários: {auto_delete_status} | " +
                f"Som de Notificação: {notification_status}[/]",
                border_style=self.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Excluir Arquivos Temporários", "value": "auto_delete"},
                    {"name": "Som de Notificação", "value": "notification"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "back":
                break
            else:
                self._submenu_notification_sound() if choice == "notification" else self._handle_config_choice(choice)
    def _submenu_notification_sound(self):
        while True:
            clear_screen()
            status = "ON" if self.notification_sound else "OFF"
            console.print(Panel.fit(
                f"[bold {self.theme_color}]Configurações de Som de Notificação[/]\n[bold {self.theme_color}]Status atual: {status}[/]",
                border_style=self.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": f"Ativar/Desativar som de notificação (atualmente: {status})", "value": "toggle"},
                    {"name": "Escolher arquivo de som para notificação", "value": "choose"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "back":
                break
            elif choice == "toggle":
                self.notification_sound = questionary.select(
                    f"Ativar som de notificação? (atualmente: {status})",
                    choices=[
                        {"name": "Sim", "value": True},
                        {"name": "Não", "value": False}
                    ],
                    style=custom_style
                ).ask()
            elif choice == "choose":
                default_sounds = [
                    "/system/media/audio/ui/Effect_Tick.ogg",
                    "/system/media/audio/notifications/Argon.ogg",
                    "/system/media/audio/notifications/Carbon.ogg",
                    "/system/media/audio/notifications/Helium.ogg",
                    "/system/media/audio/notifications/Oxygen.ogg",
                    "/sdcard/Download/notify.ogg"
                ]
                sound_file = questionary.text(
                    "Digite o caminho para o arquivo de som de notificação:",
                    default=self.notification_sound_file,
                    style=custom_style,
                    qmark="🎵"
                ).ask()
                if sound_file and os.path.exists(sound_file):
                    self.notification_sound_file = sound_file
                    console.print(f"[green]Som de notificação definido para: {sound_file}[/]")
                    time.sleep(1)
                else:
                    console.print("[yellow]Arquivo não encontrado. Caminho não alterado.[/]")
                    time.sleep(1)
    def _handle_config_choice(self, choice):
        if choice == "audio_format":
            format_choice = questionary.select(
                f"Escolha o formato de áudio padrão (atualmente: {self.default_audio_format}):",
                choices=["mp3", "aac", "m4a", "opus", "vorbis"],
                default=self.default_audio_format,
                style=custom_style
            ).ask()
            if format_choice:
                self.default_audio_format = format_choice
        elif choice == "video_format":
            format_choice = questionary.select(
                f"Escolha o formato de vídeo padrão (atualmente: {self.default_video_format}):",
                choices=["mp4", "mkv", "webm"],
                default=self.default_video_format,
                style=custom_style
            ).ask()
            if format_choice:
                self.default_video_format = format_choice
        elif choice == "audio_quality":
            quality_choice = questionary.select(
                f"Escolha a qualidade de áudio padrão (atualmente: {self.default_audio_quality}):",
                choices=["320kb", "192kb", "128kb", "96kb"],
                default=self.default_audio_quality,
                style=custom_style
            ).ask()
            if quality_choice:
                self.default_audio_quality = quality_choice
        elif choice == "video_quality":
            quality_choice = questionary.select(
                f"Escolha a qualidade de vídeo padrão (atualmente: {self.default_video_quality}):",
                choices=["best", "1080p", "720p", "480p", "360p"],
                default=self.default_video_quality,
                style=custom_style
            ).ask()
            if quality_choice:
                self.default_video_quality = quality_choice
        elif choice == "auto_delete":
            status = "ON" if self.auto_delete_temp else "OFF"
            self.auto_delete_temp = questionary.select(
                f"Excluir arquivos temporários automaticamente? (atualmente: {status})",
                choices=[
                    {"name": "Sim", "value": True},
                    {"name": "Não", "value": False}
                ],
                style=custom_style
            ).ask()
        elif choice == "subtitles":
            status = "ON" if self.download_subtitles else "OFF"
            self.download_subtitles = questionary.select(
                f"Baixar legendas quando disponíveis? (atualmente: {status})",
                choices=[
                    {"name": "Sim", "value": True},
                    {"name": "Não", "value": False}
                ],
                style=custom_style
            ).ask()
        elif choice == "subfolders":
            status = "ON" if self.create_subfolders else "OFF"
            self.create_subfolders = questionary.select(
                f"Criar subpastas para organizar downloads? (atualmente: {status})",
                choices=[
                    {"name": "Sim", "value": True},
                    {"name": "Não", "value": False}
                ],
                style=custom_style
            ).ask()
        elif choice == "concurrent":
            # Configura o número de downloads simultâneos
            choices_list = [{"name": str(i), "value": i} for i in range(1, 9)]
            # Encontra a opção correspondente ao valor atual
            matching_choice = next((c for c in choices_list if c["value"] == self.max_concurrent_downloads), choices_list[0])
            max_downloads = questionary.select(
                f"Número máximo de downloads simultâneos (atualmente: {self.max_concurrent_downloads}):",
                choices=choices_list,
                default=matching_choice,
                style=custom_style
            ).ask()
            if max_downloads:
                self.set_max_concurrent_downloads(max_downloads)
        elif choice == "notification":
            status = "ON" if self.notification_sound else "OFF"
            self.notification_sound = questionary.select(
                f"Ativar som de notificação após downloads? (atualmente: {status})",
                choices=[
                    {"name": "Sim", "value": True},
                    {"name": "Não", "value": False}
                ],
                style=custom_style
            ).ask()
        elif choice == "sub_languages":
            current = ", ".join(self.subtitle_languages)
            new_langs = questionary.text(
                f"Digite os idiomas de legendas (separados por vírgula, ex: pt,en,es) (atualmente: {current}):",
                default=current,
                style=custom_style
            ).ask()
            if new_langs is not None:
                langs = [lang.strip() for lang in new_langs.split(",") if lang.strip()]
                if langs:
                    self.subtitle_languages = langs
    def history_menu(self):
        # Gerencia o histórico de downloads online
        clear_screen()
        history = []
        
        console.print(Panel.fit(
            f"[bold {self.theme_color}]Histórico de Downloads[/]\n" +
            f"[bold {self.theme_color}]Gerenciamento de Itens Baixados Anteriormente[/]",
            border_style=self.theme_color
        ))
        
        if os.path.exists(HISTORY_FILE_ONLINE):
            with open(HISTORY_FILE_ONLINE, "r", encoding="utf-8") as f:
                try:
                    entries = json.load(f)
                except Exception:
                    entries = []
                seen = set()
                for item in reversed(entries):
                    key = (item.get("title"), item.get("url"))
                    if key not in seen:
                        history.append(item)
                        seen.add(key)
                history = list(reversed(history))
        if not history:
            console.print("[yellow]Histórico vazio.[/]")
            time.sleep(2)
            return
        # Adiciona opção "Voltar" apenas para sair, não para exclusão
        choices = [{"name": f'{item.get("title")}', "value": (item.get("title"), item.get("url"))} for item in history]
        choices.append({"name": "Voltar", "value": "back"})
        to_delete = questionary.checkbox(
            "Selecione músicas do histórico para excluir (use espaço para selecionar, Enter para confirmar):",
            choices=choices,
            style=custom_style
        ).ask()
        # Remove a opção "back" do conjunto de exclusão, se selecionada
        if to_delete:
            to_delete_set = set([x for x in to_delete if x != "back"])
            if not to_delete_set:
                return
            new_lines = [item for item in history if (item.get("title"), item.get("url")) not in to_delete_set]
            with open(HISTORY_FILE_ONLINE, "w", encoding="utf-8") as f:
                json.dump(new_lines, f, ensure_ascii=False, indent=2)
            console.print("[green]Histórico atualizado![/]")
            time.sleep(2)

    # INÍCIO - GERENCIAMENTO DE COOKIES
    def cookies_menu(self):
        while True:
            clear_screen()
            # Verifica a validade dos cookies para exibição no painel
            tiktok_valid = self._validate_tiktok_cookie()
            x_valid = self._validate_x_cookie()
            tiktok_status = "[green]Válido[/]" if tiktok_valid else "[red]Inválido[/]"
            x_status = "[green]Válido[/]" if x_valid else "[red]Inválido[/]"
            
            console.print(Panel.fit(
                f"[bold {self.theme_color}]Configurações de Cookies[/]\n" +
                f"[bold {self.theme_color}]TikTok: {tiktok_status} | X/Twitter: {x_status}[/]",
                border_style=self.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Validar Cookies", "value": "validate"},
                    {"name": "Mostrar Expiração de Cookies", "value": "show_exp"},
                    {"name": "Substituir/Atualizar Cookies", "value": "replace"},
                    {"name": "Mostrar Caminho do Arquivo de Cookies", "value": "show_path"},
                    {"name": "Exportar/Fazer Backup de Cookies", "value": "export"},
                    {"name": "Importar Cookies de Arquivo", "value": "import"},
                    {"name": "Excluir Cookies", "value": "delete"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "validate":
                self.validate_cookies()
            elif choice == "show_exp":
                self.show_cookie_expiration()
            elif choice == "replace":
                self.replace_cookies()
            elif choice == "show_path":
                self.show_cookie_path()
            elif choice == "export":
                self.export_cookies()
            elif choice == "import":
                self.import_cookies()
            elif choice == "delete":
                self.delete_cookies()
            elif choice == "back":
                break
    def validate_cookies(self):
        tiktok_valid = self._validate_tiktok_cookie()
        x_valid = self._validate_x_cookie()
        status = []
        status.append(f"TikTok: [green]Válido[/]" if tiktok_valid else "TikTok: [red]Inválido ou expirado[/]")
        status.append(f"X/Twitter: [green]Válido[/]" if x_valid else "X/Twitter: [red]Inválido ou expirado[/]")
        console.print("\n".join([f" - {s}" for s in status]))
        input("Pressione Enter para continuar...")
    def _validate_tiktok_cookie(self):
        cookies = self._read_cookies_file()
        sessionid = None
        for c in cookies:
            if c.get("domain", "").endswith("tiktok.com") and c.get("name") == "sessionid":
                sessionid = c["value"]
                break
        if not sessionid:
            return False
        try:
            resp = requests.get(
                "https://www.tiktok.com/api/me/",
                cookies={"sessionid": sessionid},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            if resp.status_code == 200 and '"user"' in resp.text:
                return True
        except Exception:
            pass
        return False
    def _validate_x_cookie(self):
        cookies = self._read_cookies_file()
        auth_token = None
        for c in cookies:
            if c.get("domain", "").endswith("twitter.com") and c.get("name") == "auth_token":
                auth_token = c["value"]
                break
        if not auth_token:
            return False
        try:
            resp = requests.get(
                "https://twitter.com/home",
                cookies={"auth_token": auth_token},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            if resp.status_code == 200 and "twitter.com" in resp.url:
                return True
        except Exception:
            pass
        return False
    def show_cookie_expiration(self):
        cookies = self._read_cookies_file()
        found = False
        for c in cookies:
            if "expiry" in c:
                exp = datetime.utcfromtimestamp(int(c["expiry"])).strftime("%Y-%m-%d %H:%M:%S")
                console.print(f"{c.get('domain','?')}: [bold]{c.get('name','?')}[/] expires at [bold {self.theme_color}]{exp}[/]")
                found = True
        if not found:
            console.print("[yellow]Nenhuma informação de expiração encontrada no arquivo de cookies.[/]")
        input("Pressione Enter para continuar...")
    def replace_cookies(self):
        console.print(f"Cole seu array JSON de cookies (formato Netscape/Chrome/yt-dlp):")
        new_cookies = []
        try:
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            new_cookies = json.loads("\n".join(lines))
            with open(self.cookie_file, "w", encoding="utf-8") as f:
                json.dump(new_cookies, f, ensure_ascii=False, indent=2)
            console.print("[green]Cookies substituídos com sucesso.[/]")
        except Exception as e:
            console.print(f"[red]Erro ao substituir cookies:[/] {e}")
        input("Pressione Enter para continuar...")
    def show_cookie_path(self):
        console.print(f"Caminho do arquivo de cookies:\n[bold {self.theme_color}]{self.cookie_file}[/]")
        input("Pressione Enter para continuar...")
    def export_cookies(self):
        export_path = questionary.text(
            "Digite o caminho de exportação (ex: /sdcard/Yt-dlp/cookies_backup.json):",
            default="/sdcard/Yt-dlp/cookies_backup.json",
            style=custom_style).ask()
        ok, msg = validate_path(os.path.dirname(export_path), must_exist=True, write=True, context="ExportCookies")
        if not ok:
            console.print(Panel(f"[red]Erro: {msg}[/]", title="Erro de Exportação", border_style="red"))
            self.logger.log(f"Falha ao exportar cookies: {msg}", "ERROR", context="ExportCookies")
            input("Pressione Enter para continuar...")
            return
        try:
            shutil.copy2(self.cookie_file, export_path)
            console.print(f"[green]Cookies exportados para {export_path}[/]")
        except Exception as e:
            console.print(f"[red]Falha na exportação:[/] {e}")
        input("Pressione Enter para continuar...")
    def import_cookies(self):
        import_path = questionary.text(
            "Digite o caminho de importação:",
            style=custom_style).ask()
        ok, msg = validate_path(import_path, must_exist=True, write=False, context="ImportCookies")
        if not ok:
            console.print(Panel(f"[red]Erro: {msg}[/]", title="Erro de Importação", border_style="red"))
            self.logger.log(f"Falha ao importar cookies: {msg}", "ERROR", context="ImportCookies")
            input("Pressione Enter para continuar...")
            return
        try:
            shutil.copy2(import_path, self.cookie_file)
            console.print(f"[green]Cookies importados de {import_path}[/]")
        except Exception as e:
            console.print(f"[red]Falha na importação:[/] {e}")
        input("Pressione Enter para continuar...")
    def delete_cookies(self):
        if not os.path.exists(self.cookie_file):
            console.print("[yellow]Arquivo de cookies não existe.[/]")
            input("Pressione Enter para continuar...")
            return
        confirm = questionary.select(
            "Tem certeza que deseja excluir o arquivo de cookies?",
            choices=[
                {"name": "Sim", "value": True},
                {"name": "Não", "value": False}
            ],
            style=custom_style).ask()
        if confirm:
            os.remove(self.cookie_file)
            console.print("[green]Cookies excluídos.[/]")
        input("Pressione Enter para continuar...")
    def _read_cookies_file(self):
        try:
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    #  FIM - GERENCIAMENTO DE COOKIES

def validate_path(path: str, must_exist: bool = True, write: bool = False, context: str = "") -> (bool, str):
    """
    Valida se o caminho existe e se há permissão de leitura/escrita.
    Retorna (True, "") se ok, ou (False, mensagem de erro) se não.
    """
    try:
        # Converte para caminho absoluto
        path = os.path.abspath(os.path.expanduser(path))

        # Verifica se o caminho deve existir
        if must_exist and not os.path.exists(path):
            return False, f"Caminho não existe: {path}"

        # Verifica permissões de escrita
        if write:
            parent = path if os.path.isdir(path) else os.path.dirname(path)
            if not os.access(parent, os.W_OK):
                return False, f"Sem permissão de escrita para: {parent}"
        else:
            # Verifica permissões de leitura
            if not os.access(path, os.R_OK):
                return False, f"Sem permissão de leitura para: {path}"

        # Validação bem-sucedida
        return True, ""
    except Exception as e:
        # Captura erros inesperados
        return False, f"Erro inesperado ao validar o caminho '{path}': {str(e)}"

class DependencyManager:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.console = Console()
        self.dependencies = {
            'yt-dlp': 'pip install --upgrade yt-dlp',
            'ffmpeg': 'pkg install -y ffmpeg',
            'mutagen': 'pip install --upgrade mutagen',
            'yaspin': 'pip install --upgrade yaspin',
            'rich': 'pip install --upgrade rich',
            'questionary': 'pip install --upgrade questionary',
            'mpv': 'pkg install -y mpv',
        }
        self.dependency_modules = {
            'yt-dlp': 'yt_dlp',
            'mutagen': 'mutagen',
            'yaspin': 'yaspin',
            'rich': 'rich',
            'questionary': 'questionary'
        }
        self.install_flag_file = "/sdcard/Yt-dlp/.deps_installed"
    def check_ffmpeg(self):
        try:
            result = subprocess.run(
                ['command', '-v', 'ffmpeg'], 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            return result.returncode == 0
        except:
            return False
    def check_mpv(self):
        """
        Verifica se o mpv está disponível no sistema.
        """
        try:
            result = subprocess.run(
                ['command', '-v', 'mpv'],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.returncode == 0
        except:
            return False
    def dependency_installed(self, dep):
        if dep == 'ffmpeg':
            return self.check_ffmpeg()
        elif dep == 'mpv':
            return self.check_mpv()
        elif dep in self.dependency_modules:
            try:
                __import__(self.dependency_modules[dep])
                return True
            except ImportError:
                return False
        return False
    def check_all_dependencies(self):
        for dep in self.dependencies:
            if not self.dependency_installed(dep):
                return False
        return True
    def install_dependency(self, dep, install_cmd, action="Baixando"):
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold {self.theme_color}]{task.description}"),
            transient=False,
            refresh_per_second=20,
            console=self.console
        ) as progress:
            task = progress.add_task(f"{action} {dep}...", total=None)
            try:
                process = subprocess.run(
                    install_cmd, 
                    shell=True, 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
            except Exception as e:
                self.logger.log(f"Falha ao {action.lower()} {dep}: {e}", "ERROR")
            progress.remove_task(task)
            time.sleep(0.2)
    def check_dependencies(self):
        if os.path.exists(self.install_flag_file) and self.check_all_dependencies():
            return
        for dep, install_cmd in self.dependencies.items():
            if not self.dependency_installed(dep):
                self.install_dependency(dep, install_cmd, action="Baixando")
                self.logger.log(f"Dependência instalada: {dep}")
        if self.check_all_dependencies():
            with open(self.install_flag_file, 'w') as f:
                f.write('ok')
        else:
            self.logger.log("Algumas dependências falharam na instalação.", "ERROR")
    def update_all_dependencies(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold {self.theme_color}]{task.description}"),
            transient=False,
            refresh_per_second=20,
            console=self.console
        ) as progress:
            task = progress.add_task("Atualizando ...", total=None)
            for dep, install_cmd in self.dependencies.items():
                progress.update(task, description=f"Atualizando {dep}...")
                try:
                    subprocess.run(
                        install_cmd, 
                        shell=True, 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL
                    )
                    self.logger.log(f"Dependência atualizada: {dep}")
                except Exception as e:
                    self.logger.log(f"Falha ao atualizar {dep}: {e}", "ERROR")
                time.sleep(0.2)
            progress.remove_task(task)
            time.sleep(0.5)
    def update_ytdlp(self):
        self.update_all_dependencies()

class Downloader:
    def __init__(self, config: DownloaderConfig):
        self.config = config
        self.logger = config.logger
        self.console = Console()
        self.progress = None
        self.current_task = None
        self.download_queue: list[str] = []  # type annotation added
        self.executor = ThreadPoolExecutor(max_workers=config.max_concurrent_downloads)
        self.theme_color = config.theme_color

    def check_mpv(self):
        """
        Verifica se o mpv está disponível no sistema.
        """
        try:
            result = subprocess.run(
                ['command', '-v', 'mpv'],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.returncode == 0
        except:
            return False

    def get_title_from_url(self, url):
        """
        Usa yt-dlp para obter o título de um vídeo ou áudio URL sem fazer download.
        """
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get("title", url)
        except Exception:
            return url

    def ensure_mpv(self):
        dep_manager = DependencyManager(self.logger)
        if not dep_manager.check_mpv():
            dep_manager.install_dependency('mpv', dep_manager.dependencies['mpv'])
        if not dep_manager.check_mpv():
            console.print("[red]O mpv não está instalado e não pôde ser instalado automaticamente.[/]")
            time.sleep(2)
            return False
        return True

    def play_music_menu(self):
        while True:
            clear_screen()
            mpv_status = "[green]Disponível[/]" if self.check_mpv() else "[red]Não Disponível[/]"
            console.print(Panel.fit(
                f"[bold {self.config.theme_color}]Reprodutor de Música[/]\n" +
                f"[bold {self.config.theme_color}]Player MPV: {mpv_status} | Pasta: {self.config.audio_path}[/]",
                border_style=self.config.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Reproduzir Música Online", "value": "online"},
                    {"name": "Reproduzir Todas as Músicas Baixadas", "value": "play_all_local"},
                    {"name": "Reproduzir Música Baixada", "value": "local"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "back":
                break
            elif choice == "online":
                self.play_online_music_menu()
            elif choice == "local":
                self.play_downloaded_music_menu()
            elif choice == "play_all_local":
                self.play_all_downloaded_music()
    
    def play_all_downloaded_music(self):
        audio_dir = self.config.audio_path
        exts = ['*.mp3', '*.m4a', '*.aac', '*.opus', '*.ogg', '*.wav', '*.flac']
        files = []
        for ext in exts:
            files.extend(glob.glob(os.path.join(audio_dir, '**', ext), recursive=True))
        files = sorted(files)
        clear_screen()
        if not files:
            console.print("[yellow]Nenhuma música encontrada na pasta de áudio.[/]")
            time.sleep(2)
            return
        if not self.ensure_mpv():
            return
        for music_file in files:
            clear_screen()
            music_name = os.path.relpath(music_file, audio_dir)
            console.print(f"[bold {self.config.theme_color}]Reproduzindo:[/] {music_name}")
            time.sleep(0.5)
            subprocess.run(['mpv', music_file])
            clear_screen()

    def play_online_music_menu(self):
        while True:
            clear_screen()
            console.print(Panel.fit(
                f"[bold {self.config.theme_color}]Reproduzir Música Online[/]\n" +
                f"[bold {self.config.theme_color}]Streaming Direto do YouTube sem Download[/]",
                border_style=self.config.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Inserir nova URL", "value": "url"},
                    {"name": "Histórico", "value": "history"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "back":
                break
            elif choice == "url":
                url = questionary.text(
                    "Digite a URL da música (YouTube, mp3, etc):",
                    style=custom_style
                ).ask()
                if url and url.strip():
                    self._play_online_music(url)
            elif choice == "history":
                history = self.get_online_history()
                if not history:
                    console.print("[yellow]Histórico vazio.[/]")
                    time.sleep(2)
                    continue
                # Display titles and play corresponding URL
                choices = [{"name": item["title"], "value": item["url"]} for item in history]
                # Only show "Back" in music selection, not in delete menu
                choices.append({"name": "Voltar", "value": "back"})
                url = questionary.select(
                    "Selecione uma música do histórico:",
                    choices=choices,
                    style=custom_style
                ).ask()
                if url and url != "back":
                    self._play_online_music(url)

    def _play_online_music(self, url):
        if not self.ensure_mpv():
            return
        title = self.get_title_from_url(url)
        if title:
            self.save_online_history(title, url)
        clear_screen()
        console.print(f"[bold {self.config.theme_color}]Reproduzindo:[/] {title}")
        subprocess.run(['mpv', url])
        clear_screen()

    def play_downloaded_music_menu(self):
        while True:
            audio_dir = self.config.audio_path
            exts = ['*.mp3', '*.m4a', '*.aac', '*.opus', '*.ogg', '*.wav', '*.flac']
            files = []
            for ext in exts:
                files.extend(glob.glob(os.path.join(audio_dir, '**', ext), recursive=True))
            files = sorted(files)
            clear_screen()
            
            file_count = len(files)
            console.print(Panel.fit(
                f"[bold {self.config.theme_color}]Reproduzir Músicas Baixadas[/]\n" +
                f"[bold {self.config.theme_color}]Total de Arquivos: {file_count} | Pasta: {audio_dir}[/]",
                border_style=self.config.theme_color
            ))
            if not files:
                console.print("[yellow]Nenhuma música baixada encontrada na sua pasta de áudio.[/]")
                time.sleep(2)
                break
            choices = [{"name": os.path.relpath(f, audio_dir), "value": f} for f in files]
            choices.append({"name": "Voltar", "value": "back"})
            selected = questionary.select(
                "Escolha um arquivo para reproduzir:",
                choices=choices,
                style=custom_style
            ).ask()
            if selected and selected != "back":
                if not self.ensure_mpv():
                    continue
                clear_screen()
                music_name = os.path.relpath(selected, audio_dir)
                console.print(f"[bold {self.config.theme_color}]Reproduzindo:[/] {music_name}")
                subprocess.run(['mpv', selected])
                clear_screen()
            elif selected == "back":
                break

    def _get_video_format_config(self):
        """
        Retorna a configuração de formato de vídeo baseada na qualidade pré-configurada.
        """
        quality = self.config.default_video_quality
        
        if quality == "best":
            return {"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}
        elif quality == "1080p":
            return {"format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]"}
        elif quality == "720p":
            return {"format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]"}
        elif quality == "480p":
            return {"format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]"}
        elif quality == "360p":
            return {"format": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]"}
        else:
            # Fallback para melhor qualidade se não reconhecer a configuração
            return {"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}

    def select_format(self, format_type: str):
        while True:
            clear_screen()
            current_format = self.config.default_audio_format if format_type == "audio" else self.config.default_video_format
            console.print(Panel.fit(
                f"[bold {self.config.theme_color}]Selecionar Formato de {format_type.title()}[/]\n" +
                f"[bold {self.theme_color}]Formato Atual: {current_format}[/]",
                border_style=self.theme_color
            ))
            if format_type == "audio":
                formats = [
                    {"name": "MP3 - 320kbps", "value": {"format": "mp3", "quality": "320kb"}},
                    {"name": "MP3 - 192kbps", "value": {"format": "mp3", "quality": "192kb"}},
                    {"name": "MP3 - 128kbps", "value": {"format": "mp3", "quality": "128kb"}},
                    {"name": "AAC - 192kbps", "value": {"format": "aac", "quality": "192kb"}},
                    {"name": "M4A - 192kbps", "value": {"format": "m4a", "quality": "192kb"}},
                    {"name": "OPUS - 160kbps", "value": {"format": "opus", "quality": "160kb"}},
                    {"name": "VORBIS - 192kbps", "value": {"format": "vorbis", "quality": "192kb"}}
                ]
            else:
                formats = [
                    {"name": "Best Quality MP4", "value": {"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}},
                    {"name": "1080p MP4", "value": {"format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]"}},
                    {"name": "720p MP4", "value": {"format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]"}},
                    {"name": "480p MP4", "value": {"format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]"}},
                    {"name": "360p MP4", "value": {"format": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]"}}
                ]
            formats.append({"name": "Voltar", "value": "back"})
            format_choice = questionary.select(
                "Escolha um formato:",
                choices=formats,
                style=custom_style
            ).ask()
            if format_choice == "back":
                return None
            return format_choice

    def is_valid_url(self, url: str) -> bool:
        return url.strip() and ('youtube.com' in url or 'youtu.be' in url or url.startswith("http"))

    def progress_hook(self, d):
        if self.progress is None or self.current_task is None:
            return
        if d['status'] == 'downloading':
            try:
                progress = float(d['_percent_str'].replace('%', ''))
                self.progress.update(self.current_task, completed=progress)
            except:
                pass
        elif d['status'] == 'finished':
            self.progress.update(self.current_task, description="[yellow]Processando arquivo...")

    def handle_playlist(self, url: str):
        if "playlist" not in url.lower():
            return None
        console.print("\n[yellow]Playlist detected![/]")
        download_all = questionary.confirm(
            "Download the entire playlist?",
            default=True,
            style=custom_style
        ).ask()
        if not download_all:
            items = questionary.text(
                "Enter item numbers (e.g. 1,3,5-7):",
                style=custom_style
            ).ask()
            return items
        return None

    def play_notification(self):
        if self.config.notification_sound:
            # Toca o arquivo de som definido pelo usuário, se possível
            sound_file = getattr(self.config, "notification_sound_file", None)
            if sound_file and os.path.exists(sound_file):
                try:
                    # Tenta tocar com vários players disponíveis
                    for player in ["aplay", "paplay", "cvlc", "ffplay", "mpg123", "play"]:
                        if shutil.which(player):
                            subprocess.Popen([player, sound_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            break
                    else:
                        print('\a')  # beep padrão como fallback
                except Exception:
                    print('\a')
            else:
                print('\a')

    def save_online_history(self, title: str, url: str):
        """
        Salva uma entrada no histórico de músicas reproduzidas online.
        """
        try:
            history = []
            if os.path.exists(HISTORY_FILE_ONLINE):
                with open(HISTORY_FILE_ONLINE, "r", encoding="utf-8") as f:
                    try:
                        history = json.load(f)
                    except:
                        history = []
            
            # Adiciona a nova entrada
            entry = {
                "title": title,
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            history.append(entry)
            
            # Mantém apenas os últimos 50 itens
            if len(history) > 50:
                history = history[-50:]
            
            with open(HISTORY_FILE_ONLINE, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.log(f"Erro ao salvar histórico online: {e}", "ERROR", context="SaveOnlineHistory")

    def get_online_history(self):
        """
        Obtém o histórico de músicas reproduzidas online.
        """
        try:
            if os.path.exists(HISTORY_FILE_ONLINE):
                with open(HISTORY_FILE_ONLINE, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    # Remove duplicatas mantendo a ordem mais recente
                    seen = set()
                    unique_history = []
                    for item in reversed(history):
                        key = (item.get("title"), item.get("url"))
                        if key not in seen:
                            unique_history.append(item)
                            seen.add(key)
                    return list(reversed(unique_history))
        except Exception as e:
            self.logger.log(f"Erro ao carregar histórico online: {e}", "ERROR", context="GetOnlineHistory")
        return []

    def _process_download(self, url: str, options: dict, download_type: str):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown Title')
                if self.config.auto_delete_temp:
                    cleanup_temp_files(
                        self.config.audio_path if download_type == 'audio' else self.config.video_path,
                        title
                    )
                self.play_notification()
                return True, title
        except Exception as e:
            return False, str(e)

    def _file_exists(self, output_path, title, ext_list):
        """
        Verifica se já existe um arquivo com o título e extensão na pasta de destino.
        """
        for ext in ext_list:
            candidate = os.path.join(output_path, f"{title}.{ext}")
            if os.path.exists(candidate):
                return candidate
        return None

    def _interactive_overwrite(self, filepath):
        """
        Exibe um menu interativo perguntando se o usuário deseja sobrescrever o arquivo existente.
        """
        filename = os.path.basename(filepath)
        choice = questionary.select(
            f"O arquivo '{filename}' já existe. Sobrescrever?",
            choices=[
                {"name": "Sim, sobrescrever", "value": True},
                {"name": "Não, cancelar", "value": False}
            ],
            style=custom_style
        ).ask()
        return choice

    def _validate_and_feedback(self, base_path, context, action="download"):
        """
        Valida caminho e permissão, mostra feedback visual e loga se houver erro.
        Retorna True se ok, False se erro.
        """
        ok, msg = validate_path(base_path, must_exist=True, write=True, context=context)
        if not ok:
            console.print(Panel(f"[red]Erro: {msg}[/]", title="Erro de Caminho", border_style="red"))
            self.logger.log(f"{action.capitalize()} falhou: {msg}", "ERROR", context=context)
            time.sleep(2)
            return False
        return True

    def _build_output_path(self, base_path):
        if self.config.create_subfolders:
            return os.path.join(base_path, "%(uploader)s/%(playlist_title)s/")
        return base_path

    def _build_audio_options(self, output_path, audio_format):
        opts = {
            'format': 'bestaudio/best',
            'cookiefile': self.config.cookie_file,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format['format'],
                    'preferredquality': audio_format['quality'],
                },
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegMetadata'},
            ],
            'progress_hooks': [self.progress_hook],
            'writethumbnail': True,
            'embedthumbnail': True,
            'convert-thumbnails': True,
            'quiet': True,
            'no_warnings': True
        }
        if self.config.proxy_url:
            opts['proxy'] = self.config.proxy_url
        return opts

    def _build_video_options(self, output_path, video_format):
        opts = {
            'format': video_format['format'],
            'cookiefile': self.config.cookie_file,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'writesubtitles': self.config.download_subtitles,
            'subtitleslangs': self.config.subtitle_languages,
            'postprocessors': [
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegVideoRemuxer', 'preferedformat': 'mp4'},
                {'key': 'FFmpegMetadata'},
            ],
            'progress_hooks': [self.progress_hook],
            'writethumbnail': True,
            'embedthumbnail': True,
            'convert-thumbnails': True,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True
        }
        if self.config.proxy_url:
            opts['proxy'] = self.config.proxy_url
        return opts

    def download_audio(self, url: str, playlist_items: str = None):
        if "tiktok.com" in url.lower():
            cookie_valid = self.config._validate_tiktok_cookie()
            if cookie_valid:
                console.print("[green]Cookies do TikTok são válidos![/]")
            else:
                console.print("[red]Aviso: Cookies do TikTok são inválidos ou expiraram! Você pode não conseguir baixar vídeos privados.[/]")
            time.sleep(1)
        
        # Usar qualidade pré-configurada ao invés de mostrar seletor
        audio_format = {
            "format": self.config.default_audio_format,
            "quality": self.config.default_audio_quality
        }
        
        clear_screen()
        console.print(f"[{self.config.theme_color}]Usando configuração de áudio:[/] {audio_format['format'].upper()} - {audio_format['quality']}")
        time.sleep(1)
        
        if not self.is_valid_url(url):
            console.print("[red]URL inválida! Retornando ao menu...[/]")
            time.sleep(2)
            return
            console.print("[red]URL inválida! Retornando ao menu...[/]")
            time.sleep(2)
            return
        output_path = self._build_output_path(self.config.audio_path)
        if not self._validate_and_feedback(self.config.audio_path, context="DownloadAudio", action="audio download"):
            return
        # Obter título antes do download
        title = self.get_title_from_url(url)
        # Verificar se arquivo já existe
        ext = audio_format['format']
        # Considerar possíveis extensões de áudio
        ext_list = [ext, "mp3", "m4a", "aac", "opus", "ogg", "wav", "flac"]
        # Substituir variáveis do yt-dlp por valores reais para checar existência
        real_output_path = output_path
        if "%(uploader)s" in real_output_path or "%(playlist_title)s" in real_output_path:
            real_output_path = self.config.audio_path  # fallback para pasta base
        existing_file = self._file_exists(real_output_path, title, ext_list)
        if existing_file:
            if not self._interactive_overwrite(existing_file):
                console.print("[yellow]Download cancelado pelo usuário.[/]")
                time.sleep(2)
                return
        options = self._build_audio_options(output_path, audio_format)
        if playlist_items:
            options['playlist_items'] = playlist_items
        else:
            playlist_items_from_url = self.handle_playlist(url)
            if playlist_items_from_url:
                options['playlist_items'] = playlist_items_from_url
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            self.progress = progress
            self.current_task = progress.add_task(
                f"[{self.config.theme_color}]Baixando...", 
                total=100
            )
            success, result = self._process_download(url, options, 'audio')
            if success:
                progress.update(self.current_task, description="[green]Download concluído!")
                self.logger.log(f"Download de áudio concluído: {result}")
                console.print(f"\n[bold green]✓[/] Baixado: {result}")
            else:
                progress.update(self.current_task, description="[red]Erro no download!")
                self.logger.log(f"Erro no download de áudio: {result}", "ERROR")
                console.print(f"\n[red]Erro:[/] {result}")
        time.sleep(2)

    def download_video(self, url: str, playlist_items: str = None):
        if "tiktok.com" in url.lower():
            cookie_valid = self.config._validate_tiktok_cookie()
            if cookie_valid:
                console.print("[green]Cookies do TikTok são válidos![/]")
            else:
                console.print("[red]Aviso: Cookies do TikTok são inválidos ou expiraram! Você pode não conseguir baixar vídeos privados.[/]")
            time.sleep(1)
        
        # Usar qualidade pré-configurada ao invés de mostrar seletor
        video_format = self._get_video_format_config()
        
        clear_screen()
        console.print(f"[{self.config.theme_color}]Usando configuração de vídeo:[/] {self.config.default_video_quality}")
        time.sleep(1)
        
        if not self.is_valid_url(url):
            console.print("[red]URL inválida! Retornando ao menu...[/]")
            time.sleep(2)
            return
            console.print("[red]URL inválida! Retornando ao menu...[/]")
            time.sleep(2)
            return
        output_path = self._build_output_path(self.config.video_path)
        if not self._validate_and_feedback(self.config.video_path, context="DownloadVideo", action="video download"):
            return
        # Obter título antes do download
        title = self.get_title_from_url(url)
        # Verificar se arquivo já existe
        ext_list = ["mp4", "mkv", "webm"]
        real_output_path = output_path
        if "%(uploader)s" in real_output_path or "%(playlist_title)s" in real_output_path:
            real_output_path = self.config.video_path  # fallback para pasta base
        existing_file = self._file_exists(real_output_path, title, ext_list)
        if existing_file:
            if not self._interactive_overwrite(existing_file):
                console.print("[yellow]Download cancelado pelo usuário.[/]")
                time.sleep(2)
                return
        options = self._build_video_options(output_path, video_format)
        if playlist_items:
            options['playlist_items'] = playlist_items
        else:
            playlist_items_from_url = self.handle_playlist(url)
            if playlist_items_from_url:
                options['playlist_items'] = playlist_items_from_url
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            self.progress = progress
            self.current_task = progress.add_task(
                f"[{self.config.theme_color}]Baixando...", 
                total=100
            )
            success, result = self._process_download(url, options, 'video')
            if success:
                progress.update(self.current_task, description="[green]Download concluído!")
                self.logger.log(f"Download de vídeo concluído: {result}")
                console.print(f"\n[bold green]✓[/] Baixado: {result}")
            else:
                progress.update(self.current_task, description="[red]Erro no download!")
                self.logger.log(f"Erro no download de vídeo: {result}", "ERROR")
                console.print(f"\n[red]Erro:[/] {result}")
        time.sleep(2)

class Menu:
    def __init__(self):
        self.config = DownloaderConfig()
        self.dependency_manager = DependencyManager(self.config.logger)
        self.downloader = Downloader(self.config)
        self.console = Console()
        self.script_filename = os.path.abspath(__file__)
        self.backup_filename = self.script_filename.replace('.py', '_backup.py')
        self.github_raw_url = "https://raw.githubusercontent.com/Reyzn24/youtube_downloader_linux_termux/main/youtuber_download_termux(beta).py"
        self.theme_color = self.config.theme_color

    def update_menu(self):
        clear_screen()
        self.console.print(Panel.fit(
            f"[bold {self.theme_color}]Atualizar Dependências[/]\n" +
            f"[bold {self.theme_color}]yt-dlp, ffmpeg, e componentes do sistema[/]",
            border_style=self.theme_color
        ))
        confirm = questionary.confirm(
            "Deseja atualizar todas as dependências (yt-dlp, ffmpeg, etc)?",
            default=True,
            style=custom_style
        ).ask()
        if confirm:
            self.dependency_manager.update_all_dependencies()
            self.console.print("[green]Dependências atualizadas![/]")
            time.sleep(2)
        else:
            self.console.print("[yellow]Atualização cancelada.[/]")
            time.sleep(1)

    def display_header(self):
        clear_screen()
        console.print(Panel.fit(
            f"[bold {self.theme_color}]YouTube Downloader v{VERSION}[/]\n"
            f"[yellow]Autor:[/] {AUTHOR}\n"
            f"[yellow]Última Atualização:[/] {LAST_UPDATED}\n"
            f"[bold {self.theme_color}]Áudio: {self.config.default_audio_format} | Vídeo: {self.config.default_video_format} | Tema: {self.config.theme_color}[/]",
            border_style=self.theme_color
        ))

    def download_menu(self):
        while True:
            clear_screen()
            audio_format = self.config.default_audio_format
            video_format = self.config.default_video_format
            console.print(Panel.fit(
                f"[bold {self.config.theme_color}]Opções de Download[/]\n" +
                f"[bold {self.config.theme_color}]Formatos: Áudio: {audio_format} | Vídeo: {video_format}[/]",
                border_style=self.config.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Música", "value": "1"},
                    {"name": "Vídeo", "value": "2"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "1":
                url = questionary.text(
                    "Digite a URL (ou pressione Enter para voltar):",
                    style=custom_style
                ).ask()
                if not url or not url.strip():
                    continue
                self.downloader.download_audio(url)
            elif choice == "2":
                url = questionary.text(
                    "Digite a URL (ou pressione Enter para voltar):",
                    style=custom_style
                ).ask()
                if not url or not url.strip():
                    continue
                self.downloader.download_video(url)
            elif choice == "back":
                break

    def update_menu(self):
        while True:
            clear_screen()
            self.console.print(Panel.fit(
                f"[bold {self.theme_color}]Atualizações[/]\n" +
                f"[bold {self.theme_color}]Dependências: yt-dlp, ffmpeg | Script: v1.0[/]",
                border_style=self.theme_color
            ))
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Atualizar dependências", "value": "deps"},
                    {"name": "Atualizar script do GitHub", "value": "script"},
                    {"name": "Voltar", "value": "back"}
                ],
                style=custom_style
            ).ask()
            if choice == "deps":
                self.dependency_manager.update_all_dependencies()
                self.console.print("[green]Dependências atualizadas![/]")
                time.sleep(2)
            elif choice == "script":
                self.update_script_from_github()
                time.sleep(2)
            elif choice == "back":
                break

    def update_script_from_github(self):
        """
        Atualiza o script baixando a versão mais recente do GitHub.
        """
        try:
            self.console.print("[yellow]Baixando atualização do script...[/]")
            
            # Fazer backup do script atual
            if os.path.exists(self.script_filename):
                shutil.copy2(self.script_filename, self.backup_filename)
                self.console.print(f"[green]Backup criado: {self.backup_filename}[/]")
            
            # Baixar nova versão
            response = requests.get(self.github_raw_url, timeout=30)
            response.raise_for_status()
            
            # Salvar nova versão
            with open(self.script_filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            self.console.print("[green]Script atualizado com sucesso![/]")
            self.console.print("[yellow]Reinicie o programa para usar a nova versão.[/]")
            
        except requests.RequestException as e:
            self.console.print(f"[red]Erro ao baixar atualização: {e}[/]")
            self.config.logger.log(f"Erro na atualização do script: {e}", "ERROR", context="UpdateScript")
        except Exception as e:
            self.console.print(f"[red]Erro inesperado durante atualização: {e}[/]")
            self.config.logger.log(f"Erro inesperado na atualização: {e}", "ERROR", context="UpdateScript")
            
            # Restaurar backup em caso de erro
            if os.path.exists(self.backup_filename):
                try:
                    shutil.copy2(self.backup_filename, self.script_filename)
                    self.console.print("[yellow]Backup restaurado devido ao erro.[/]")
                except Exception as restore_error:
                    self.console.print(f"[red]Erro ao restaurar backup: {restore_error}[/]")

    def main_menu(self):
        self.dependency_manager.check_dependencies()
        while True:
            self.display_header()
            choice = questionary.select(
                "Escolha uma opção:",
                choices=[
                    {"name": "Download (música e vídeo)", "value": "1"},
                    {"name": "Download de Playlist (escolher itens)", "value": "playlist"},
                    {"name": "Reproduzir Música (online ou offline)", "value": "6"},
                    {"name": "Atualizar", "value": "2"},
                    {"name": "Configurações", "value": "3"},
                    {"name": "Sair", "value": "5"}
                ],
                style=custom_style
            ).ask()
            if choice == "1":
                self.download_menu()
            elif choice == "playlist":
                self.download_playlist_menu()
            elif choice == "2":
                self.update_menu()
            elif choice == "3":
                self.config.configure_paths()
            elif choice == "5":
                console.print(f"\n[{self.config.theme_color}]Obrigado por usar o YouTube Downloader![/]")
                break
            elif choice == "6":
                self.downloader.play_music_menu()

    def download_playlist_menu(self):
        while True:
            clear_screen()
            console.print(Panel.fit(
                f"[bold {self.config.theme_color}]Download de Playlist[/]\n" +
                f"[bold {self.config.theme_color}]Seleção de Itens | Formato: {self.config.default_audio_format}/{self.config.default_video_format}[/]",
                border_style=self.config.theme_color
            ))
            url = questionary.text(
                "Digite a URL da playlist (ou deixe em branco para voltar):",
                style=custom_style
            ).ask()
            if not url or not url.strip():
                return
            try:
                with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True, "skip_download": True, "forcejson": True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                if "entries" not in info or not info["entries"]:
                    console.print("[red]Nenhum item encontrado na playlist.[/]")
                    time.sleep(2)
                    continue
                entries = info["entries"]
                choices = [
                    {"name": f"{i+1}. {entry.get('title', 'No Title')}", "value": entry["id"]}
                    for i, entry in enumerate(entries)
                ]
                choices.append({"name": "Voltar", "value": "back"})
                selected_ids = questionary.checkbox(
                    "Selecione itens para download (espaço para selecionar, Enter para confirmar):",
                    choices=choices,
                    style=custom_style
                ).ask()
                if not selected_ids or "back" in selected_ids:
                    continue
                download_type = questionary.select(
                    "Baixar como:",
                    choices=[
                        {"name": "Áudio", "value": "audio"},
                        {"name": "Vídeo", "value": "video"},
                        {"name": "Voltar", "value": "back"}
                    ],
                    style=custom_style
                ).ask()
                if download_type == "back":
                    continue
                indices = [str(i+1) for i, entry in enumerate(entries) if entry["id"] in selected_ids]
                playlist_items = ",".join(indices)
                if download_type == "audio":
                    self.downloader.download_audio(f"{url}", playlist_items=playlist_items)
                else:
                    self.downloader.download_video(f"{url}", playlist_items=playlist_items)
            except Exception as e:
                console.print(f"[red]Falha ao obter informações da playlist: {e}[/]")
                self.config.logger.log(f"Falha ao obter informações da playlist: {e}", "ERROR", context="DownloadPlaylist")
                time.sleep(2)
                continue
# --- Fim da classe Menu ---

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()

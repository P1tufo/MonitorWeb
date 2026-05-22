import os
import subprocess

def quit_app(app_name):
    """Cierra una aplicación de forma segura usando AppleScript."""
    script = f'tell application "{app_name}" to quit'
    try:
        subprocess.run(["osascript", "-e", script], capture_output=True, check=True)
        return True
    except:
        return False

def main():
    # Lista de aplicaciones que suelen consumir mucha RAM en segundo plano
    apps_to_close = [
        "Google Chrome",
        "Slack",
        "Spotify",
        "Discord",
        "Microsoft Teams",
        "Microsoft Outlook",
        "Microsoft Excel",
        "Microsoft Word",
        "Mail",
        "Calendar",
        "Notes",
        "WhatsApp",
        "Telegram"
    ]

    print("--- Optimizador de Memoria MonitorWeb ---")
    print("Cerrando aplicaciones de alto consumo...")

    closed_count = 0
    for app in apps_to_close:
        if quit_app(app):
            print(f" [✓] {app} cerrado.")
            closed_count += 1
    
    if closed_count == 0:
        print(" [!] No se encontraron aplicaciones abiertas de la lista.")
    else:
        print(f"\nSe han cerrado {closed_count} aplicaciones.")
    
    print("\n--- Estado de Memoria Actual ---")
    # Mostrar el Top 5 de procesos por memoria (excluyendo Ollama)
    try:
        cmd = "ps -eo pmem,comm | sort -rn | head -n 10"
        output = subprocess.check_output(cmd, shell=True).decode()
        print("Top 10 procesos (por % de RAM):")
        print(output)
    except:
        pass

    print("\nSugerencia: Ejecuta 'ollama gc' en la terminal si quieres forzar la limpieza de modelos antiguos.")

if __name__ == "__main__":
    main()

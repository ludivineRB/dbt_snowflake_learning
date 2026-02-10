#!/bin/bash
# =============================================
#   FORMULE ANCESTRALE DES ANCIENS
#   Console d'activation du ZPM-GAMMA
# =============================================

# --- Fonctions de bruitages ---
beep_chevron() {
    if command -v afplay &>/dev/null; then
        afplay /System/Library/Sounds/Tink.aiff &>/dev/null &
    else
        printf '\a'
    fi
}

beep_lock() {
    if command -v afplay &>/dev/null; then
        afplay /System/Library/Sounds/Glass.aiff &>/dev/null &
    else
        printf '\a'
    fi
}

beep_kawoosh() {
    if command -v afplay &>/dev/null; then
        afplay /System/Library/Sounds/Submarine.aiff &>/dev/null &
    else
        printf '\a'
    fi
}

beep_success() {
    if command -v afplay &>/dev/null; then
        afplay /System/Library/Sounds/Hero.aiff &>/dev/null &
    else
        printf '\a'
    fi
}

generate_python_script() {
    cat << 'PYTHON_EOF' > sauver_atlantis.py
#!/usr/bin/env python3
import time
import sys
import subprocess
import os

CYAN = '\033[1;36m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
WHITE = '\033[1;37m'
NC = '\033[0m'

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def play_sound(sound_name):
    try:
        sound_path = f"/System/Library/Sounds/{sound_name}.aiff"
        if os.path.exists(sound_path):
            subprocess.Popen(["afplay", sound_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            sys.stdout.write('\a')
    except Exception:
        sys.stdout.write('\a')

def loading_bar(label, duration=2.0, width=30):
    sys.stdout.write(f"  {label} [")
    sys.stdout.flush()
    for i in range(width):
        time.sleep(duration / width)
        sys.stdout.write("=")
        sys.stdout.flush()
    play_sound("Pop")
    sys.stdout.write(f"] {GREEN}[OK]{NC}\n")
    sys.stdout.flush()

print()
print(f"{CYAN}=============================================")
print(f"   CITE D ATLANTIS - GALAXIE DE PEGASE")
print(f"============================================={NC}")
print()

time.sleep(0.5)
slow_print(f"{YELLOW}  Insertion du ZPM-GAMMA...{NC}", 0.05)
time.sleep(0.5)

print()
print(f"{WHITE}  Initialisation des systemes d'Atlantis:{NC}")
print()

loading_bar("Alimentation de la cite...", 1.5)
loading_bar("Bouclier active...........", 1.2)
loading_bar("Systemes de survie........", 1.0)
loading_bar("Moteurs subluminiques.....", 0.8)
loading_bar("Propulsion hyperspatiale..", 1.5)
loading_bar("Capteurs longue portee....", 0.6)
loading_bar("Drones de defense.........", 0.8)

print()
time.sleep(0.5)

zpm = f"""{CYAN}
         _____
        /     \\
       / () () \\
      |  \\   /  |
      |   | |   |
       \\  |_|  /
        \\_____/
       [ZPM-GAMMA]
        ACTIF !{NC}
"""
for line in zpm.split('\n'):
    print(line)
    time.sleep(0.1)

time.sleep(0.5)
print(f"{GREEN}")
play_sound("Hero")
slow_print("  *** ATLANTIS EST SAUVEE! ***", 0.06)
print()
slow_print("  Felicitations, SG-nouveau!", 0.04)
slow_print("  Vous avez accompli votre mission avec brio.", 0.03)
slow_print("  Le General Landry est fier de vous.", 0.03)
slow_print("  Bienvenue dans les equipes SG.", 0.03)
print()
slow_print(f'  {WHITE}"In the middle of difficulty lies opportunity"', 0.04)
slow_print(f"    - Les Anciens (et aussi Albert Einstein){NC}", 0.03)
print()
print(f"{GREEN}=============================================")
print(f"   MISSION ACCOMPLIE")
print(f"============================================={NC}")
print()
PYTHON_EOF
}

echo ""
echo "============================================="
echo "   CONSOLE D'ACTIVATION - ANCIENS"
echo "============================================="
echo ""

# Verification du code iris
if [[ -z "$CODE" ]]; then
    echo "ERREUR: Variable CODE non definie."
    echo "Utilisez: export CODE=\"votre_code_iris\""
    echo "avant de relancer le script."
    exit 1
fi

# Demande du second mot de passe
echo -n "Entrez le second mot de passe (decouvert via le DHD): "
read PASS
echo ""

if [[ "$CODE" = "kree" ]] && [[ "$PASS" = "vortex" ]]; then
    echo "============================================="
    echo "   ACCES AUTORISE"
    echo "============================================="
    echo ""
    for i in 1 2 3 4 5 6; do
        beep_chevron
        echo "  Chevron $i... encode."
        sleep 0.8 2>/dev/null || true
    done
    beep_lock
    echo "  Chevron 7... VERROUILLE!"
    sleep 1 2>/dev/null || true
    echo ""
    beep_kawoosh
    echo "*KAWOOSH* - Le vortex s'ouvre vers Atlantis!"
    echo ""
    beep_success
    echo "Generation du module d'alimentation..."
    generate_python_script
    echo ""
    echo "Le fichier 'sauver_atlantis.py' a ete cree!"
    echo "Executez-le pour alimenter Atlantis:"
    echo "  python3 sauver_atlantis.py"
    echo ""
elif [[ "$CODE" = "kree" ]] && [[ "$PASS" != "vortex" ]]; then
    echo "Le second mot de passe est incorrect."
    echo "Indice: retournez au DHD (porte_des_etoiles/) et"
    echo "relisez les instructions. ls -lS est votre ami."
elif [[ "$CODE" != "kree" ]] && [[ "$PASS" = "vortex" ]]; then
    echo "Le code iris est incorrect."
    echo "Indice: retournez au SGC et cherchez le journal"
    echo "de Walter dans la salle de controle."
else
    echo "Code iris ET mot de passe incorrects!"
    echo "Retournez au SGC et au DHD pour les retrouver."
fi

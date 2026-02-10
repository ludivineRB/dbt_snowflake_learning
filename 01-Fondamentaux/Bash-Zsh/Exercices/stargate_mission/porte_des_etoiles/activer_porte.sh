#!/bin/bash
# =============================================
#   ACTIVATION DE LA PORTE DES ETOILES
#   Animation ASCII - SGC
# =============================================

clear 2>/dev/null || true

BLUE='\033[1;34m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
GREEN='\033[1;32m'
WHITE='\033[1;37m'
NC='\033[0m'

# --- Fonctions de bruitages ---
# Utilise les sons macOS si disponibles, sinon le bip terminal
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

gate_inactive() {
    echo -e "${WHITE}"
    echo "          .:xxxXXXXXXXxxx:."
    echo "       .xXXXXXXXXXXXXXXXXXXx."
    echo "     .XXXXXXXXX.:::.XXXXXXXXX."
    echo "   .XXXXXXX.           .XXXXXXX."
    echo "  .XXXXXX.               .XXXXXX."
    echo " .XXXXX.                   .XXXXX."
    echo " XXXXX.                     .XXXXX"
    echo " XXXX.                       .XXXX"
    echo " XXXX           SGC           XXXX"
    echo " XXXX.                       .XXXX"
    echo " XXXXX.                     .XXXXX"
    echo " .XXXXX.                   .XXXXX."
    echo "  .XXXXXX.               .XXXXXX."
    echo "   .XXXXXXX.           .XXXXXXX."
    echo "     .XXXXXXXXX.:::.XXXXXXXXX."
    echo "       .xXXXXXXXXXXXXXXXXXXx."
    echo "          .:xxxXXXXXXXxxx:."
    echo -e "${NC}"
}

gate_chevron() {
    local num=$1
    local color=$2
    echo -e "${color}"
    echo "          .:xxxXXXXXXXxxx:."
    echo "       .xXXX[ CHEVRON $num ]XXXx."
    echo "     .XXXXXXXXX.:::.XXXXXXXXX."
    echo "   .XXXXXXX.    |||    .XXXXXXX."
    echo "  .XXXXXX.       |      .XXXXXX."
    echo " .XXXXX.                  .XXXXX."
    echo " XXXXX.                    .XXXXX"
    echo " XXXX---                  ---XXXX"
    echo " XXXX        P3X-974        XXXX"
    echo " XXXX---                  ---XXXX"
    echo " XXXXX.                    .XXXXX"
    echo " .XXXXX.                  .XXXXX."
    echo "  .XXXXXX.              .XXXXXX."
    echo "   .XXXXXXX.          .XXXXXXX."
    echo "     .XXXXXXXXX.:::.XXXXXXXXX."
    echo "       .xXXXXXXXXXXXXXXXXXXx."
    echo "          .:xxxXXXXXXXxxx:."
    echo -e "${NC}"
}

gate_active() {
    echo -e "${CYAN}"
    echo "          .:xxxXXXXXXXxxx:."
    echo "       .xXXXXXXXXXXXXXXXXXXx."
    echo "     .XXXXXXXXX.:::.XXXXXXXXX."
    echo "   .XXXXXXX.  ~~~~~~~  .XXXXXXX."
    echo "  .XXXXXX. ~~~~~~~~~~~~~ .XXXXXX."
    echo " .XXXXX. ~~~~~~~~~~~~~~~~~ .XXXXX."
    echo " XXXXX. ~~~~~~~~~~~~~~~~~~~ .XXXXX"
    echo " XXXX. ~~~~~~~~~~~~~~~~~~~~~ .XXXX"
    echo " XXXX ~~~~~~~ KAWOOSH ~~~~~~~ XXXX"
    echo " XXXX. ~~~~~~~~~~~~~~~~~~~~~ .XXXX"
    echo " XXXXX. ~~~~~~~~~~~~~~~~~~~ .XXXXX"
    echo " .XXXXX. ~~~~~~~~~~~~~~~~~ .XXXXX."
    echo "  .XXXXXX. ~~~~~~~~~~~~~ .XXXXXX."
    echo "   .XXXXXXX.  ~~~~~~~  .XXXXXXX."
    echo "     .XXXXXXXXX.:::.XXXXXXXXX."
    echo "       .xXXXXXXXXXXXXXXXXXXx."
    echo "          .:xxxXXXXXXXxxx:."
    echo -e "${NC}"
}

gate_stable() {
    echo -e "${BLUE}"
    echo "          .:xxxXXXXXXXxxx:."
    echo "       .xXXXXXXXXXXXXXXXXXXx."
    echo "     .XXXXXXXXX.:::.XXXXXXXXX."
    echo "   .XXXXXXX.  .......  .XXXXXXX."
    echo "  .XXXXXX. ............. .XXXXXX."
    echo " .XXXXX. ................. .XXXXX."
    echo " XXXXX. ................... .XXXXX"
    echo " XXXX. ..................... .XXXX"
    echo " XXXX ..... VORTEX STABLE ... XXXX"
    echo " XXXX. ..................... .XXXX"
    echo " XXXXX. ................... .XXXXX"
    echo " .XXXXX. ................. .XXXXX."
    echo "  .XXXXXX. ............. .XXXXXX."
    echo "   .XXXXXXX.  .......  .XXXXXXX."
    echo "     .XXXXXXXXX.:::.XXXXXXXXX."
    echo "       .xXXXXXXXXXXXXXXXXXXx."
    echo "          .:xxxXXXXXXXxxx:."
    echo -e "${NC}"
}

# Animation principale
echo ""
echo -e "${WHITE}=== PORTE DES ETOILES - ACTIVATION ===${NC}"
echo ""
sleep 1

gate_inactive
sleep 1

for i in 1 2 3 4 5 6; do
    clear 2>/dev/null || true
    echo ""
    echo -e "${YELLOW}  >>> Chevron $i... encode. <<<${NC}"
    echo ""
    beep_chevron
    gate_chevron "$i" "$YELLOW"
    sleep 0.8
done

clear 2>/dev/null || true
echo ""
echo -e "${RED}  >>> Chevron 7... VERROUILLE! <<<${NC}"
echo ""
beep_lock
gate_chevron "7" "$RED"
sleep 1

clear 2>/dev/null || true
echo ""
echo -e "${CYAN}  >>> *KAWOOSH* <<<${NC}"
echo ""
beep_kawoosh
gate_active
sleep 1.5

clear 2>/dev/null || true
echo ""
echo -e "${BLUE}  >>> Vortex stabilise <<<${NC}"
echo ""
gate_stable
sleep 1

beep_success
echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}  La Porte est ouverte vers P3X-974!${NC}"
echo -e "${GREEN}  Traversez le vortex...${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""
echo -e "${WHITE}Direction: planete_P3X_974/${NC}"
echo -e "${WHITE}(Mais attention, il y a aussi d'autres planetes...${NC}"
echo -e "${WHITE} Seule P3X-974 contient le ZPM!)${NC}"
echo ""

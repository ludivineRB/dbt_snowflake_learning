#!/bin/bash
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m'

echo "=== Verification Mission 4 ==="

if [ ! -f "stats_energie.txt" ]; then
    echo -e "${RED}ERREUR: fichier stats_energie.txt introuvable${NC}"
    exit 1
fi

ERRORS=0

LINES=$(wc -l < stats_energie.txt | tr -d ' ')
if [ "$LINES" -eq 3 ]; then
    echo -e "${GREEN}[OK] 3 lignes (TOP 3)${NC}"
else
    echo -e "${RED}[FAIL] Nombre de lignes incorrect ($LINES, attendu: 3)${NC}"
    ERRORS=$((ERRORS+1))
fi

if head -1 stats_energie.txt | grep -q "Bouclier"; then
    echo -e "${GREEN}[OK] Bouclier est le plus gros consommateur${NC}"
else
    echo -e "${RED}[FAIL] Bouclier devrait etre en premiere position${NC}"
    ERRORS=$((ERRORS+1))
fi

if grep -q "Vie" stats_energie.txt; then
    echo -e "${GREEN}[OK] Systemes de Vie inclus dans le TOP 3${NC}"
else
    echo -e "${RED}[FAIL] Systemes de Vie manquant${NC}"
    ERRORS=$((ERRORS+1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}=== MISSION 4 REUSSIE! ===${NC}"
    echo "McKay: 'Hmm, le bouclier consomme trop. Je vais optimiser ca.'"
    echo "Passez a mission_5_pipeline/"
else
    echo -e "${RED}=== $ERRORS erreur(s) ===${NC}"
fi

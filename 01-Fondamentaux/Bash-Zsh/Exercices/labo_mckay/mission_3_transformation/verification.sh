#!/bin/bash
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m'

echo "=== Verification Mission 3 ==="

if [ ! -f "rapports_corriges.txt" ]; then
    echo -e "${RED}ERREUR: fichier rapports_corriges.txt introuvable${NC}"
    exit 1
fi

ERRORS=0

# Check date format is DD/MM/YYYY (first data line should have 15/03/2024)
if grep -q "15/03/2024" rapports_corriges.txt; then
    echo -e "${GREEN}[OK] Dates converties au format EU (15/03/2024)${NC}"
else
    echo -e "${RED}[FAIL] Dates non converties (cherche 15/03/2024)${NC}"
    ERRORS=$((ERRORS+1))
fi

# Check STATUS replaced
if grep -q "\[VALIDE\]" rapports_corriges.txt; then
    echo -e "${GREEN}[OK] STATUS:OK remplace par [VALIDE]${NC}"
else
    echo -e "${RED}[FAIL] STATUS:OK non remplace${NC}"
    ERRORS=$((ERRORS+1))
fi

if grep -q "\[ECHEC\]" rapports_corriges.txt; then
    echo -e "${GREEN}[OK] STATUS:KO remplace par [ECHEC]${NC}"
else
    echo -e "${RED}[FAIL] STATUS:KO non remplace${NC}"
    ERRORS=$((ERRORS+1))
fi

# No old format remaining
if grep -q "STATUS:OK\|STATUS:KO" rapports_corriges.txt; then
    echo -e "${RED}[FAIL] Il reste des STATUS:OK ou STATUS:KO${NC}"
    ERRORS=$((ERRORS+1))
else
    echo -e "${GREEN}[OK] Aucun ancien format STATUS restant${NC}"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}=== MISSION 3 REUSSIE! ===${NC}"
    echo "McKay: 'Les regex, c'est de la magie. MA magie.'"
    echo "Passez a mission_4_agregation/"
else
    echo -e "${RED}=== $ERRORS erreur(s) ===${NC}"
fi

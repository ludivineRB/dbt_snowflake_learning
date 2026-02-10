#!/bin/bash
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m'

echo "=== Verification Mission 2 ==="

if [ ! -f "items_critiques.csv" ]; then
    echo -e "${RED}ERREUR: fichier items_critiques.csv introuvable${NC}"
    exit 1
fi

ERRORS=0

# Check it has a header
if head -1 items_critiques.csv | grep -q "Nom,Categorie"; then
    echo -e "${GREEN}[OK] Header present${NC}"
else
    echo -e "${RED}[FAIL] Header manquant ou incorrect${NC}"
    ERRORS=$((ERRORS+1))
fi

# Check correct number of items (items with quantity < 10)
# ZPM(0), Generateur_Naquadah(3), Detecteur_Vie(8), Jumper(6), Barre(2),
# Combinaison(4), Emetteur(1), Tablette(7), Serum(3), Balise(9), Alimentation(5) = 11 items
DATA_LINES=$(($(wc -l < items_critiques.csv | tr -d ' ') - 1))
if [ "$DATA_LINES" -eq 11 ]; then
    echo -e "${GREEN}[OK] Nombre d'items critiques correct ($DATA_LINES)${NC}"
else
    echo -e "${RED}[FAIL] Nombre d'items incorrect ($DATA_LINES, attendu: 11)${NC}"
    ERRORS=$((ERRORS+1))
fi

# Check ZPM is included
if grep -q "ZPM_Reserve" items_critiques.csv; then
    echo -e "${GREEN}[OK] ZPM_Reserve inclus (quantite: 0)${NC}"
else
    echo -e "${RED}[FAIL] ZPM_Reserve manquant${NC}"
    ERRORS=$((ERRORS+1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}=== MISSION 2 REUSSIE! ===${NC}"
    echo "McKay: 'Bon, vous commencez a comprendre. Impressionnant.'"
    echo "Passez a mission_3_transformation/"
else
    echo -e "${RED}=== $ERRORS erreur(s) ===${NC}"
fi

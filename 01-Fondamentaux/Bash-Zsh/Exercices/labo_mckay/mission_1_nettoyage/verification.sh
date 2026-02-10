#!/bin/bash
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m'

echo "=== Verification Mission 1 ==="

if [ ! -f "capteurs_propres.csv" ]; then
    echo -e "${RED}ERREUR: fichier capteurs_propres.csv introuvable${NC}"
    echo "Creez-le en suivant les instructions."
    exit 1
fi

ERRORS=0

# Check no semicolons
if grep -q ";" capteurs_propres.csv; then
    echo -e "${RED}[FAIL] Il reste des points-virgules${NC}"
    ERRORS=$((ERRORS+1))
else
    echo -e "${GREEN}[OK] Points-virgules remplaces par des virgules${NC}"
fi

# Check no ERREUR lines
if grep -q "ERREUR" capteurs_propres.csv; then
    echo -e "${RED}[FAIL] Il reste des lignes ERREUR${NC}"
    ERRORS=$((ERRORS+1))
else
    echo -e "${GREEN}[OK] Lignes ERREUR supprimees${NC}"
fi

# Check no F (should be C)
if grep -qE "[0-9]F" capteurs_propres.csv; then
    echo -e "${RED}[FAIL] Il reste des temperatures en F${NC}"
    ERRORS=$((ERRORS+1))
else
    echo -e "${GREEN}[OK] Temperatures converties en C${NC}"
fi

# Check line count (header + 16 data lines = 17)
LINES=$(wc -l < capteurs_propres.csv | tr -d ' ')
if [ "$LINES" -eq 17 ]; then
    echo -e "${GREEN}[OK] Nombre de lignes correct ($LINES)${NC}"
else
    echo -e "${RED}[FAIL] Nombre de lignes incorrect ($LINES, attendu: 17)${NC}"
    ERRORS=$((ERRORS+1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}=== MISSION 1 REUSSIE! ===${NC}"
    echo "McKay: 'Pas mal. Pour un debutant.'"
    echo "Passez a mission_2_extraction/"
else
    echo -e "${RED}=== $ERRORS erreur(s) detectee(s) ===${NC}"
    echo "Relisez les instructions et reessayez."
fi

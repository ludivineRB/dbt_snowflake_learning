#!/bin/bash
GREEN='\033[1;32m'
RED='\033[1;31m'
CYAN='\033[1;36m'
NC='\033[0m'

echo "=== Verification Mission 5 - FINALE ==="

if [ ! -f "rapport_final.csv" ]; then
    echo -e "${RED}ERREUR: fichier rapport_final.csv introuvable${NC}"
    exit 1
fi

ERRORS=0

# Check header
if head -1 rapport_final.csv | grep -q "Date,Zone,Valeur"; then
    echo -e "${GREEN}[OK] Header correct${NC}"
else
    echo -e "${RED}[FAIL] Header incorrect (attendu: Date,Zone,Valeur)${NC}"
    ERRORS=$((ERRORS+1))
fi

# Check no OFFLINE
if grep -q "OFFLINE" rapport_final.csv; then
    echo -e "${RED}[FAIL] Lignes OFFLINE presentes${NC}"
    ERRORS=$((ERRORS+1))
else
    echo -e "${GREEN}[OK] Lignes OFFLINE supprimees${NC}"
fi

# Check date format (should be DD/MM not MM/DD)
if grep -q "01/03/2024" rapport_final.csv; then
    echo -e "${GREEN}[OK] Dates au format EU (01/03/2024)${NC}"
else
    echo -e "${RED}[FAIL] Dates non converties${NC}"
    ERRORS=$((ERRORS+1))
fi

# Check no tabs
if grep -qP '\t' rapport_final.csv 2>/dev/null || grep -q '	' rapport_final.csv; then
    echo -e "${RED}[FAIL] Tabs encore presentes${NC}"
    ERRORS=$((ERRORS+1))
else
    echo -e "${GREEN}[OK] Tabs remplaces par des virgules${NC}"
fi

# Check exactly 3 columns (Date,Zone,Valeur)
COLS=$(head -1 rapport_final.csv | awk -F',' '{print NF}')
if [ "$COLS" -eq 3 ]; then
    echo -e "${GREEN}[OK] 3 colonnes exactement${NC}"
else
    echo -e "${RED}[FAIL] Nombre de colonnes: $COLS (attendu: 3)${NC}"
    ERRORS=$((ERRORS+1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=============================================${NC}"
    echo -e "${GREEN}  TOUTES LES MISSIONS ACCOMPLIES!${NC}"
    echo -e "${GREEN}=============================================${NC}"
    echo ""
    echo -e "${CYAN}  Dr. McKay: 'OK... je suis... impressionne.${NC}"
    echo -e "${CYAN}  Et croyez-moi, ca n'arrive pas souvent.${NC}"
    echo ""
    echo -e "${CYAN}  Vous maitrisez maintenant:${NC}"
    echo "    - sed (remplacement, suppression)"
    echo "    - awk (extraction, aggregation)"
    echo "    - cut (selection de colonnes)"
    echo "    - tr (transformation de caracteres)"
    echo "    - sort, uniq, wc (statistiques)"
    echo "    - Pipes complexes (enchainer les commandes)"
    echo ""
    echo -e "${CYAN}  Ces competences sont essentielles pour${NC}"
    echo -e "${CYAN}  un Data Engineer. Bienvenue dans l'equipe.'${NC}"
    echo ""
    echo -e "${GREEN}=============================================${NC}"
else
    echo -e "${RED}=== $ERRORS erreur(s) ===${NC}"
    echo "Relisez les instructions et reessayez."
fi

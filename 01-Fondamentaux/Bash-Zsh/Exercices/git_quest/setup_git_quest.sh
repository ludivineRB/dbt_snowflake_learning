#!/bin/bash
# =============================================
#   GIT QUEST - Script d'initialisation
#   Cree un depot Git avec un historique complexe
# =============================================

GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo -e "${CYAN}=== GIT QUEST - Initialisation ===${NC}"
echo ""

# Nettoyage si le depot existe deja
if [ -d "$SCRIPT_DIR/depot_ancien" ]; then
    echo -e "${YELLOW}Le depot existe deja. Suppression...${NC}"
    rm -rf "$SCRIPT_DIR/depot_ancien"
fi

mkdir "$SCRIPT_DIR/depot_ancien"
cd "$SCRIPT_DIR/depot_ancien"
git init

# Configuration locale pour le jeu
git config user.name "Dr. Daniel Jackson"
git config user.email "daniel.jackson@sgc.mil"

echo "Initialisation du depot..."
sleep 0.5

# === COMMIT 1: Fichier initial ===
cat > coordonnees.txt << 'EOF'
=== COORDONNEES ANCIENNES ===
Fichier de recherche du Dr. Jackson

Planete cible: [DONNEES CORROMPUES]
Coordonnees: ???

Note: Les coordonnees sont fragmentees
dans l'historique de ce depot.
EOF

cat > journal_jackson.txt << 'EOF'
Journal de Daniel Jackson - Jour 1
"J'ai commence a cataloguer les coordonnees
trouvees dans les ruines de P3X-888."
EOF

git add coordonnees.txt journal_jackson.txt
git commit -m "Initial: debut des recherches du Dr. Jackson"

# === COMMIT 2 ===
cat >> journal_jackson.txt << 'EOF'

Journal de Daniel Jackson - Jour 5
"Premier fragment trouve! Le premier glyphe
correspond au symbole de la constellation du Serpent."
Premier fragment: ALPHA-7
EOF

git add journal_jackson.txt
git commit -m "Jour 5: premier fragment decouvert (ALPHA-7)"

# === COMMIT 3 (contient un indice important) ===
cat >> journal_jackson.txt << 'EOF'

Journal de Daniel Jackson - Jour 12
"IMPORTANT: J'ai decouvert que les coordonnees
sont composees de 4 fragments. J'en ai 1 sur 4.
Les Goa'uld ont tente de corrompre mes fichiers.
Je dois sauvegarder chaque fragment sur une branche
differente pour les proteger."

INDICE: Les fragments sont caches dans les branches.
Utilisez 'git branch -a' pour les trouver.
EOF

git add journal_jackson.txt
git commit -m "Jour 12: IMPORTANT - decouverte du systeme de fragments"

# === COMMIT 4 ===
cat > artefacts.txt << 'EOF'
=== INVENTAIRE DES ARTEFACTS ===
1. Tablette de pierre (P3X-888) - Fragment ALPHA-7
2. Cristal de donnees (P4X-639) - En cours d'analyse
3. Statuette ancienne (P3R-272) - Contient des glyphes
4. Parchemin ancien (Abydos) - Coordonnee partielle
EOF

git add artefacts.txt
git commit -m "Ajout inventaire des artefacts"

# === COMMIT 5 ===
cat >> journal_jackson.txt << 'EOF'

Journal de Daniel Jackson - Jour 20
"Teal'c m'a aide a traduire le deuxieme fragment.
Les Goa'uld approchent. Je cache les fragments."
EOF

git add journal_jackson.txt
git commit -m "Jour 20: Teal'c aide a la traduction"

# === COMMIT 6 ===
cat > equipe_recherche.txt << 'EOF'
=== EQUIPE DE RECHERCHE ===
- Dr. Daniel Jackson (responsable)
- Teal'c (traduction Goa'uld)
- Dr. Robert Rothman (assistance)
- Nyan (stagiaire Bedrosien)
EOF

git add equipe_recherche.txt
git commit -m "Documentation de l'equipe de recherche"

# === COMMIT 7 ===
cat >> journal_jackson.txt << 'EOF'

Journal de Daniel Jackson - Jour 30
"Trois fragments sur quatre sont securises dans
des branches separees. Le dernier est presque decode."
Fragments trouves: ALPHA-7, BETA-3, GAMMA-9
Fragment manquant: DELTA-?
EOF

git add journal_jackson.txt
git commit -m "Jour 30: trois fragments sur quatre securises"

# === COMMIT 8 (dernier sur main) ===
cat > coordonnees.txt << 'EOF'
=== COORDONNEES ANCIENNES ===
Fichier de recherche du Dr. Jackson

Planete cible: DESIGNATION INCONNUE
Fragment 1: ALPHA-7 (verifie)
Fragment 2: [voir branche 'traduction_tealc']
Fragment 3: [voir branche 'analyse_carter']
Fragment 4: [voir branche 'fragments_anciens']

Pour reconstituer les coordonnees completes,
explorez chaque branche et fusionnez les donnees.
EOF

git add coordonnees.txt
git commit -m "Jour 35: mise a jour du fichier de coordonnees"

# === BRANCHE 1: traduction_tealc ===
git checkout -b traduction_tealc HEAD~3

cat > fragment_tealc.txt << 'EOF'
=== TRADUCTION DE TEAL'C ===
"En effet. Le deuxieme fragment est: BETA-3.
Ce symbole represente la constellation du Bouvier
dans la cartographie Goa'uld."
EOF

cat > coordonnees.txt << 'EOF'
=== COORDONNEES ANCIENNES ===
Fragment 2: BETA-3
Traduit par Teal'c depuis les archives Goa'uld.
EOF

git add fragment_tealc.txt coordonnees.txt
git commit -m "Teal'c: traduction du fragment BETA-3"

# === BRANCHE 2: analyse_carter ===
git checkout -b analyse_carter main~4

cat > fragment_carter.txt << 'EOF'
=== ANALYSE DU DR. CARTER ===
"Le troisieme fragment decode par analyse spectrale:
GAMMA-9. Correspond a un point d'origine stellaire."
EOF

cat > coordonnees.txt << 'EOF'
=== COORDONNEES ANCIENNES ===
Fragment 3: GAMMA-9
Decode par le Dr. Carter via analyse spectrale.
EOF

git add fragment_carter.txt coordonnees.txt
git commit -m "Carter: analyse spectrale du fragment GAMMA-9"

# === BRANCHE 3: fragments_anciens (avec conflit de merge) ===
git checkout -b fragments_anciens main~2

cat > fragment_final.txt << 'EOF'
=== FRAGMENT FINAL ===
"Le dernier fragment est: DELTA-1.
Les coordonnees completes de l'arme Ancienne sont:
ALPHA-7 / BETA-3 / GAMMA-9 / DELTA-1"
EOF

cat > coordonnees.txt << 'EOF'
=== COORDONNEES ANCIENNES ===
Planete cible: P9G-844

COORDONNEES COMPLETES:
  Fragment 1: ALPHA-7
  Fragment 2: BETA-3
  Fragment 3: GAMMA-9
  Fragment 4: DELTA-1

Designation: ARME DES ANCIENS - DAKARA
"With great power comes great responsibility"
EOF

git add fragment_final.txt coordonnees.txt
git commit -m "Fragment final: DELTA-1 - coordonnees completes!"

# Retour sur main
git checkout main

# === Creer le script de verification ===
cat > verification.sh << 'VERIF_EOF'
#!/bin/bash
GREEN='\033[1;32m'
RED='\033[1;31m'
CYAN='\033[1;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}=== VERIFICATION DES COORDONNEES ===${NC}"
echo ""

# Verifier qu'on est sur main
BRANCH=$(git branch --show-current 2>/dev/null)
if [[ "$BRANCH" != "main" ]]; then
    echo -e "${RED}Vous n'etes pas sur la branche 'main'.${NC}"
    echo "Faites: git checkout main"
    exit 1
fi

# Verifier que le merge a eu lieu
if grep -q "DELTA-1" coordonnees.txt 2>/dev/null; then
    echo -e "${GREEN}Fragment DELTA-1 trouve!${NC}"
else
    echo -e "${RED}Fragment DELTA-1 manquant.${NC}"
    echo "Fusionnez la branche 'fragments_anciens' dans main."
    exit 1
fi

if grep -q "ALPHA-7" coordonnees.txt 2>/dev/null; then
    echo -e "${GREEN}Fragment ALPHA-7 trouve!${NC}"
else
    echo -e "${RED}Fragment ALPHA-7 manquant dans les coordonnees.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}  COORDONNEES RECONSTITUEES AVEC SUCCES!${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""
echo -e "${CYAN}  Planete: P9G-844${NC}"
echo -e "${CYAN}  ALPHA-7 / BETA-3 / GAMMA-9 / DELTA-1${NC}"
echo ""
echo "  Felicitations! Vous maitrisez Git:"
echo "  - git log (explorer l'historique)"
echo "  - git show (lire un commit)"
echo "  - git diff (comparer des versions)"
echo "  - git branch (lister les branches)"
echo "  - git checkout (naviguer)"
echo "  - git merge (fusionner)"
echo "  - Resolution de conflits"
echo ""
echo -e "${GREEN}  Le Dr. Jackson est fier de vous!${NC}"
echo -e "${GREEN}=============================================${NC}"
VERIF_EOF

git add verification.sh
git commit -m "Ajout du script de verification"

cd "$SCRIPT_DIR"

echo ""
echo -e "${GREEN}=== GIT QUEST initialise avec succes! ===${NC}"
echo ""
echo -e "Le depot ${CYAN}depot_ancien/${NC} a ete cree avec:"
echo "  - 9 commits sur la branche main"
echo "  - 3 branches supplementaires a explorer"
echo "  - 1 conflit de merge a resoudre"
echo ""
echo -e "Pour commencer: ${YELLOW}cd depot_ancien${NC}"
echo -e "Puis lisez les missions dans ${YELLOW}README.txt${NC}"
echo ""

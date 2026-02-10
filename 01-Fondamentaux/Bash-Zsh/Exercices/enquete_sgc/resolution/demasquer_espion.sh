#!/bin/bash
# =============================================================================
#  STARGATE COMMAND - SYSTEME D'IDENTIFICATION DU TRAITRE
# =============================================================================

# Couleurs
ROUGE='\033[0;31m'
VERT='\033[0;32m'
JAUNE='\033[1;33m'
BLEU='\033[0;34m'
CYAN='\033[0;36m'
BLANC='\033[1;37m'
GRAS='\033[1m'
RESET='\033[0m'

# Fonction pour afficher du texte lettre par lettre
taper() {
    local texte="$1"
    local delai="${2:-0.03}"
    for (( i=0; i<${#texte}; i++ )); do
        printf "%s" "${texte:$i:1}"
        sleep "$delai"
    done
    echo ""
}

# Fonction pour une pause dramatique
pause_dramatique() {
    local duree="${1:-1}"
    sleep "$duree"
}

# Effacer l'ecran
clear

echo -e "${BLEU}"
echo "================================================================================"
echo "         STARGATE COMMAND - SYSTEME DE SECURITE NIVEAU OMEGA"
echo "================================================================================"
echo -e "${RESET}"
echo ""

pause_dramatique 1

echo -e "${JAUNE}[SYSTEME]${RESET} Connexion au systeme de securite du SGC..."
pause_dramatique 1
echo -e "${JAUNE}[SYSTEME]${RESET} Authentification en cours..."
pause_dramatique 1
echo -e "${VERT}[SYSTEME]${RESET} Acces autorise."
echo ""
pause_dramatique 0.5

echo -e "${BLANC}${GRAS}============================================${RESET}"
echo -e "${BLANC}${GRAS}   IDENTIFICATION DE L'AGENT INFILTRE${RESET}"
echo -e "${BLANC}${GRAS}============================================${RESET}"
echo ""

echo -e "${CYAN}D'apres votre enquete, qui est l'espion du NID infiltre au SGC?${RESET}"
echo ""
echo -ne "${JAUNE}> Entrez le nom du traitre: ${RESET}"
read -r reponse

# Convertir en majuscules pour la comparaison
reponse_maj=$(echo "$reponse" | tr '[:lower:]' '[:upper:]')

echo ""
pause_dramatique 1

echo -e "${JAUNE}[SYSTEME]${RESET} Verification dans la base de donnees..."
pause_dramatique 1
echo -e "${JAUNE}[SYSTEME]${RESET} Croisement avec les preuves collectees..."
pause_dramatique 1
echo -e "${JAUNE}[SYSTEME]${RESET} Analyse en cours..."
pause_dramatique 2

echo ""

if [[ "$reponse_maj" == "MAKEPEACE" || "$reponse_maj" == "COLONEL MAKEPEACE" || "$reponse_maj" == "ROBERT MAKEPEACE" ]]; then
    # ==================== BONNE REPONSE ====================
    echo -e "${VERT}"
    echo "    ****************************************************"
    echo "    *                                                  *"
    echo "    *          IDENTIFICATION CONFIRMEE !              *"
    echo "    *                                                  *"
    echo "    ****************************************************"
    echo -e "${RESET}"
    pause_dramatique 1

    echo -e "${ROUGE}${GRAS}"
    taper "   TRAITRE IDENTIFIE: Colonel Robert MAKEPEACE" 0.05
    taper "   Equipe: SG-3" 0.05
    taper "   Badge: SGC-0042" 0.05
    taper "   Affiliation secrete: NID" 0.05
    echo -e "${RESET}"
    pause_dramatique 1

    echo -e "${BLANC}${GRAS}"
    echo "  ============================================================"
    echo "                    PREUVES RETENUES"
    echo "  ============================================================"
    echo -e "${RESET}"

    echo -e "  ${CYAN}[1]${RESET} 12 acces nocturnes a la salle de la Porte"
    echo -e "      -> Plus que tout autre membre du personnel"
    echo ""
    echo -e "  ${CYAN}[2]${RESET} 5 connexions a des serveurs externes chiffres"
    echo -e "      -> Depuis le TERMINAL-42, toujours la nuit"
    echo ""
    echo -e "  ${CYAN}[3]${RESET} Badge SGC-0042 falsifie"
    echo -e "      -> Habilitation modifiee de GAMMA vers OMEGA"
    echo -e "      -> Restrictions d'acces supprimees"
    echo ""
    echo -e "  ${CYAN}[4]${RESET} 5 acces au laboratoire (anormal pour un Marine)"
    echo -e "      -> Dont 4 de nuit"
    echo ""
    echo -e "  ${CYAN}[5]${RESET} Communication NID interceptee"
    echo -e "      -> Reference a \"notre agent au sein de SG-3\""
    echo -e "      -> Nom de code: FAUCON"
    echo ""

    pause_dramatique 1

    echo -e "${VERT}${GRAS}"
    echo "  ============================================================"
    echo "                    MISSION ACCOMPLIE !"
    echo "  ============================================================"
    echo -e "${RESET}"
    echo ""
    taper "  Le Colonel Makepeace a ete arrete et place en detention." 0.03
    taper "  Il travaillait pour le NID, une organisation secrete qui" 0.03
    taper "  cherche a s'emparer de technologies extraterrestres par" 0.03
    taper "  tous les moyens, y compris le vol et la trahison." 0.03
    echo ""
    taper "  Dans la serie Stargate SG-1, le Colonel Makepeace est" 0.03
    taper "  effectivement demasque comme agent du NID dans l'episode" 0.03
    taper "  \"Shades of Grey\" (Saison 3, Episode 18)." 0.03
    echo ""

    echo -e "${JAUNE}${GRAS}"
    echo "  ============================================================"
    echo "               COMMANDES APPRISES AUJOURD'HUI"
    echo "  ============================================================"
    echo -e "${RESET}"
    echo ""
    echo -e "  ${VERT}grep${RESET}    - Rechercher des motifs dans des fichiers"
    echo -e "  ${VERT}awk${RESET}     - Extraire et manipuler des colonnes de donnees"
    echo -e "  ${VERT}sort${RESET}    - Trier des donnees"
    echo -e "  ${VERT}uniq${RESET}    - Eliminer les doublons (avec -c pour compter)"
    echo -e "  ${VERT}diff${RESET}    - Comparer deux fichiers"
    echo -e "  ${VERT}wc${RESET}      - Compter les lignes, mots, caracteres"
    echo -e "  ${VERT}ls -a${RESET}   - Afficher les fichiers caches"
    echo ""

    echo -e "${BLEU}"
    echo "================================================================================"
    echo "    Felicitations, enqueteur ! Le General Hammond vous remercie."
    echo "    Le SGC est a nouveau en securite grace a vos talents d'analyse."
    echo "================================================================================"
    echo -e "${RESET}"

else
    # ==================== MAUVAISE REPONSE ====================
    echo -e "${ROUGE}"
    echo "    ****************************************************"
    echo "    *                                                  *"
    echo "    *         IDENTIFICATION NON CONFIRMEE             *"
    echo "    *                                                  *"
    echo "    ****************************************************"
    echo -e "${RESET}"
    echo ""

    echo -e "${JAUNE}[SYSTEME]${RESET} \"$reponse\" ne correspond pas aux preuves collectees."
    echo ""
    pause_dramatique 1

    echo -e "${BLANC}Indices pour reprendre l'enquete:${RESET}"
    echo ""
    echo "  1. Retournez a l'etape 1 et comptez les acces NUIT:"
    echo "     grep \"NUIT\" logs_securite/acces_porte.log | awk -F'|' '{print \$2}' | sort | uniq -c | sort -rn"
    echo ""
    echo "  2. Verifiez les connexions suspectes:"
    echo "     grep \"EXTERNE_CHIFFRE\" logs_securite/connexions_reseau.log"
    echo ""
    echo "  3. N'oubliez pas de comparer les badges:"
    echo "     diff preuves/badge_original.txt preuves/badge_suspect.txt"
    echo ""
    echo "  4. Et cherchez les fichiers caches:"
    echo "     ls -la preuves/"
    echo ""
    echo -e "${CYAN}Reessayez quand vous aurez reuni toutes les preuves!${RESET}"
    echo -e "${CYAN}  bash resolution/demasquer_espion.sh${RESET}"
    echo ""
fi

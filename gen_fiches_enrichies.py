#!/usr/bin/env python3
"""Enrichit les fiches de cours — ajoute des items aux sections trop légères."""
import json

# Clé : (subject_id, title partiel) → items à ajouter
EXTRA = {

  # ═══════════════════════════════════════════
  # MATHÉMATIQUES
  # ═══════════════════════════════════════════
  ("maths", "Second degré"): [
    {"label": "Discriminant Δ",
     "text": "Δ = b² − 4ac\n• Δ > 0 : deux racines réelles x₁=(−b−√Δ)/2a et x₂=(−b+√Δ)/2a\n• Δ = 0 : une racine double x₀ = −b/2a\n• Δ < 0 : pas de racine réelle (deux racines complexes conjuguées en Terminale)"},
    {"label": "Forme canonique & sommet",
     "text": "ax²+bx+c = a(x − α)² + β  où  α = −b/2a  et  β = −Δ/4a\nSommet de la parabole : S(α ; β)\n→ minimum si a > 0, maximum si a < 0"},
    {"label": "Factorisation & formules de Viète",
     "text": "Si Δ ≥ 0 : ax²+bx+c = a(x−x₁)(x−x₂)\nFormules de Viète : x₁+x₂ = −b/a  et  x₁·x₂ = c/a\nUtile pour vérifier des racines ou construire un polynôme connaissant ses racines."},
    {"label": "Signe du trinôme",
     "text": "Si a > 0 :\n  • x ∈ ]x₁ ; x₂[ → ax²+bx+c < 0\n  • x ∉ [x₁ ; x₂]  → ax²+bx+c > 0\nSi Δ < 0 : même signe que a pour tout x\nMéthode : tableau de signes avec les racines comme bornes"},
    {"label": "Équations se ramenant au 2nd degré",
     "text": "Changement de variable : X = xⁿ ou X = eˣ...\nEx. : x⁴−5x²+4=0 → poser X=x² → X²−5X+4=0\nÉq. du type |f(x)|=k : résoudre f(x)=k ET f(x)=−k séparément."},
  ],

  ("maths", "Dérivation"): [
    {"label": "Tableau des dérivées usuelles",
     "text": "f(x)         | f′(x)\n-------------|----------\nxⁿ           | nxⁿ⁻¹\n√x           | 1/(2√x)\n1/x          | −1/x²\neˣ           | eˣ\nln x         | 1/x\nsin x        | cos x\ncos x        | −sin x"},
    {"label": "Règles de calcul",
     "text": "(u+v)′ = u′+v′\n(ku)′ = ku′\n(uv)′ = u′v + uv′\n(u/v)′ = (u′v − uv′)/v²\n(f∘g)′(x) = g′(x)·f′(g(x))  ← composition\nEx. : (e^(2x+1))′ = 2·e^(2x+1)"},
    {"label": "Dérivée et variations",
     "text": "f′(x) > 0 sur I → f croissante sur I\nf′(x) < 0 sur I → f décroissante sur I\nf′(x₀) = 0 + changement de signe → extremum local\nTableau de variations : dresser le signe de f′, puis flèches ↗↘"},
    {"label": "Tangente & application",
     "text": "Équation de la tangente en x=a :\ny = f(a) + f′(a)·(x − a)\nPente = f′(a)\nPour trouver une tangente parallèle à y = mx+b : résoudre f′(x) = m"},
  ],

  ("maths", "Fonctions exponentielle et logarithme"): [
    {"label": "Propriétés algébriques de ln",
     "text": "ln(ab) = ln a + ln b\nln(a/b) = ln a − ln b\nln(aⁿ) = n·ln a\nln(√a) = ½·ln a\nln(1) = 0  |  ln(e) = 1  |  ln(e²) = 2\nDomaine : x > 0 obligatoire"},
    {"label": "Propriétés de l'exponentielle",
     "text": "eᵃ⁺ᵇ = eᵃ·eᵇ    eᵃ⁻ᵇ = eᵃ/eᵇ    (eᵃ)ᵇ = eᵃᵇ\ne⁰ = 1   e¹ = e ≈ 2,718\n(eˣ)′ = eˣ    (eᵘ)′ = u′eᵘ\nDomaine : ℝ entier (définie partout)"},
    {"label": "Limites et croissances comparées",
     "text": "lim(x→+∞) eˣ = +∞   lim(x→−∞) eˣ = 0\nlim(x→0⁺) ln x = −∞   lim(x→+∞) ln x = +∞\nCroissances comparées :\n  eˣ/xⁿ → +∞  (exp domine polynôme)\n  xⁿ·ln x → 0  quand x→0⁺\n  ln x / xⁿ → 0  quand x→+∞"},
    {"label": "Résoudre eˣ = k et ln x = k",
     "text": "eˣ = k (k > 0)  ↔  x = ln k\nln x = k  ↔  x = eᵏ  (et x > 0)\neˣ > k  ↔  x > ln k\nln x > k  ↔  x > eᵏ\nAstuce : toujours vérifier le domaine avant de résoudre"},
    {"label": "Étude de f(x) = eˣ·P(x) ou ln(g(x))",
     "text": "Pour f = eˣP(x) : f′ = eˣ(P+P′), signe = signe de P+P′\nPour f = ln(g) : f′ = g′/g, domaine : g > 0\nLimites : règle de L'Hôpital ou croissances comparées\nEx. f(x) = x·eˣ : f′ = eˣ(x+1), min en x=−1 : f(−1)=−1/e"},
  ],

  ("maths", "Suites numériques"): [
    {"label": "Suites arithmétiques — formules clés",
     "text": "Raison r : uₙ = u₀ + n·r\nSomme : S = (n+1)·(u₀+uₙ)/2 = (nb de termes)×(premier+dernier)/2\nEx. 1+2+…+n = n(n+1)/2\nVariations : r > 0 → croissante | r < 0 → décroissante | r = 0 → constante"},
    {"label": "Suites géométriques — formules clés",
     "text": "Raison q : uₙ = u₀·qⁿ\nSomme (q ≠ 1) : S = u₀·(1−qⁿ⁺¹)/(1−q)\nSi |q| < 1 : suite converge vers 0\nEx. 1+2+4+…+2ⁿ = 2ⁿ⁺¹−1  (q=2, u₀=1)"},
    {"label": "Convergence et limites",
     "text": "Suite croissante + majorée → converge\nSuite décroissante + minorée → converge\nSuite géométrique : |q|<1 → lim=0 | q=1 → lim=u₀ | |q|>1 → ±∞\nSi uₙ₊₁=f(uₙ) converge vers ℓ, alors ℓ = f(ℓ) (point fixe)"},
    {"label": "Raisonnement par récurrence",
     "text": "① Initialisation : vérifier pour n=0 (ou n=1)\n② Hérédité : supposer P(n) vraie → montrer P(n+1)\n③ Conclusion : vraie pour tout n ≥ n₀\n⚠ Utiliser explicitement l'hypothèse de récurrence dans l'étape ②"},
  ],

  ("maths", "Trigonométrie"): [
    {"label": "Valeurs exactes — tableau",
     "text": "θ    | 0  | π/6  | π/4  | π/3  | π/2\n-----|----|----- |------|------|-----\nsin  | 0  | 1/2  | √2/2 | √3/2 | 1\ncos  | 1  | √3/2 | √2/2 | 1/2  | 0\ntan  | 0  | 1/√3 | 1    | √3   | —\nMémo sin : 0, ½, √2/2, √3/2, 1 (croissant sur [0;π/2])"},
    {"label": "Identités fondamentales",
     "text": "sin²x + cos²x = 1  (Pythagore)\ntan x = sin x / cos x\n1 + tan²x = 1/cos²x\nFormules double angle :\n  cos(2x) = cos²x−sin²x = 1−2sin²x = 2cos²x−1\n  sin(2x) = 2 sin x cos x"},
    {"label": "Formules d'addition",
     "text": "cos(a+b) = cos a cos b − sin a sin b\ncos(a−b) = cos a cos b + sin a sin b\nsin(a+b) = sin a cos b + cos a sin b\nsin(a−b) = sin a cos b − cos a sin b\nApplications : cos(π/12), sin(7π/12)..."},
    {"label": "Résoudre sin x = k ou cos x = k",
     "text": "cos x = k : x = ±arccos(k) + 2kπ, k∈ℤ\nsin x = k : x = arcsin(k)+2kπ  OU  x = π−arcsin(k)+2kπ\ntan x = k : x = arctan(k) + kπ\n→ Toujours trouver les solutions sur [0;2π] d'abord, puis généraliser"},
  ],

  ("maths", "Géométrie dans l'espace"): [
    {"label": "Formules de volumes",
     "text": "Cube (a) : V = a³\nPavé (l,L,h) : V = lLh\nCylindre (r,h) : V = πr²h\nCône (r,h) : V = πr²h/3\nSphère (r) : V = 4πr³/3\nPyramide : V = Aire base × h / 3\nAire sphère : S = 4πr²  |  Aire lat. cône : S = πrl"},
    {"label": "Produit scalaire en 3D",
     "text": "u⃗·v⃗ = xᵤxᵥ + yᵤyᵥ + zᵤzᵥ\n|u⃗| = √(x²+y²+z²)\ncos(u⃗,v⃗) = u⃗·v⃗ / (|u⃗|·|v⃗|)\nu⃗ ⊥ v⃗ ⟺ u⃗·v⃗ = 0\nProjection de u⃗ sur v⃗ : (u⃗·v⃗)/|v⃗|"},
    {"label": "Équation de plan",
     "text": "Plan de vecteur normal n⃗(a,b,c) passant par A(x₀,y₀,z₀) :\na(x−x₀) + b(y−y₀) + c(z−z₀) = 0\nForme générale : ax + by + cz + d = 0\nDistance de M(x₁,y₁,z₁) au plan : |ax₁+by₁+cz₁+d| / √(a²+b²+c²)"},
    {"label": "Droite en 3D (représentation paramétrique)",
     "text": "Droite passant par A(x₀,y₀,z₀), vect. dir. u⃗(a,b,c) :\n{ x = x₀+at\n{ y = y₀+bt\n{ z = z₀+ct  (t∈ℝ)\nIntersection 2 droites : égaliser les paramétrisations → système\nPoints alignés : AB⃗ = k·AC⃗"},
  ],

  ("maths", "Probabilités et statistiques"): [
    {"label": "Loi binomiale B(n,p)",
     "text": "X ~ B(n,p) : n épreuves indépendantes de Bernoulli, P(succès)=p\nP(X=k) = C(n,k)·pᵏ·(1−p)ⁿ⁻ᵏ\nE(X) = np    V(X) = np(1−p)    σ = √(np(1−p))\nEx. : 10 lancers de pièce, P(5 faces) = C(10,5)·(0,5)¹⁰ ≈ 0,246"},
    {"label": "Loi normale N(μ,σ²)",
     "text": "Courbe en cloche symétrique autour de μ\nP(μ−σ < X < μ+σ) ≈ 68 %\nP(μ−2σ < X < μ+2σ) ≈ 95 %\nP(μ−3σ < X < μ+3σ) ≈ 99,7 %\nCentrage-réduction : Z = (X−μ)/σ ~ N(0,1)\nUtiliser calculatrice ou table pour P(a<X<b)"},
    {"label": "Probabilités conditionnelles",
     "text": "P(A|B) = P(A∩B) / P(B)  (B ≠ ∅)\nFormule de Bayes : P(B|A) = P(A|B)·P(B) / P(A)\nForumle des prob. totales : P(A) = Σ P(A|Bᵢ)·P(Bᵢ)\n→ Utiliser un arbre de probabilités pour visualiser"},
    {"label": "Intervalle de confiance",
     "text": "Pour une proportion p, n observations, fréquence f :\nIC à 95 % : [ f − 1/√n ; f + 1/√n ]\nInterprétation : 95 % des IC construits ainsi contiennent le vrai p\nPlus n est grand, plus l'IC est précis (largeur ∝ 1/√n)"},
  ],

  ("maths", "Primitives et intégration"): [
    {"label": "Tableau des primitives usuelles",
     "text": "f(x)     | F(x) (primitive)\n---------|------------------\nxⁿ (n≠−1)| xⁿ⁺¹/(n+1)\n1/x      | ln|x|\neˣ       | eˣ\nsin x    | −cos x\ncos x    | sin x\neᵃˣ      | eᵃˣ/a\nsin(ax)  | −cos(ax)/a\ncos(ax)  | sin(ax)/a"},
    {"label": "Théorème fondamental de l'analyse",
     "text": "Si F est une primitive de f sur [a;b] :\n∫ₐᵇ f(x) dx = [F(x)]ₐᵇ = F(b) − F(a)\nConséquence : G(x) = ∫ₐˣ f(t) dt  est primitive de f, G′(x) = f(x)\nLinéarité : ∫(αf+βg) = α∫f + β∫g"},
    {"label": "Intégration par parties",
     "text": "∫u·v′ dx = [uv] − ∫u′·v dx\nChoisir u qui se simplifie en dérivant, v′ simple à intégrer\nCas courants :\n  ∫x·eˣ dx  → u=x, v′=eˣ\n  ∫x·ln x dx → u=ln x, v′=x\n  ∫x·cos x dx → u=x, v′=cos x"},
    {"label": "Aire et interprétation géométrique",
     "text": "∫ₐᵇ f(x) dx = aire algébrique (positive si f≥0, négative si f≤0)\nAire entre f et g sur [a;b] = ∫ₐᵇ |f(x)−g(x)| dx\nDécoupe aux points d'intersection (f=g) si les courbes se croisent\nUnités : si x en m et f en m → intégrale en m²"},
  ],

  # ═══════════════════════════════════════════
  # PHYSIQUE-CHIMIE
  # ═══════════════════════════════════════════
  ("physique", "Mécanique — Lois du mouvement"): [
    {"label": "2e loi de Newton — formule",
     "text": "Σ F⃗ = m·a⃗  (en N, kg, m/s²)\nProjections sur les axes :\n  Ox : ΣFₓ = m·aₓ\n  Oy : ΣFᵧ = m·aᵧ\nSi Σ F⃗ = 0⃗ → a⃗ = 0⃗ → MRU (1re loi de Newton)"},
    {"label": "Équations horaires des mouvements usuels",
     "text": "MRU : x(t) = x₀ + v·t  (a = 0)\nMRUA : { v(t) = v₀ + a·t\n         x(t) = x₀ + v₀t + ½at²\nChute libre (axe vers le bas) :\n  v(t) = gt  |  z(t) = ½gt²  (g ≈ 9,8 m/s²)"},
    {"label": "Tir parabolique",
     "text": "Décomposition indépendante :\n  Ox : aₓ=0  → x = v₀cosθ·t  (MRU)\n  Oy : aᵧ=−g → y = v₀sinθ·t − ½gt²  (MRUA)\nPortée maximale : θ = 45°\nTrajecture : parabole y = f(x)"},
    {"label": "Mouvement circulaire uniforme",
     "text": "Vitesse constante en valeur, direction change\nAccélération centripète : a = v²/R = ω²R (vers le centre)\nForce centripète : F = mv²/R\nPériode T = 2πR/v = 2π/ω\nFrequence f = 1/T  |  ω = 2πf"},
  ],

  ("physique", "Mécanique — Travail et énergie"): [
    {"label": "Travail d'une force",
     "text": "W = F·d·cosα  (α = angle entre F⃗ et déplacement)\nUnité : joule (J)\nW > 0 : force motrice\nW < 0 : force résistante\nW = 0 : force perpendiculaire au déplacement\nTravail du poids : W(P) = mg·Δh (>0 si descente)"},
    {"label": "Énergie cinétique & théorème travail-énergie",
     "text": "Ec = ½mv²  (en joules)\nThéorème travail-énergie : ΔEc = ΣW(toutes les forces)\nSi seule la pesanteur agit : ΔEc = −ΔEp\nConservation si pas de frottements : Ec + Ep = cste"},
    {"label": "Énergie potentielle & conservation",
     "text": "Ep (gravitationnelle) = mgh  (référence : h=0 au sol)\nÉnergie mécanique : Em = Ec + Ep\nSans frottements : Em = cste (conservation)\nAvec frottements : ΔEm = W(frottements) < 0\n→ énergie dissipée en chaleur = |W(frottements)|"},
    {"label": "Puissance",
     "text": "P = W/t  (puissance moyenne)  ou  P = F·v  (instantanée)\nUnité : watt (W = J/s)\nRendement η = P_utile / P_consommée  (0 < η ≤ 1)\n1 kWh = 3,6 MJ\n1 cheval-vapeur ≈ 736 W"},
    {"label": "Plan incliné — bilan des forces",
     "text": "Angle θ, longueur L, masse m :\nW(poids) = mgL·sinθ\nW(normale) = 0\nW(frottement) = −f·L  avec f = μ·mg·cosθ\nBilan : Ec_f = Ec_i + mgL·sinθ − μ·mg·cosθ·L"},
  ],

  ("physique", "Électricité — Lois et circuits"): [
    {"label": "Loi d'Ohm et résistances",
     "text": "U = R·I  (tension V, résistance Ω, intensité A)\nEn série : R_tot = R₁+R₂+…  (même intensité)\nEn parallèle : 1/R_tot = 1/R₁+1/R₂+…  (même tension)\n2 résistances parallèle : R_tot = R₁R₂/(R₁+R₂)\nPuissance dissipée : P = UI = RI² = U²/R"},
    {"label": "Lois de Kirchhoff",
     "text": "Nœuds (loi des courants) : ΣI_entrants = ΣI_sortants\nMailles (loi des tensions) : Σu = 0 sur toute maille fermée\n→ Permettent de résoudre tout circuit électrique\nConvention récepteur : U et I en sens opposés\nConvention générateur : U et I dans le même sens"},
    {"label": "Condensateur — régime transitoire RC",
     "text": "Charge : Uc(t) = E(1 − e^(−t/τ))  avec τ = RC\nDécharge : Uc(t) = U₀·e^(−t/τ)\nAprès 5τ : condensateur considéré chargé/déchargé\nq = C·U  (charge en coulombs)\nBloque le courant continu en régime permanent"},
    {"label": "Courant alternatif sinusoïdal",
     "text": "i(t) = Iₘₐₓ·sin(2πft + φ)\nValeur efficace : I_eff = Iₘₐₓ/√2\nRéseau France : 230 V / 50 Hz → Vₘₐₓ = 325 V, T = 20 ms\nPuissance : P = U_eff·I_eff·cos(φ)\ncos(φ) = facteur de puissance"},
  ],

  ("physique", "Ondes mécaniques et sonores"): [
    {"label": "Formules fondamentales",
     "text": "λ = v/f  (longueur d'onde = vitesse / fréquence)\nv_son ≈ 340 m/s dans l'air à 20°C\nv_son ≈ 1 480 m/s dans l'eau\nT = 1/f  (période)\nRetard τ = d/v  (d = distance, v = célérité)"},
    {"label": "Niveau sonore et décibels",
     "text": "L(dB) = 10·log(I/I₀)  avec I₀ = 10⁻¹² W/m²\nÉchelle : 0 dB (seuil audition) | 60 dB (conversation) | 120 dB (concert)\n+10 dB → intensité ×10  |  +3 dB → ×2\n> 85 dB prolongé → risque de surdité"},
    {"label": "Effet Doppler",
     "text": "Source se rapproche → fréquence apparente augmente (son aigu)\nSource s'éloigne → fréquence diminue (son grave)\nf′ = f·(v ± v_obs) / (v ∓ v_source)\nApplications : radar, échographie Doppler, exoplanètes"},
    {"label": "Ondes stationnaires",
     "text": "Superposition de 2 ondes identiques en sens opposés\nNœuds (immobiles) et ventres (amplitude max) fixes\nCondition : L = n·λ/2  (n entier)\nApplications : cordes (guitare), colonnes d'air (flûte, orgue)\nHarmoniques : f₁ (fondamental), 2f₁, 3f₁..."},
  ],

  ("physique", "Optique — Lumière et lentilles"): [
    {"label": "Loi de Snell-Descartes (réfraction)",
     "text": "n₁·sin(i₁) = n₂·sin(i₂)\nn = c/v  (indice, c = 3×10⁸ m/s)\nn_vide = 1 | n_eau ≈ 1,33 | n_verre ≈ 1,5\nRéflexion totale : sin(i_lim) = n₂/n₁  (n₁ > n₂)\n→ Application : fibre optique"},
    {"label": "Lentilles convergentes — formule conjuguée",
     "text": "1/OA′ − 1/OA = 1/f′  (relation de conjugaison)\nGrandissement : γ = OA′/OA = A′B′/AB\nDistance focale f′ = 1/vergence (en dioptries)\nObjets réels : OA < 0\n3 rayons constructeurs : parallèle→F′, par O, par F→parallèle"},
    {"label": "Spectre électromagnétique",
     "text": "Ondes radio | Micro-ondes | IR | Visible | UV | X | γ\n(longueur d'onde décroissante, fréquence croissante)\nVisible : 400 nm (violet) → 700 nm (rouge)\nToutes les ondes EM : c = λf  avec c = 3×10⁸ m/s dans le vide\nDispersion : un prisme dévie differemment chaque λ"},
    {"label": "Défauts de l'œil",
     "text": "Myopie : globe trop long ou cristallin trop convergent\n→ image avant la rétine → lunettes DIVERGENTES\nHypermétropie : globe trop court\n→ image derrière la rétine → lunettes CONVERGENTES\nPresbyties : cristallin rigide (accommodation réduite)\n→ verres progressifs"},
  ],

  ("physique", "Thermochimie et cinétique"): [
    {"label": "Enthalpie de réaction ΔrH",
     "text": "ΔrH = H_produits − H_réactifs  (kJ/mol)\nΔrH < 0 : réaction exothermique (libère de la chaleur)\nΔrH > 0 : réaction endothermique (absorbe)\nLoi de Hess : ΔrH = ΣΔfH(produits) − ΣΔfH(réactifs)\nΔfH (corps simple état standard) = 0"},
    {"label": "Loi d'Arrhenius & énergie d'activation",
     "text": "k = A·e^(−Eₐ/RT)\nEₐ = énergie d'activation (kJ/mol)\nR = 8,314 J/(mol·K)  |  T en kelvins\nPlus Eₐ est grande → réaction plus lente\nCatalyseur : abaisse Eₐ → accélère sans modifier l'équilibre\nln(k) = f(1/T) : droite de pente −Eₐ/R"},
    {"label": "Constante d'équilibre K et Le Chatelier",
     "text": "K = [produits]^stœchio / [réactifs]^stœchio\nPrincipe de Le Chatelier : toute perturbation déplace l'équilibre pour s'y opposer\n• Ajout réactif → équilibre vers les produits\n• Augment. T pour réaction endothermique → K augmente\n• Augment. P → favorise le côté avec moins de gaz"},
    {"label": "Ordre de réaction & vitesse",
     "text": "v = k·[A]ᵅ·[B]ᵝ  (déterminés expérimentalement)\nOrdre 1 : [A](t) = [A]₀·e^(−kt) | t½ = ln2/k\nOrdre 2 : 1/[A] = 1/[A]₀ + kt\nSuivi expérimental : spectrophotométrie, pH-métrie, conductimétrie"},
  ],

  ("physique", "Chimie des solutions — Acides & Bases"): [
    {"label": "Constantes acide-base",
     "text": "Ka = [H₃O⁺][A⁻] / [HA]  (constante d'acidité)\npKa = −log Ka  |  pH = pKa + log([A⁻]/[HA])  (Henderson-Hasselbalch)\nAcide fort : pKa << 0 (dissociation totale) → Ex. HCl, H₂SO₄\nAcide faible : pKa intermédiaire → Ex. CH₃COOH pKa=4,75\nCouple A/B : l'acide fort a la base conjuguée la plus faible"},
    {"label": "Calcul de pH",
     "text": "Acide fort (C mol/L) : pH = −log C\nBase forte (C mol/L) : pH = 14 + log C\nAcide faible : [H₃O⁺] ≈ √(Ka·C) → pH = ½(pKa − log C)\nBase faible : [OH⁻] ≈ √(Kb·C) → pH = 14 − ½(pKb − log C)\nTampon (acide+base conjuguée) : pH ≈ pKa"},
    {"label": "Dosage pH-métrique — lecture de courbe",
     "text": "Courbe pH = f(V_versé) : saut de pH au point d'équivalence\nPoint d'équivalence : dérivée dpH/dV maximale\nÀ mi-équivalence : pH = pKa (zone tampon)\nChoisir indicateur coloré dont virage est dans le saut de pH\nΔn(acide) = Δn(base) au point équivalent : CₐVₐ = CᵦVᵦ"},
  ],

  ("physique", "Chimie organique"): [
    {"label": "Groupes fonctionnels — tableau",
     "text": "Alcool : −OH\nAldéhyde : −CHO\nCétone : >C=O\nAcide carboxylique : −COOH\nEster : −COO−\nAmine : −NH₂\nAmide : −CO−NH−\nHalogénure : −X (F,Cl,Br,I)"},
    {"label": "Réactions importantes",
     "text": "Estérification : RCOOH + R′OH ⇌ RCOOR′ + H₂O (équilibre, lent, H⁺)\nSaponification : RCOOR′ + NaOH → RCOONa + R′OH (totale)\nAddition HX sur alcène (Markovnikov) : H sur C le moins substitué\nSubstitution nucléophile (SN2) : Nu⁻ + RX → NuR + X⁻"},
    {"label": "Spectroscopie IR — bandes caractéristiques",
     "text": "O−H large : 3200−3600 cm⁻¹ (alcool, acide)\nN−H : 3300−3500 cm⁻¹\nC=O : 1700−1750 cm⁻¹ (ester/acide ~1735, cétone ~1715)\nC−H : 2800−3000 cm⁻¹\nC=C : 1620−1680 cm⁻¹\n→ Identifier d'abord C=O, puis OH/NH pour distinguer les fonctions"},
  ],

  # ═══════════════════════════════════════════
  # SVT — Métabolisme cellulaire (section fine)
  # ═══════════════════════════════════════════
  ("svt", "Métabolisme cellulaire"): [
    {"label": "Bilan de la respiration cellulaire",
     "text": "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ~36-38 ATP\nÉtapes :\n① Glycolyse (cytoplasme) : glucose → 2 pyruvates + 2 ATP + 2 NADH\n② Cycle de Krebs (matrice mito.) : pyruvate → CO₂ + NADH + FADH₂\n③ Chaîne respiratoire (mb. interne) : NADH/FADH₂ + O₂ → H₂O + ~34 ATP"},
    {"label": "Fermentation — sans oxygène",
     "text": "Fermentation lactique (muscles, bactéries) :\n  Pyruvate → Lactate + NAD⁺ régénéré\nFermentation alcoolique (levures) :\n  Pyruvate → Éthanol + CO₂ + NAD⁺\nBilan énergétique : 2 ATP seulement (vs ~38 en aérobie)\nRôle : régénérer le NAD⁺ pour poursuivre la glycolyse"},
    {"label": "Photosynthèse — bilan et étapes",
     "text": "6CO₂ + 6H₂O + lumière → C₆H₁₂O₆ + 6O₂\nPhase lumineuse (thylakoïdes) :\n  Lumière + H₂O → O₂ + ATP + NADPH\nCycle de Calvin (stroma) :\n  CO₂ + ATP + NADPH → G3P → glucose\nRuBisCO : enzyme clé de la fixation du CO₂"},
  ],
}

# ── Injection ──────────────────────────────────────────────────────────
HTML_PATH = '/Users/stagiaire/flashcards/mobile.html'
OPEN_TAG  = '<script type="application/json" id="f-data">'
CLOSE_TAG = '</script>'

with open(HTML_PATH, encoding='utf-8') as f:
    html = f.read()

s = html.find(OPEN_TAG)
assert s != -1, 'f-data block not found'
e = html.find(CLOSE_TAG, s + len(OPEN_TAG))

data = json.loads(html[s + len(OPEN_TAG):e])

added = 0
for (subj_id, sec_title_partial), new_items in EXTRA.items():
    subj = next((x for x in data if x['id'] == subj_id), None)
    if not subj:
        print(f'  ⚠ sujet {subj_id} introuvable')
        continue
    sec = next((x for x in subj['sections'] if sec_title_partial in x['title']), None)
    if not sec:
        print(f'  ⚠ section "{sec_title_partial}" introuvable dans {subj_id}')
        continue
    existing_labels = {item['label'] for item in sec['items']}
    for item in new_items:
        if item['label'] not in existing_labels:
            sec['items'].append(item)
            added += 1

new_json = json.dumps(data, ensure_ascii=False, indent=2)
html = html[:s + len(OPEN_TAG)] + '\n' + new_json + '\n' + html[e:]

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✅ {added} items ajoutés')
for subj in data:
    print(f"\n  {subj['emoji']} {subj['name']}")
    for sec in subj['sections']:
        print(f"    [{len(sec['items'])} items] {sec['title']}")

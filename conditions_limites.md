Les conditions au bord dans un problème de résolution d'EDP peuvent être choisis pour représenter une certaine situation physique ou bien pour gérer les problèmes numériques. Souvent on va faire une combinaison des deux, surtout lorsqu'on a plusieurs variables comme pour Shallow-Waters.

# Conditions périodiques
Cette condition est spéciale car elle concerne les deux bords de notre domaine en même temps. L'idée est de simplement lier les deux bords du domaine. Ça marche bien lorsque les ondes se déplacent dans une seule direction et à des vitesses pas trop différentes. Mais c'est plutôt un cas de tests car c'est pas très réaliste lorsque les ondes se déplacent dans les deux directions et finissent par se croiser. On l'implémente sur les deux variables (car ça n'aurait pas trop de sens de le faire que sur une seule) de cette façon :
$$\begin{cases}
u_{N+1} &= u_1\\
u_{0} &= u_N\\
\eta_{N+1} &= \eta_1\\
\eta_{0} &= \eta_N
\end{cases}$$

Les conditions suivantes étant non périodiques, on va se concentrer sur le bord gauche, et donc aux valeurs $u_0$ et $\eta_0$ à la cellule fantôme.








# Conditions de Dirichlet
En général Dirichlet fait référence à une condition au bord constante imposée à la solution $f$ de l'EDP. Si $\Omega$ est ton domaine, $\partial \Omega$ sa frontière et $f$ l'inconnue de ton EDP, la condition au bord de Dirichlet s'écrit
$$f = \text{cst} \quad \text{sur} \quad \partial \Omega$$
Avec la constante qui peut potentiellement être nulle. Dans notre cas ça serait juste imposer des valeurs (qui peuvent dépendre du temps) pour $u_0$ OU $\eta_0$.

## Marée et vagues
Un exemple est d'imposer une valeur pour $\eta_0$ pour réprésenter la marée ou des vagues :
$$\eta_0^n = A\sin\left(\omega t^n \right)$$

## Rivière
Tu peux aussi imposer une vitesse entrante qui pourrait représenter une rivière qui plonge dans ton domaine :
$$u_0^n = u_r\left(t^n\right)$$
où $u_r$ est une fonction du temps.

## Caractéristiques
Ce n'est pas possible d'imposer une condition de Dirichlet aux deux variables si tu veux conserver une cohérence numérique et physique. Cette question ouvre sur l'étude des équations hyperboliques et leurs résolution et c'est très riche, ça représente des cours entiers de niveau M2 en maths. Tu peux trouver beaucoup d'information sur internet si ça t'intéresse. L'idée à retenir c'est que dans Shallow-Water, l'information se propoage à une certaine vitesse, sauf que cette vitesse est variable. Cela peut créer des ondes de choc et des ondes de relaxation, ce qui n'est pas toujours évident à gérer numériquement.

Si tu imposes Dirichlet à une des deux varriables et que tu ne veux pas de comportement spécifique pour l'autre, tu peux retrouver l'autre variable avec la méthode des caractéristiques. Pour le bord gauche l'idée est de conserver entre les différentes cellules l'invariant dans la direction droite->gauche :
$$R^- = u - 2 \sqrt{g(H+\eta)}$$
Pour le bord droite il faudrait conserver l'invariant dans la direction gauche->droite :
$$R^+ = u + 2 \sqrt{g(H+\eta)}$$

### Passer de $h$ à $u$
Si tu imposes $h_0$, tu peux retrouver $u_0$ avec la formule
$$u_0 = R^-_1 + 2 \sqrt{g(H\eta_0)}$$
où $R^-_1 = u_1 - 2 \sqrt{g(H+\eta_1)}$

### Passer de $u$ à $h$
Si tu imposes $u_0$, tu peux retrouver $h_0$ avec la formule
$$h_0 = \frac{\left(u_0 - R^-_1\right)^2}{4g}$$

# Conditions de Neumann
En général Neumann fait référence à une condition au bord constante imposée à la dérivée spatialle de l'EDP. Ça s'écrit
$$\frac{\partial f}{\partial x} = \text{cst} \quad \text{sur} \quad \partial \Omega$$

## Océan ouvert
La situation d'océan ouvert correspond à imposer un flux nul sur les deux variables.
$$\begin{cases}
u_0 = u_1\\
\eta_0 = \eta_1
\end{cases}$$

## Mur impérméable
Pour représenter un mur impérméable sur laquelle l'eau se réfléchirait, on peut faire
$$\begin{cases}
u_0 = 0\\
\eta_0 = \eta_1
\end{cases}$$
qui est un mélange entre une conditon de Dirichlet pour $u$ et de Neumann pour $\eta$.

## Mur parfaitement réflexif
Une autre possibilité serait d'imposer cette condition qui représente un mur parfaitement réflexif numériquement :
$$\begin{cases}
u_0 = -u_1\\
\eta_0 = \eta_1
\end{cases}$$
la condition sur $u$ est spéciale, ni de Dirichlet ni de Neumann.

## Pente de la surface de l'eau
Pour représenter une pente de la surface de l'eau, par exemple pour représenter une chute d'eau, on peut utiliser la condition de Neumann suivante
$$\eta_0^n = \eta_1^n - \beta\left(t^n\right)$$
où $\beta$ représente la pente de la surface de l'eau à l'entrée du canal.

## Variation de vitesse
Une manière de représenter un canal qui s'élargit ou un canal où l'eau accélère serait d'écrire
$$u_0^n = u_1^n - \alpha\left(t^n\right)$$
où $\alpha$ est une fonction évoluant avec le temps et représentant la variation de vitesse sur le côté gauche du canal.

## Flux non nul
On peut aussi imposer un flux non nul sur une des deux variables, par exemple
$$u_0 = \Delta x s u_1$$
impose que la hauteur de l'eau ait une pente de $s$ au bord gauche, ça représente par exemple un canal où l'eau coulerait. Dans ce cas, ainsi que le précédent, pour trouver l'autre variable, on peut soit faire une condition de Neumann simple, soit de nouveau utiliser la méthode de l'invariant.

# Réflexions parasites
Le soucis avec les conditions de Neumann, est qu'on a souvent des réflexions parasites dues à la résolution numérique. Ce que tu observes dans ton cas d'open ocean. Dans ce cas il y a plusieurs leviers pour régler cela.

## Schéma d'intégration spatial
Tu peux utiliser des schémas d'intégration spatial plus complexes qui minimisent ces soucis, mais ils peuvent impliquer d'avoir plusieurs cellules fantômes au lieu de une. cf. le diapo que je t'ai envoyé et mon rapport de stage.

## Condition au bord de Sommerfeld ou de radiation
Elle permet de laisser passer les ondes à l'extérieur sans réflexion parasite. On ajoute un terme à Neumann qui dépend de la dérivée temporelle pour "faire passer" les ondes artificiellement.
$$\frac{\partial f}{\partial t} + c \frac{\partial f}{\partial x} = 0 \quad \text{sur} \quad \partial \Omega$$
Par exemple pour $\eta$ à gauche, on choisit $c=R^-_n$ et on aurait
$$\eta^{n+1}_0 = \eta_1^n + R^-_n\frac{\Delta t}{\Delta x} \left(\eta ^n_1 - \eta^n_0\right)$$
A priori si tu veux faire de l'open ocean, ça marche mieux si tu fais Sommerfeld sur $\eta$ car c'est $\eta$ qui est la variable principale qui "porte" les ondes. Pour $u$ tu peux utiliser la méthode des caractéristiques ou simplement Neumann.

## Zone absorbante
Une autre solution est d'imposer une zone absorbante sur le bord de ton domaine, ainsi les réflexions parasites seront absorbées. Cela nécessite de modifier un peu les équations et donc le solveur et pas seulement les conditions aux limite.
$$\begin{cases}
\dfrac{\partial u}{\partial t} + u\dfrac{\partial u}{\partial x} + g\dfrac{\partial \eta}{\partial x} &= \nu \nabla^{2}  u - \color{red}{\sigma(x)(h-h_{\text{ref}})}\\
\dfrac{\partial \eta}{\partial t} + \dfrac{\partial}{\partial x}\big[(H+\eta)\,u\big] &= - \color{red}{\sigma(x)(\eta-\eta_{\text{ref}})}
\end{cases}$$
$\sigma$ est un coefficient d'amortissmenet vers le bord, typiquement pour le côté gauche encore une fois
$$\sigma(x) = \sigma_{\text{max}} \left(\dfrac x {L_a} \right)^2$$
où $L_a$ est la longueur de la zone absorbante (10% de la taille du domaine), et $\sigma_{\text{max}} = \dfrac{3c}{L_a}$ où $c$ va être la moyenne de de la vitesse. Et où $\eta_{\text{ref}}$ et $h_{\text{ref}}$ vont être les valeurs cible, donc $\eta_{\text{ref}}=0$ et $u_{\text{ref}}=0$ pour l'open ocean.

Si tu discrétistes ça dans ton solveur et que tu mets des conditions de Neumann sur $u$ et $\eta$ ça devrait résoudre les problème (avec le défaut de sacrifier une zone de simulation).
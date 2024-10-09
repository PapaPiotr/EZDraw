[CuteFen]


![test jpg](https://github.com/PapaPiotr/CuteFen/assets/167995662/b4b277ed-d5ca-459c-bfa1-e91282977e6b)
## English
## Description

EZDraw is a Python program that generates chess diagram pages.
Features

The program is presented as a form where users can determine layout and decoration parameters for the diagrams.
The diagrams can be generated from a FEN code, or from the problem id on lichess.org (ex : #wOUPe (needs internet connexion btw)).
It also features a basic pgn reader (make sur your pgn contains only one game) that allows you to quickly fetch the desired positions from a game.
You can also compose your position by hand or add some basic annotations (cross, arrows, etc) using the graphical position editor.
EZDraw can generate an A4-sized image containing all desired diagrams, or generate a separate image for each diagram.
EZDraw allows to save and load forms so you don't have to rebuild a page from scratch if you just want to make a minor change to a page you already edited.

## Use sources

-Make sure to have Python3 installed on your system
-Clone this depot
-Install dependencies by running the following line:
  pip install -r requirements.txt
-Run the program:
  python3 (or python) main.py

## Dependencies

This program uses the following libraries:

- Pillow 10.3.0
- PyQt6 6.4.2
- requests 2.31.0

## License

This program is distributed under the GNU General Public License version 3. Please refer to the LICENSE file for more details.

## Credits

- Chess piece images are created by Armando Hernandez Marroquin and are distributed under the GPLv2+ license.
- Board, arrow, and symbol images are created by Pierre Foulquié and are distributed under the GPL3 license.

## Français
## Description

EZDraw est un programme écrit en Python qui permet de générer des pages de diagrammes d'échecs à partir de codes FEN.

Le programme se présente sous la forme d'un formulaire permettant de déterminer les paramètres de mise en page et de décoration des diagrammes.
Les diagrammes peuvent être générés à partir d'un code FEN ou bien d'un identifiant de problème sur lichess.org (ex : #wOUPe (nécessite une connection internet)).
Il comprend également un lecteur de pgn basique (assurez-vous que le pgn utilisé ne contient bien qu'une seule partie) qui permet de récupérer rapidement les positions désirées à l'intérieur d'une partie.
Vous pouvez aussi composer vos positions à la main ou rajouter des annotations basiques (flèches, croix, etc...) en utilisant l'éditeur graphique de position.
EZDraw permet de générer une image de format A4 contenant tous les diagrammes souhaités, ou bien de générer une image séparée pour chaque diagramme.
EZDraw permet de sauvegarder et charger des formulaires afin de ne pas avoir à recomposer une page de 0 si vous souhaitez simplement effectuer un changement mineur sur une page déjà éditée.

## Utilisation depuis les fichiers source.

-Assurez vous d'avoir installé Python3 sur votre machine
-Clonez ce dépot
-Installez les dépendances en utilisant la commande suivante:
  pip install -r requirements.txt
-Lancez le programme:
  python3 (ou python) main.py

## Dépendances

Ce programme utilise les bibliothèques suivantes :
- Pillow 10.3.0
- PyQt6 6.4.2
- requests 2.31.0

## Licence

Ce programme est distribué sous la licence GNU General Public License version 3. Veuillez consulter le fichier LICENSE pour plus de détails.

## Crédits

- Les images des pièces d'échecs sont réalisées par Armando Hernandez Marroquin et sont distribuées sous la licence GPLv2+.
- Les images de plateau, flèches et symboles sont réalisées par Pierre Foulquié et sont distribuées sous la licence GPL3.

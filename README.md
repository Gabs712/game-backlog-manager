# GAME BACKLOG MANAGER
#### Video Demo:  <https://youtu.be/Itpo8vly794>
#### Description:
 The purpose of this program is to create a list of games that the user might be willing to play and permanently record this information.


Among the main functionalities of the program are:

- Provide a user interface utilizing the user input on the terminal
- Search for a new game and view information about it
- Add the game to an permanent list
- Remove the game from an already existing list

\
The program utilizes the _curses_ module in order to create a dynamic interface. In order to navigate through the menu, the user might use the up and down arrows to highlight an option, the enter key to select the option, and the esc key to go back to the previous section of the menu.


When searching for a game, up to ten options of matching results are offered to the user, when an option is choose, several related information are shown and then the game can be stored in a file called _backlog.txt_.

To have access to these piece of information, the program makes use of a module called _howlongtobeatpy_, that gives it access to the API of the website _howlongtobeat.com_, wich is a site known for assemble information about the playtime of a vast variety of games. I've choosen to utilize this API because it provides a set of valuable information when choosing to play a game, because of that, this API is highly compatible with the purprose of this project.

##### Observation: To this program work poperly, the terminal must be in fullscreen.

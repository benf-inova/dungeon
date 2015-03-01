# dungeon
Class for generating a random rogue-like dungeon
* Developed using Python 3.4

*Using whatever languages, frameworks and libraries you choose write a Roguelike dungeon generator. (http://en.wikipedia.org/wiki/Roguelike) Your system should generate random but sensible dungeons - e.g. there should not be isolated areas that are unreachable and there should be an entrance and exit.*

*The presentation of your dungeons is up to you. Take the implementation as far as you'd like. Some ideas:*  
*- generate dungeons with provided x/y dimensions*  
*- treasures*  
*- monsters*  
*- locked doors w/ accessible keys*  
*- other terrain types*  
*- obstacles (fire, water, pits, traps)*  

**Generating a Dungeon**  
1. Create an instance of a Dungeon 'object' providing the dungeon's:  
* Height  
* Width  
* Maximum number of Rooms  
* Minimum Room Size  
* Maximum Room Size  
2. Call generate_random_dungeon() on the newly made dungeon 'object'  

**Printing a Dungeon**  
1. Pass your dungeon 'object' to the print command  
    `ex: print(my_dungeon)`  
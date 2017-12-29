### Seshat

Seshat started as an attempt to roll my own personal management program using Python.  I use Asana for what we might call "life management" to keep track of recurring tasks, events, and reminders that I want.  It works great.  But I often found myself wanting to keep more of an "idea list" or log of ideas for projects or bits of analysis I wanted to do.  For whatever reason, tracking these longer term tasks using Asana did not appeal.  

So I started Seshat, which populates a text file on my desktop with an idea log via a simplistic CLI.  It was a great exercise in some very basic programming features:
- encryption of some passphrases key info in the program
- Asana API interaction
- using MongoDB to store both Asana tasks pulled using the API along with locally generated ideas and todos.

Eventually though I stumbled across this [article](https://zwischenzugs.com/2017/12/03/how-i-manage-my-time/) which convinced me to slightly alter the way I use Asana to encapsulate my life management and idea log needs.  I plan to begin some note-taking using Git and I realized Asana boards will work great as an idea-list.

So for now, Seshat ([the Egyptian goddess of knowledge](https://en.wikipedia.org/wiki/Seshat)), lies dormant.  

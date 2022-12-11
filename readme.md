# Spyder - Chatting safely

## Why should you choose Spyder?

The idea to create Spyder was formed in 2021. The first implementation wasn't a bad
approach, but it wasn't a professional one. One year later (now) I started this project again
from sketch, just to make sure every bit of it is logical. In the 2021 version, security
wasn't my main problem, thus I skipped the development of security almost entirely. The currently
developed 2022 Spyder is mainly focused on 3 things: **security**, **accessibility**
 & **extensibility**. I truly think that a Spyder fulfills all of the 3 aspects mentioned above.

## Security

As I mentioned earlier, security was on of my main concerns. I wanted to create a **quantum-safe**
chat. But that's something others can offer as well. Spyder's main strength lies in the
server structure. There are 2 types of servers: **network** & **group**. Group servers are casual servers
like Discord groups. Network servers serve however completely different purposes. Each group server can
be assigned to a network server. Once that's done every user from the network can connect to that group
server. Other network users have to create a mirror user before joining the network.

### Why does this help?

The credentials are only stored on one server: the network server. That means you can't join a group which could steal your credentials. But well this isn't anything special yet. The main thing is, you can't
do that with Discord for example. You connect to Discord's "network" servers and you validate yourself
there. That means if someone gets into the Discord servers, your password will be leaked. Spyder offers
you to host your own network server, so you know exactly what happens there, you can set up your own
defense, and you can set policies which would ban users from the network or prohibit the use of
functionalities.

## Accessibility

Spyder can be accessed from your terminal! Yes you heard that right. Spyder was written in python with
ncurses/curses, which means it's entire UI is in your terminal. No need for any window manager, a
plain SSH shell can open Spyder! You can use Spyder to chat with your buddy from a headless RPi server.

## Extensibility

Spyder's extensibility lies in the plugin system. You can create various plugins in an event
oriented way with python. Plugins can manage almost your entire screen! Of course plugins present
a new problem regarding security, so if you want to be sure everything is safe in your Spyder
environment, don't use plugins! I'm constantly looking for malicious plugins and the plugins
uploaded in the `plugins` folder should be safe.

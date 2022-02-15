# CSGO Computer Vision (WIP)

In this repository you can find models of csgo objects using cascade classifiers.

![CT detection example](https://user-images.githubusercontent.com/26195439/138152437-7befbba8-4e1c-4d63-815b-32fd8c3a5ea8.gif)

## Setting Up

TODO :)

## How to training your data

### Getting backgrounds

It is recommended but not necessary to use the following commands when collecting data

`cl_drawhud 0` to disables your HUD

`crosshair 0` disables your [funky crosshair](https://esports-news.co.uk/wp-content/uploads/2017/06/crosshair-generators-csgo-1.jpg)


There are two main methods I found to collect backgrounds

- Record yourself playing a map alone
- Record a bot playing a deathmatch alone

The latter one is probably less time consuming since you could just change the `host_timescale` but the BOT can often repeat routes and you can get frames from repeated places.

## Data Roadmap

### Positives 

- [ ] [Counter terrorists](https://counterstrike.fandom.com/wiki/Counter-Terrorists#Factions)
  - [ ] FBI
  - [ ] GIGN
  - [ ] GSG-9
  - [x] IDF (600 samples)
  - [ ] SWAT
  - [ ] SAS
  - [ ] SEALS
  - [ ] Custom Models
- [ ] [Terrorists](https://counterstrike.fandom.com/wiki/Terrorists#Factions)
  - [ ] Anarchist
  - [ ] Balkan
  - [ ] Elite Crew
  - [ ] Phoenix Connexion
  - [ ] Pirate
  - [ ] Professional
  - [ ] Separatist 

### Negatives/Backgrounds

- [ ] Mirage
- [ ] Inferno
- [ ] Train
- [x] Dust2 (900 samples)
- [ ] Overpass
- [ ] Nuke
- [ ] Cache
- [ ] Cobblestone
- [ ] Vertigo
- [ ] Ancient

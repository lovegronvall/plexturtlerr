```
   .
           .                 .          .                               .
  _|__:                          .    . .      ·
_/ |·:|__:_|___________ :____|_  .      :      :        .....   :_______|_ _
\     |  | |·:\_______/_|    |:\ :____|_|      |_____ .::·  ·:. |   _   |:\_\_
 \    :  |     /      ·:|       \|    |:\   ________/_::   .:·  |  _/      / /
  \_     :    /         |      \ \       \_  ·:|      ·:..:·  .:·:.\______/ ·
    \______|_/________|_|______|\         /______       ·:::::· |.·  ·:|
         . |  .    .  | :      : \____|__/      \____|_/        :      :
           .          . :__|_  ·     ·|              |          ·      .
        _|____|_  _|____|  |:\ :     :.       .....  .
      _/ |    |:\/ |  ·:|     \|     |_____ .::·  ·:.
     /      :    \      :      \_ ________/_::   .:·
  · /    :  |     \______       /  ·:|      ·:..:·  .:·:.
_/_/     |__|_|____/    \____|_/_|____        ·:::::·  .·
\_\_|____|  : |              |   |   \_____|__/
    |    :    .              .   .         |
    .                                      .
```
turtlarr is a little software to set qBittorrent to turtle mode when ever someone watches a stream on your Plex server

I prefer to create a docker image, just clone the repo, enter the repo dir and run
```docker build . -t turtlarr```

Then you can use the image you just built in docker-compose:
```
---
services:
  turtlarr:
    image: turtlarr
    container_name: turtlarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - ./turtlarr:/config
    restart: unless-stopped
```
Just make your you have your config file available in one of the following locations:
```
/config/turtlarr.conf
config/turtlarr.conf
turtlarr.conf
```

Afterwards
Enjoy
//czi

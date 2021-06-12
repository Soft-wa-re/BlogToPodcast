---
layout: post
title:  "Basics of Docker"
tags: [Programing, GeneralAdvice, Docker, Tools]
permalink: /basics-of-docker/
---

I am brand new to docker, so I though I might start documenting docker from the perspective of a beginner.  I will come back and correct any bad info as necessary.

### Mental Model
Docker data structures are similar to git.  If you understand the git ([Merkle Trees](https://en.wikipedia.org/wiki/Merkle_tree)), then you would understand the docker data structure.

### Running an Interactive Session
Assuming you want to start a docker image, you are gonna need a command like this. The 'i' stands for interactive. 't' stands for tty.

```bash
docker run -it ubuntu bash
```

### Running a GUI
Some of the guides out there I found to be a little complex if you are looking for something easily copy-and-pasteable.

```bash
#Host machine
XAUTH_COOKIE=$(xauth list | head -n 1 | sed -e s/:/$(echo $DISPLAY)/g)
docker run -it --net=host -e DISPLAY -e XAUTH_COOKIE="$XAUTH_COOKIE" -v /tmp/.X11-unix ubuntu bash

#Docker container
apt update; apt install -y xauth; xauth add $XAUTH_COOKIE;

#Test it. Make sure you don't have pinta on your host machine running otherwise X seems to get confused and create a new window for your host install of pinta.
apt install -y pinta; pinta
```
See also: 
1. [Geeks for Geeks](https://www.geeksforgeeks.org/running-gui-applications-on-docker-in-linux/)
2. [CloudSavvyIt](https://www.cloudsavvyit.com/10520/how-to-run-gui-applications-in-a-docker-container/)
3. [FabioRehm](http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/)


### Sharing data with the host
To do this effectivly you have to understand a little bit more about how docker works and the relevant permissions.

So yes, the below command will technically work, the problem though is, the `dockerworkspace` folder on the host machine will be owned by root.  Meaning to interact with it in any way you will need to be root.
```bash
docker run -v ~/dockerworkspace:/workspace ubuntu
```


I think you will find the below series of commands much more effective.
```bash
#On the host machine create mappings of the permissions config files.
PERM_CONF="-v /etc/passwd:/etc/passwd -v /etc/group:/etc/group -v /etc/shadow:/etc/shadow"
perm_conf=( $PERM_CONF )
#Run your docker container providing the permissions config files.
docker run -it -v ~/dockerworkspace:/workspace "${perm_conf[@]}" ubuntu

#When the mountbind is created it will be owned by root.  You can fix that like this. 
chown normalHostUser workspace/
chgrp normalHostGroup workspace/

#Now login to your normal host user account.
su normalHostUser

#Create a file with permissions that your normal host user will be able to access.
touch /workspace/createNonRootOwnedFile

#Logout of normalHostUser (on docker)
exit

#Logout of root (on docker)
exit

#Confirm it worked (on host)
ls -la ~/dockerworkspace
total 8
drwxr-xr-x  2 normalHostUser normalHostGroup 4096 Jun  6 14:55 .
drwxr-xr-x 35 normalHostUser normalHostGroup 4096 Jun  6 14:50 ..
-rw-rw-r--  1 normalHostUser normalHostGroup    0 Jun  6 14:55 createNonRootOwnedFile
```

See Also:
1. [Stack Overflow: Share Files Between host system and docker container](https://stackoverflow.com/questions/27925006/share-files-between-host-system-and-docker-container-using-specific-uid)
2. [Marc Campbell: Understanding how uid and gid work in Docker containers](https://medium.com/@mccode/understanding-how-uid-and-gid-work-in-docker-containers-c37a01d01cf)

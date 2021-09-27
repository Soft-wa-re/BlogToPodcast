Getting Started

Python
1. With out a lot of testing to confirm this claim, you should need two things installed: Docker and Python.
2. Run `python3 ./buildDocker.py`, this should provide you with a docker image that you can run.

Ba(sh)
1. With out a lot of testing to confirm this claim, you should need two things installed: Docker and bash.
2. Run `./buildDocker.sh`, this should provide you with a docker image that you can run.
3. Navigate to the test folder, and run 
    a. `./runBlogCast.sh`
    b. `./runBlogCastDebug.sh`
    c. `./runBlogCastIterate.sh`

Todo:
1. Switch Docker to Podman or minikube
2. Develop better config/command interface to tell BlogCast what files need to be ingested.
3. Develop better system for transforming incoming files into text that is ready to be processed.
4. Train better voice models.
5. Move python package dependencies into setup.py
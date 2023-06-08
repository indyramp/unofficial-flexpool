FlexFarmer Docker Usage Instructions
========================================================================

Requirements
------------------------------------------------------------------------

- Docker daemon installed on your computer


Pulling the image
------------------------------------------------------------------------

First, you need to pull the docker image. It is done by:

    docker pull flexpool/flexfarmer

This will fetch the latest version of flexfarmer. Alternatively, you can
specify a custom version as a tag to the docker image:

    docker pull flexpool/flexfarmer:v1.x.x

Configuring, and Running FlexFarmer
------------------------------------------------------------------------

As with the regular FlexFarmer setup, you will need to prepare a
config.yml file and mount it to the docker container you will create.
You will also need to pass the plots by mounting the plot directories
as volumes.

    docker run -v $PWD/config.yml:/config.yml -v /mnt/plotdir1:/mnt/plotdir1 flexpool/flexfarmer -c /config.yml

Explanation of the command:
- docker run -- Run the docker image (create a container based on docker image)
- -v $PWD/config.yml:/config.yml -- Mount the config file located in <current working directory>/config.yml to /config.yml inside the container
- -v /mnt/plotdir1:/mnt/plotdir1 -- Mount the plot directory
- flexpool/flexfarmer -- Use FlexFarmer official docker image
- -c /config.yml -- Tell FlexFarmer the config file to use inside the docker container (we have mounted it as /config.yml)

Note: $PWD is a UNIX environment variables that resolves to the current working directory path.
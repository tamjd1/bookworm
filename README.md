![bookworm logo](logo.png)
# 

### Overview
Project: bookworm

### Prerequisites
- Docker
- Google Chrome

### Getting Started
``docker-compose build``

``docker-compose up``

### To delete database volume and force recreate containers 
``docker-compose down --volumes``

``docker-compose up --force-recreate``

### To add the chrome extension

- Enable Developer mode
- Load the ``chrome_extension`` folder using ``Load unpacked`` option
- Go to ``chrome://bookmarks/`` in your browser
# Article sharing web app

## About
Article sharing is web app, where you can share useful web development articles with everybody. <br>
Live DEMO https://share-articles.herokuapp.com/

## Setup

#### Prequisites
- VirtualBox from https://www.virtualbox.org/
- Vagrant from https://www.vagrantup.com/

#### Setup
Clone this repository
```
git clone git@github.com:karlveskus/article-sharing.git
```

Change directory to project folder
```
cd /article-sharing
```

Start virtual machine 
```
vagrant up
```

SSH into virtual machine.
```
vagrant ssh
```

Change directory to project folder
```
cd ../../vagrant
```

Generate database
```
python models.py
```

Start application
```
python app.py
```

Access the application ```locally``` using http://localhost:5000

## Using own GitHub oauth
Currently this app is using default pre-made oauth. F ollow steps below to create your own.

1. Go to https://github.com/settings/applications/new
2. Register a new OAuth application (Set authorization callback URL to http://localhost:5000/github-callback)
3. Open ```config.py```
4. Set up new ```GITHUB_CLIENT_ID``` and ```GITHUB_CLIENT_SECRET```

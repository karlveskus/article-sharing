# Article sharing web app

## About
Article sharing is web app, where you can share useful web development articles with everybody. <br>
Live DEMO https://share-articles.herokuapp.com/

## Setup

#### Prequisites
- VirtualBox from https://www.virtualbox.org/
- Vagrant from https://www.vagrantup.com/

Node: Due Vagrant and VirtualBox incompatibilities in some versions I suggest to use VirtualBox version 5.1.X

#### Setup
Clone this repository
```
git clone https://github.com/karlveskus/article-sharing.git
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

Start application
```
python app.py
```

Access the application ```locally``` using http://localhost:5000

## Using own GitHub oauth
Currently this app is using default pre-made oauth with authorization callback URL to ```http://localhost:5000/github-callback``` so authorization works only locally. Follow steps below to create your own oauth for different URL.

1. Go to https://github.com/settings/applications/new
2. Register a new OAuth application (Set authorization callback URL to http://```<APP_URL>```/github-callback)
3. Open ```config.py```
4. Set up new ```GITHUB_CLIENT_ID``` and ```GITHUB_CLIENT_SECRET```

## API endpoints

### Get all topics
```
GET /api/topics
```
##### Response
```
[
  {
    "id": 1, 
    "name": "JavaScript"
  }, 
  {
    "id": 2, 
    "name": "HTML"
  }, 
  {
    "id": 3, 
    "name": "CSS"
  }
]
```

### Get a single topic
```
GET /api/topics/:topic_id
```
##### Response
```
{
  "id": 1, 
  "name": "JavaScript"
}
```

### Get all articles in topic
```
GET /api/topics/:topic_id/articles
```
##### Response
```
[
  {
    "date_added": "Tue, 24 Oct 2017 00:00:00 GMT", 
    "description": "Learn HTML Links", 
    "id": 4, 
    "title": "HTML Links", 
    "topic_id": 2, 
    "url": "https://www.w3schools.com/html/html_links.asp"
  }, 
  {
    "date_added": "Wed, 25 Oct 2017 00:00:00 GMT", 
    "description": "This article's intent is to help clarify some of the advantages and disadvantages of using frames and provide resources for further information.", 
    "id": 5, 
    "title": "TO FRAME OR NOT TO FRAME: THAT IS THE QUESTION", 
    "topic_id": 2, 
    "url": "http://websitetips.com/articles/html/frames/"
  }
]
```

### Get a single article from topic
```
GET /api/topics/:topic_id/articles/:article_id
```
##### Response
Note: The article's topic_id has to match with given topic_id
```
{
  "date_added": "Tue, 24 Oct 2017 00:00:00 GMT", 
  "description": "Learn HTML Links", 
  "id": 4, 
  "title": "HTML Links", 
  "topic_id": 2, 
  "url": "https://www.w3schools.com/html/html_links.asp"
}
```

### Get all articles
```
GET /api/articles
```
##### Response
```
[
  {
    "date_added": "Sat, 21 Oct 2017 00:00:00 GMT", 
    "description": "Cool article about async javascript", 
    "id": 1, 
    "title": "JavaScript Async/Await Explained in 10 Minutes", 
    "topic_id": 1, 
    "url": "https://tutorialzine.com/2017/07/javascript-async-await-explained"
  }, 
  {
    "date_added": "Sun, 22 Oct 2017 00:00:00 GMT", 
    "description": "Best Webpack tutorial", 
    "id": 2, 
    "title": "Learn Webpack in 15 Minutes", 
    "topic_id": 1, 
    "url": "https://tutorialzine.com/2017/04/learn-webpack-in-15-minutes"
  }, 
  {
    "date_added": "Mon, 23 Oct 2017 00:00:00 GMT", 
    "description": "Everything You Should Know About Progressive Web Apps", 
    "id": 3, 
    "title": "Everything You Should Know About Progressive Web Apps", 
    "topic_id": 1, 
    "url": "https://tutorialzine.com/2016/09/everything-you-should-know-about-progressive-web-apps"
  }
]
```

### Get a single article
```
GET /api/articles/:article_id
```
##### Response
```
{
  "date_added": "Sat, 21 Oct 2017 00:00:00 GMT", 
  "description": "Cool article about async javascript", 
  "id": 1, 
  "title": "JavaScript Async/Await Explained in 10 Minutes", 
  "topic_id": 1, 
  "url": "https://tutorialzine.com/2017/07/javascript-async-await-explained"
}
```

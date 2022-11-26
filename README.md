# music_player
![](https://imgur.com/e4gFXK0.png)
My music is a cloud music player which allows you to add and listen songs from anywhere in the world.

### Features
It allows you to:
 - Add new albums 

  ![album](https://imgur.com/t57ukkK.png)

 - Add songs to Albums

   ![](https://imgur.com/swOZKEU.png)

 - Search for songs and Albums

   ![](https://imgur.com/YpxVFah.png)


### Usage
I am using python "3.10.6" version 

first step clone my project
```
git clone https://github.com/sorooshm78/music_player/
```

and then install requirements  
```
pip install -r requirements.txt
```

This will create all the migrations file (database migrations) required to run this App.
```
python manage.py makemigrations
```

Now, to apply this migrations run the following command
```
python manage.py migrate
```

### Running the code 
Just go into the code directory and type 
```
python manage.py runserver
```
"music_player" app will start on 127.0.0.1:8000 (Local Address).
 
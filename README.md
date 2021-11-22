# Trend-Identification-on-Stack-Overflow

# Team-30B
Team 30B repository  


**Project title: Trend Identification on Stack Overflow  
Client/Supervisor: Dr. Christoph Treude**

## MCI Poster Presentation Team 30B >> [click here](https://www.youtube.com/watch?v=xgLYr9b-5k8)


## About the Team

**Team members**  
Tianjiao Jiang (a1807401)   
Po-Yi Lee (a1806297)   


## Branch Structure 

### master

The master contains all the code.   
 

### project_management_m2 

This branch contains project management documents for milestone 2.  
For details please see README.md in this branch.  


## Running the Latest Prototype
#### important for testers/developers: to save your BigQuery quota, please do not enter too many time windows  

1. install mysql 8.0  
**remember your username (= "root" by default) and password**  

2. create a database named "stack" using mysql  

3. install all necessary python3 packages:  
   spacy  
   google-cloud  
   google-cloud-bigquery  
   google-cloud-storage  
   django 3.0  
   inflect  
   pyspellchecker  
   pymysql   

4. in mysite/settings.py, set your **username and password**  
```
'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'stack',
            'USER': 'root',
            'PASSWORD': '',  # todo: use your own password
            'HOST': '127.0.0.1',
            'PORT': '3306',
}
```  

5. run the following commands
```
python manage.py makemigrations
python manage.py migrate
```
  
6. run the software on port 8000  
```
python manage.py runserver
```

# Trend-Identification-on-Stack-Overflow

# Team-30B
Team 30B repository  


**Project title: Trend Identification on Stack Overflow  
Client/Supervisor: Dr. Christoph Treude**

- Business case >> [click here](https://github.com/boyleerock/Trend-Identification-on-Stack-Overflow/blob/main/Business%20Case%20and%20Draft%20Plan%20-%20Trend%20Identification%20on%20Stack%20Overflow%20-%20Team%2030-3-1.pdf)         
- Poster Presentation >> [click the video!](https://www.youtube.com/watch?v=xgLYr9b-5k8)             
- Poster (shown below)>> [click here](https://github.com/boyleerock/Trend-Identification-on-Stack-Overflow/blob/main/MCI%20Poster%2030B%200406%20.pdf)  
![poster_trend identification on stackoverflow](https://user-images.githubusercontent.com/61671531/142989517-6240ccca-44b3-4772-99b8-3b4bdd58bd30.png)

- Final report (包含使用說明) >> [click here](https://github.com/boyleerock/Trend-Identification-on-Stack-Overflow/blob/main/MCIP_Final_report_Team30B_Po-Yi%20Lee.pdf)              

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

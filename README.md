## FUNCTIONALITY ##

This app help the Football fans be engaged with their favourite teams.

User can login and see their favourite teams, see all their favourite teams matches and even predict the match result.

The concept is the club names and the matches with the player information is fetched via the club API and directly displayed on the application. 
So, conceptually the application does not handle the data of the clubs, the players and the matches.

On a perfect prediction the user gets 1 point as a reward, which they can check from their profile.

And using these rewards there are various perks a user can avail which will help in more user engagement.

## TECHNOLOGIES ##

I have used Pyhton with Django as a framework. Since Django has built in admin panel, helps with CSRF Tokens, Authentication System and managing complex data models with ORM.
For now, the admin has to change the status of the match as soon as it is completed and also select the winning team.

For updating the rewards of a user if his prediction is true, I have used "Signals" and "Celery", which helps to run asynchronous tasks in the background.

I have also used custom annotations to make the code more clean and readable.

For Database I have used MongoDB. And to use MongoDB with Django I have used a library "pymongo". 

This app right now does not have its full implementation but it has some core functionalities of what it does.

## APP / MODULE DESCRIPTION ##

Core
- Models: It contains models for Club, Matches and userProfile
- Views: Handles the processing and data for matches and clubs
- Admin: COnfigures the Admin interface of Django for managing models

Users
- Authentication: Manages user logins, registrations and profiles
- Views: Provides views for user related actions

Matches
- Management: Allows for updation of match data
- Views: Displays the match data to users

## How to run the application locally

1) Clone the Repository
   ```
      git clone https://github.com/Irish011/fanconnect.git
      cd fanconnect
   ```
   
2) Create a Virtual Environment
   ```
      python -m venv env
      source env/bin/activate  #MacBook
      env\Scripts\activate     #Windows
   ```
   
3) Install the dependencies
   ```
      pip install -r requirements.txt
   ```
   
5) Start the server
   ```
      python manage.py runserver
   ```
   
7) Access the application on
   ```
      http://localhost:8000
   ```
   
9) Create a superuser to access Admin panel
   ```
      python manage.py createsuperuser
   ```

## DATABASE

For database Create a Database in MongoDB and have 3 collections matches, clubs and players. The flow of the application is that the data of these 3 collections come from an API, so you have to manually input the data in those collections for demo use.

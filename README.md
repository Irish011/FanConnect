## FUNCTIONALITY ##

This app help the Football fans be engaged with their favourite teams.

User can login and see their favourite teams, see all their favourite teams matches and even predict the match result.

The concept is the club names and the matches with the player information is fetched via the club API and directly displayed on the application. 
So, conceptually the application does not handle the data of the clubs, the players and the matches.

On a perfect prediction the user gets 1 point as a reward, which they can check from their profile.

And using this rewards there is various perks a user can get which will help in more user engagement.

## TECHNOLOGIES ##

I have used Pyhton with Django as a framework. Since Django has built in admin panel, helps with CSRF Tokens, Authentication System and managing complex data models with ORM.
For now, the admin has to change the status of the match as soon as it is completed and also select the winning team.

For updating the rewards of a user if his prediction is true, I have used "Signals" and "Celery", which helps to run asynchronous tasks in the background.

I have also used custom annotations to make the code more clean and readable.

For Database I have used MongoDB. And to use MongoDB with Django I have used a library "pymongo". 

This app right now does not have its full implementation but it has some core functionalities of what it does.

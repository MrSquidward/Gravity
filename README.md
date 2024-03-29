# Gravity
Gravity is GUI application wirtten in Python with TKinter library by two students of WUT in their free time. It simulates movement of objects under the action of gravity force. User can specyfiy number of objects as well as starting position, mass and velocity.

## Install and run using pipenv
```
git clone https://github.com/MrSquidward/Gravity.git
cd Gravity
pipenv shell
pipenv install
python main.py
```

## GUI
![readme](https://user-images.githubusercontent.com/50464859/76998937-265db200-6956-11ea-8682-be13e6b182c5.png)

## Physical background
Objects with mass affects on each other by [gravity force](https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation). At first this force is being transfered into acceleration (due to [Netwon's second law](https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion#Newton's_second_law)) and split into two dimensions (x and y) with use of cosinus function. After that acceleration is being integrated into velocity and position*:
  * new_velocity = acceleration_x * time + old_velocity
  * new_position_x = (acceleration_x (time ^ 2) / 2) + old_velocity * time + old_position_x
 
 
 where velocity, position and acceleration are values in x dimention. Formulas in y dimention apply by analogy.
 
 
Unfortunately, distance between objects is dependent on time, which makes this equation false in general case**. To solve this properly it is needed to use complex math (sloving a derivate equation with unknown function) and can't be easliy computed (or I can't do this at the moment). However, this can be avoided by assuming that distance is constant during small peroid of time (which is good approximation if we take it short enough). Now it is only needed to calculate these formulas all over again after certain period of time (after which current approximation is no longer good) and that is what program essentially does.


*[see how it is done](https://openstax.org/books/university-physics-volume-1/pages/3-6-finding-velocity-and-displacement-from-acceleration)

**these equations come true (and simple) when it is possible to factor out every parameter outside the intgral. This is possible as long as parameters don't depend on integrating variable (in example linked above acceleration is direcly known, but in our case we don't have that pleasure, distance function is unknown)

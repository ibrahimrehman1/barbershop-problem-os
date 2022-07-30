# The Barbershop Problem
Barbershop Problem - A Classical Synchronization problem - Operating Systems (OS) Complex Engineering Project of 6th Semester

# Problem Description?
A barbershop consists of a waiting room with n chairs, and the barber room containing the barber chair. If there
are no customers to be served, the barber goes to sleep. If a customer enters the barbershop and all chairs are
occupied, then the customer leaves the shop. If the barber is busy, but chairs are available, then the customer sits
in one of the free chairs. If the barber is asleep, the
customer wakes up the barber. Write a program to coordinate the barber and the customers.

To make the problem a little more concrete, the following information is added:
* Customer threads should invoke a function named getHairCut.
* If a customer thread arrives when the shop is full, it can invoke balk, which does not return.
* Barber threads should invoke cutHair.
* When the barber invokes cutHair, there should be exactly one thread invoking getHairCut concurrently.

# Group Members?
1) Ibrahim Rehman
2) Hasnain Ali Arain
3) Eesha Ansari
4) Heba Naveed

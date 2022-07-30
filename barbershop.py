# Import Libraries
import threading
from time import sleep as sp
import random
import sys

# Semaphores Declaration

# For Synchronization between Barber and Customers
BARBER_SEM = threading.Semaphore(0)
CUSTOMERS_SEM = threading.Semaphore(0)
# For Mutual Exclusion 
MUTEX = threading.Semaphore(1)

# GLOBAL VARIABLES

SLEEPING = False        # bool  -> True if Barber is sleeping else False
WAITING_CUSTS = 0       # int   -> Number of Customers present in Waiting Room
TOTAL = 0               # int   -> Total Customers present in BarberShop
WAITING_LIST = []       # str[] -> Names of Customers present in Waiting Room
BARBER_CHAIR_CUST = ""  # str   -> Name of Customer getting Haircut

# A Class to Initialize all the Threads and take user input for Number of Chairs and Number of Customers
class BarberShop:
    def __init__(self):

        print("*"*50) 
        print("\tWelcome to BarberShop")
        print("*"*50) 

        global NUM_CUST
        NUM_CUST = int(input("Please enter number of customers? \n"))

        global CHAIRS
        CHAIRS = int(input("Please enter number of chairs? \n"))

        if (NUM_CUST > 0):
            print("Barbershop Opening!!...\n")
            sp(random.choice([1,2,3]))
            
         # if user want more customer including customer define in example list
        if (NUM_CUST> 8):
            for i in range(9, NUM_CUST+1):
                self.customers.append(f'Customer{i}')

        # Initializing Barber Thread
        br = Barber()
        barber_thread = threading.Thread(name="Barber" , target=br.barberMain)
        barber_thread.start()
        sp(random.choice([1,2,3]))
        
        # Demo Customer Names
        self.customers = ["Heba","Eesha","Hasnain","Ibrahim","Izma","Bisma","Ayesha","Sadaf"]
        self.cust_threads = []

        # Initializing Customer Threads
        for index, cust in enumerate(self.customers[:NUM_CUST]):
            sp(random.choice([1,2,3]))
            cs = Customer(cust)
            customer_thread = threading.Thread(name="Customer", target=cs.customerMain, args=['{}({})'.format(cust, str(index+1))])
            customer_thread.start()
            self.cust_threads.append(customer_thread)

        # Joining customer threads
        if (len(self.cust_threads)):
            for t in self.cust_threads:
                t.join()

# A Barber Class to manage all Barber Functions            
class Barber:

    def  barberMain(self):

        global TOTAL, WAITING_CUSTS, SLEEPING , WAITING_LIST, BARBER_CHAIR_CUST, NUM_CUST

        while True:

            print("Barber- Barber checks waiting room for more customers")

            if (WAITING_CUSTS):
                print(f"Number of customers present in Waiting Room: {WAITING_CUSTS}\n")
                print("Waiting customers are : " , WAITING_LIST,"\n")               

            # If no customer is present in Waiting Room as well as Barber Room
            if (WAITING_CUSTS == 0 and TOTAL == 0):
                print("Barber found no customer")
                print("Barber - I am going to sleep\n")
                if NUM_CUST == 0:
                    print("No more customers :( \nBarberShop Closing!!...")
                    break
                SLEEPING=True
                # Barber is sleeping and waiting for more customers to arrive
                CUSTOMERS_SEM.acquire()

            if NUM_CUST == 0:
                print("No more customers :( \nBarberShop Closing!!...")
                break
                
            # semwait()
            MUTEX.acquire()

            if ( WAITING_CUSTS > 0 ):  
                WAITING_CUSTS-=1

            # semsignal()
            BARBER_SEM.release()  
            MUTEX.release()

            sp(random.choice([1,2,3]))

            # Barber starts cutting hair
            if (BARBER_CHAIR_CUST):
                self.cutHair()
                print(f"Barber - {BARBER_CHAIR_CUST}'s haircut has been done\n")
            MUTEX.acquire()

            if (len(WAITING_LIST) > 0 and  BARBER_CHAIR_CUST in WAITING_LIST):
                WAITING_LIST.remove(BARBER_CHAIR_CUST)  # remove customer from waiting list who have done with hair cut

            BARBER_CHAIR_CUST = ""  
            TOTAL -=1

            MUTEX.release()

    # customer getting haircut
    def cutHair(self):  
            print(f"Barber - {BARBER_CHAIR_CUST} is getting a haircut \n")
            sp(random.choice([1,2,3]))
            return

# A Customer Class to manage all customer functions

class Customer:
    def __init__(self,name):
        self.name = name
        
    def customerMain(self,name):

        global TOTAL, WAITING_CUSTS, SLEEPING , WAITING_LIST, BARBER_CHAIR_CUST , CHAIRS, NUM_CUST

        # Critical Section
        MUTEX.acquire()
        print(f"Customer - {self.name} arrived at the Barber Shop\n")

        # If Chairs Available
        if (WAITING_CUSTS < CHAIRS or TOTAL == 0): 
            if (TOTAL == 0):
                TOTAL += 1
                print(f"Customer - {self.name} has entered the Barber room \n")
            else:
                TOTAL+=1
                WAITING_CUSTS+=1
                WAITING_LIST.append(self.name)
                print(f"Customer - {self.name} has entered the waiting room\nTotal waiting customers are :", WAITING_CUSTS,"\n")

            CUSTOMERS_SEM.release() 
            MUTEX.release()      
            BARBER_SEM.acquire()

            if (SLEEPING): 
                print(f"Customer - {self.name} is waking up the barber \n")
                SLEEPING=False
            
            self.getHairCut(self.name)
            NUM_CUST -= 1
            BARBER_CHAIR_CUST = self.name

        else:
            NUM_CUST -= 1 
            MUTEX.release()
            # All chairs are occupied, customer leaves the shop
            self.balk(self.name)
              

        
    # customer called for a haircut        
    def getHairCut(self,name):   
        print(f"Customer - {name} has asked barber for haircut and entered the Barber room\n")
        return

    def balk(self,name):  # leave the shop
        print(f"Customer - {name} is trying to enter waiting room \n ")
        print(f"Customer - All chairs are occupied, {name} leaves the shop\n")
        

if __name__ == "__main__":
    bs = BarberShop()

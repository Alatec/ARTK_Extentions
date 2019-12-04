
#include <ARTK.h>

// these pins and interrupt numbers should work for UNO or MEGA
#define LED    13         // this pin has an LED on all Arduino boards
#define LED1    12         // this pin has an LED on all Arduino boards
#define INTPIN 2          // we'll use this pin to trigger an interrupt
#define INTNUM 0          // this is the corresponding interrupt number

void producer(), consumer(), myisr() ; //printer(), recurser(), 
void(* resetFunc) (void) = 0;
SEMAPHORE sem ;
long itime ;
unsigned int last_prime = 0;
double pi_approx = 0.0;

int sent_prime = 0;

int alg;

void Setup()
{

  // changing to large model, leaving default sleep timer interval (10 msec)
  // changing the memory model MUST be done before creating any tasks  
  ARTK_SetOptions(0,-1) ;

  // if an ISR that signals a semaphore is installed here, then the semaphore
  // should also be created here in case the ISR fires right away
  sem = ARTK_CreateSema(0) ;

  pinMode(LED, OUTPUT) ;                   // configure an output pin for the LED
  pinMode(INTPIN, OUTPUT) ;                // we'll trigger an interrupt with a high
  digitalWrite(INTPIN, HIGH) ;             // to low transition on an output pin
  // attachInterrupt(INTNUM, myisr, FALLING) ;
  
//  Printf("Hello from Setup (%u avail)\n", ARTK_EstAvailRam() ) ; 

  // create several tasks with varying priority and a default stack size of 256
  Printf("Init\n");
  while(last_prime == 0){
     if (Serial.available()>0)
    {      
      last_prime=(unsigned int)Serial.parseInt();
    }
  }
  Serial.flush();
  while(pi_approx == 0.0){
     if (Serial.available()>0)
    {      
      
      pi_approx=Serial.readString().toDouble();
      
   
    }
  }

  
    ARTK_CreateTask(producer, 2) ;
    ARTK_CreateTask(consumer, 3) ;
    // ARTK_CreateTask(finish, 1);
  
  
  
  


  

  
  Printf("Setup returning (%u avail)\n", ARTK_EstAvailRam() ) ; 
}

// this ISR also signals the producer/consumer semaphore
void myisr()
{
   itime = micros() ;
   ARTK_SignalSema(sem) ;
}

void producer()
{
//   Printf("Hello from task1\n") ;
  
  unsigned int next = 0;
  last_prime++;
  while (next == 0)
  {
      for (unsigned int i = 2; i < last_prime; i++)
      {
        if(last_prime % i == 0) break;
        else if (i == last_prime - 1)
        {
          next = i+1;

          Printf("prime: %u\n",last_prime);
          // sem = ARTK_CreateSema(0) ;
          ARTK_SignalSema(sem) ;
          // sent_prime = 1;
          // ARTK_Yield();
          break;
        } 
      }
      last_prime++;  
  }
    
  
}

void consumer()
{
  ARTK_WaitSema(sem);
  double val = 1.0;
  if(last_prime % 4 == 3){
    val = val - (1/(double)last_prime);
    Printf("p4=3\n");
  }else
  {
    val = val + (1/(double)last_prime);
    Printf("p4=1\n");
  }
  pi_approx = pi_approx * val;
  
  Printf("PI\n");
  double temp_pi = (1/pi_approx)*2;
  Serial.print( temp_pi, 9);
  Printf("\n");
  // Serial.print(String(String(pi_approx,9) + "\n"));
  ARTK_Yield();
  

  
  
}

void finish(){
//  Printf("Results: %d %d\n", task1_time, task2_time);
//  resetFunc();
}
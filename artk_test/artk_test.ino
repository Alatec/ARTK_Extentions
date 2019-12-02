
#include <ARTK.h>

// these pins and interrupt numbers should work for UNO or MEGA
#define LED    13         // this pin has an LED on all Arduino boards
#define LED1    12         // this pin has an LED on all Arduino boards
#define INTPIN 2          // we'll use this pin to trigger an interrupt
#define INTNUM 0          // this is the corresponding interrupt number

void task1(), task2(), myisr() ; //printer(), recurser(), 
void(* resetFunc) (void) = 0;
SEMAPHORE sem ;
long itime ;
signed int task1_time, task1_arrive;
signed int task2_time, task2_arrive;
signed int cpu_time = 0;
int alg;

void Setup()
{
  task1_time = 0;
  task2_time = 0;
  // changing to large model, leaving default sleep timer interval (10 msec)
  // changing the memory model MUST be done before creating any tasks  
  ARTK_SetOptions(0,-1) ;

  // if an ISR that signals a semaphore is installed here, then the semaphore
  // should also be created here in case the ISR fires right away
  sem = ARTK_CreateSema(0) ;

  pinMode(LED, OUTPUT) ;                   // configure an output pin for the LED
  pinMode(INTPIN, OUTPUT) ;                // we'll trigger an interrupt with a high
  digitalWrite(INTPIN, HIGH) ;             // to low transition on an output pin
  attachInterrupt(INTNUM, myisr, FALLING) ;
  
//  Printf("Hello from Setup (%u avail)\n", ARTK_EstAvailRam() ) ; 

  // create several tasks with varying priority and a default stack size of 256
  Printf("Init\n");
  while(task1_time == 0){
     if (Serial.available()>0)
    {      
      task1_time=Serial.parseInt();
      
   
  }
  }
  while(task2_time == 0){
     if (Serial.available()>0)
    {      
      task2_time=Serial.parseInt();
      
   
    }
  }

  
    ARTK_CreateTask(task1, 3) ;
    ARTK_CreateTask(task2, 3) ;
    ARTK_CreateTask(finish, 1);
  
  
  
  


  

  
  Printf("Setup returning (%u avail)\n", ARTK_EstAvailRam() ) ; 
}

// this ISR also signals the producer/consumer semaphore
void myisr()
{
   itime = micros() ;
   ARTK_SignalSema(sem) ;
}

void task1()
{
//   Printf("Hello from task1\n") ;
   
   // give a message every 80 msec, then sleep - blink the LED too
   Printf("Task1 size: %d\n",task1_time);
   while (task1_time > 0)
   {
        cpu_time++;
        task1_time--;
//      digitalWrite(LED, ~digitalRead(LED)) ;
//      Printf("Sleep %d\n", i) ; 

      if(task1_time > task2_time) ARTK_Yield() ;
   }
   task1_time = cpu_time;
   Printf("T1 %d\n", task1_time);
//   Printf("task exiting\n") ;
}

void task2()
{
//   Printf("Hello from task2\n") ;
   // give a message every 80 msec, then sleep - blink the LED too
   Printf("Task2 size: %d\n",task2_time);
   while (task2_time > 0)
   {
    cpu_time++;
    task2_time--;
//      digitalWrite(LED1, ~digitalRead(LED1)) ;
//      Printf("Sleep %d\n", i) ; 
  
      if(task2_time > task1_time) ARTK_Yield() ;
   }
   task2_time = cpu_time;
   Printf("T2 %d\n", task2_time);
//   Printf("task exiting\n") ;
}

void finish(){
//  Printf("Results: %d %d\n", task1_time, task2_time);
//  resetFunc();
}

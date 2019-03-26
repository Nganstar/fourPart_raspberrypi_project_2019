#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
pwm_led=GPIO.PWM(25,50)
pwm_led.start(100)
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

stepper_pins=[18,17,27,22]
GPIO.setup(stepper_pins,GPIO.OUT)
stepper_sequence=[]
stepper_sequence.append([GPIO.HIGH, GPIO.LOW, GPIO.LOW,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.HIGH, GPIO.LOW,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.HIGH,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.LOW,GPIO.HIGH])
z=0
speed=1.00
ROW=[5,6,13,19]
COL=[16,20,21]
MATRIX = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        ['*', 0, '#']]
for i in range(3):
        GPIO.setup(COL[i],GPIO.OUT)
        GPIO.output(COL[i],1)
for j in range(4):
        GPIO.setup(ROW[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
        # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance
x=1.00
if __name__ == '__main__':
    try:
        while True:
                z=0
                speed=1.00
                for i in range(3):
                        GPIO.output(COL[i],0)
                        for j in range(4):
                                if GPIO.input(ROW[j])==0:
                                        x=int( MATRIX[j][i])

                                        #time.sleep(1)
                                        while(GPIO.input(ROW[j])==0):
                                                pass
                        GPIO.output(COL[i],1)
                speed=0.03/x
                print(x)
                while z<10:
                        for row in stepper_sequence:
                                GPIO.output(stepper_pins,row)
                                time.sleep(speed)
                        z+=1
                dist = distance()
                print ("Measured Distance = %.1f cm" % dist)
                if(dist<10):
                        pwm_led.ChangeDutyCycle(dist*10)
                        print("TOO Close!!! STOP!")
                        break
                else:
                        pwm_led.ChangeDutyCycle(100)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()



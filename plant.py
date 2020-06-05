#Device Libraries
import sys
from gpiozero import LED, Button
from time import sleep

#PubNub
import pubnub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

#Pump is connected to GPIO4 as an LED
pump = LED(4)

#Soil Moisture sensor is connected to GPIO14 as a button
soil = Button(14)

#flag variable to toggle between Auto and Manual mode
flag = 1
# always make sure the program starts with the pump turned off
#conventions are backwards for pump  i.e. .on() =='off' and .off() == 'on$
pump.on()

class MySubscribeCallback(SubscribeCallback):
        def status(self,pubnub,status):
                pass
                # The status object returned is always related to subscribe but could contain
                # information about subscribe, heartbeat, or errors
                # use the operationType to switch on different options
                if status.operation == PNOperationType.PNSubscribeOperation \
                    or status.operation == PNOperationType.PNUnsubscribeOperation:
                    if status.category == PNStatusCategory.PNConnectedCategory:
                        pass
                    # This is expected for a subscribe, this means there is no error or issue
                    elif status.category == PNStatusCategory.PNReconnectedCategory:
                        pass
                    # This usually occurs if subscribe temporarily fails but reconnects. This means there was an error but there is no longer any issue
                    elif status.category == PNStatusCategory.PNDisconnectedCategory:
                        pass
                    # This is expected category for an unsubscribe. This means there was no error in unsubscribing from everything
                    elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                        pass
                    # This is usually an issue with the internet connection, this is an error, handle appropriately retry will be called
                    elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                        pass
                    # This means that PAM does allow this client to subscribe to this
                    # channel and channel group configuration. This is another explicit error
                    else:
                        pass
                    #This is usually an issue with the internet connection, this is an error, handle appropriately
                elif status.operation == PNOperationType.PNSubscribeOperation:
                    # Heartbeat operations can in fact have errors, so it is important to check first for an error.
                    if status.is_error():
                        pass
                    # There was an error with the heartbeat operation, handle here
                    else:
                        pass
                        # Heartbeat operation was successful
                else:
                    pass
                    # Encountered unknown status type

        def prescence(self, pubnub,prescence):
            pass # handle incoming prescence data

        def message(self, pubnub, message):
            global flag
            if message.message == 'ON':
                flag = 1
            elif message.message == 'OFF':
                flag = 0
            elif message.message == 'WATER':
                pump.off()
                sleep(5)
                pump.on()


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('ch1').execute()

def publish_callback(result, status):
    pass

def get_status():
    # Soil sensor acts as a button. is_held == sensor outputting a 1 for dryness
    if soil.is_held:
        print("dry")
        return True
    else:
        print("wet")
        return False
    
while True:
    if flag == 1:
        # auto mode to be implemented
        #DHT Sensor part ***************
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        # humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        # DHT_Read = ('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        # print(DHT_Read)
        # dictionary = {"eon": {"Temperature": temperature, "Humidity": humidity}}
		# pubnub.publish().channel('ch2').message([DHT_Read]).async(publish_callback)
		# pubnub.publish().channel("eon-chart").message(dictionary).async(publish_callback)
        wet = get_status()

        if wet == True:
            print("turning on")
            pump.off()
            sleep(5)
            print("pump turning off")
            pump.on()
            sleep(1)
        else:
            pump.on()
        sleep(1)
    elif flag == 0:
        # manual mode to be implemented make sure pump is always off
        pump.on()
        sleep(3)

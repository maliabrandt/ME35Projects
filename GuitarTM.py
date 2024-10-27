#Malia Brandt 
#For Musical Instrument Midterm October 2024
#This code is meant to run on the TM tab of the ME35 pyscript page. The teachable machines 
#detects the arrow pointing to either the standard tuning, capo on 3rd fret signs, and when 
#it is in the middle. 
from pyscript.js_modules import teach, pose, ble_library, mqtt_library
async def run_model(URL2):
    s = teach.s  
    s.URL2 = URL2
    await s.init()
def get_predictions(num_classes):
    predictions = []
    for i in range (0,num_classes):
        divElement = document.getElementById('class' + str(i))
        if divElement:
            divValue = divElement.innerHTML
            predictions.append(divValue)
    return predictions
#initialize mqtt stuff
mqtt_broker = 'broker.hivemq.com'
port = 1883
topic_sub = 'ME35-24/#'       
client = mqtt_library.myClient
print('Connected to %s MQTT broker' % (mqtt_broker))



#await run_model("https://teachablemachine.withgoogle.com/models/vNJV8BXJ-/") 
await run_model("https://teachablemachine.withgoogle.com/models/TgDcKdXX8/")
topic_pub = 'ME35-24/Malia'
while True:
    predictions = get_predictions(3)
    values = [float(item.split(': ')[1]) for item in predictions]
    print(values)
    if values[0] >= 0.80:
        client.publish("ME35-24/Malia", "Capo")
    elif values[2] >= 0.80:
        client.publish("ME35-24/Malia", "Standard")
    #else: send nothing

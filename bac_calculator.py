# import kivy module  
import kivy  
    
# this restricts the kivy version i.e  
# below this kivy version you cannot  
# use the app or software  
kivy.require("1.9.1")  
    
# base Class of your App inherits from the App class.  
# app:always refers to the instance of your application  
from kivy.app import App  
    
# creates the button in kivy  
# if not imported shows the error  
from kivy.uix.button import Button

from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
# BoxLayout arranges children in a vertical or horizontal box. 
# or help to put the children at the desired location. 
from kivy.uix.boxlayout import BoxLayout
#import mathematics module
import math

age_values = []
for i in range(17,120):
    age_values.append(i)

height_values = []
for i in range(100, 230):
    height_values.append(i)

weight_values = []
for i in range(50, 200):
    weight_values.append(i)

hour_values = []
am_pm_labels = []
for i in range(0,24):
    hour_values.append(i)

minute_values = []
for i in range(0,60,5):
    minute_values.append(i)

drink_values = []
for i in range(60):
    drink_values.append(i)

def is_it_a_number(string):
    answer = False
    digitcount = 0
    charactercount = 0
    decimalpointcount = 0
    negative = '-'
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    decimalpoint = '.'
    stringsize = len(string)

    for i in range(stringsize):
        for j in range(10):
            if string[i] == numbers[j]:
                digitcount += 1
        if string[i] == decimalpoint:
            decimalpointcount += 1
        if string[i] == negative:
            digitcount += 1

    digitcount = digitcount + decimalpointcount
    if digitcount == stringsize:
        answer = True

    return answer

def calculate_bac(height, weight, age, gender, stomach_status, hours_since_start_drinking, numdrinks, drink_volumes, alcohol_percentages):

    #Calculate body water content using gender, height, weight and age
     if gender == "MALE":
            total_body_water = 2.447 - 0.09156*age + 0.1074*height + 0.3362*weight
     else:
            total_body_water = -2.097 + 1.1069*height + 0.2466*weight
     #Calculate the Widmark coefficent (r) based on today body water and weight
     r = total_body_water/(0.844*weight)

     #Determine k based on whether stomach is full or empty
     if stomach_status == "FULL":
            k = 2.3
     else:
            k = 6.5
            
     alcohol_consumed = 0
     numdrinktypes = len(numdrinks)
     for i in range(numdrinktypes):
         alcohol_consumed = alcohol_consumed + numdrinks[i]*drink_volumes[i]*(alcohol_percentages[i]/100)

     #convert to grams using density of alcohol of 0.7892g/mL
     alcohol_consumed = alcohol_consumed*0.7892


     A = alcohol_consumed
     B = 0.016
     t = hours_since_start_drinking
     e = math.exp(-k*t)
     x = 1-e
     y = A*x
     z = y/(r*weight*1000)
     w = z*100
     j = B*t
     bac = w - j
        #bac = ((A*(1-e))/(r*weight*1000))*100 - (B*t)
     if bac < 0:
         bac = 0

     return bac, alcohol_consumed
    
# class in which we are creating the button by using boxlayout  
# defining the App class 
class BoxLayoutApp(App):  
        
    def build(self):

        MainBox = BoxLayout(orientation ='vertical')

        PersonalDetailsBox = BoxLayout(orientation ='horizontal', spacing=1, size_hint=(1,0.6))
        AgeBox = BoxLayout(orientation ='vertical')
   
        updownBox1 = BoxLayout(orientation ='horizontal')

        question_age = Label(text="Age:")
        question_age.bold = True
        age = TextInput(text ="21")
          
        btn1 = Button(text ="+", background_color = (0,1,0,1))
        btn1.bind(on_press=lambda a:self.go_up(age_values, age))
        btn2 = Button(text ="-", background_color = (1,0,0,1))
        btn2.bind(on_press=lambda a:self.go_down(age_values, age))

        updownBox1.add_widget(btn1) 
        updownBox1.add_widget(btn2)

        AgeBox.add_widget(question_age)
        AgeBox.add_widget(updownBox1)
        AgeBox.add_widget(age)
        
        
        #User height details
        HeightBox = BoxLayout(orientation ='vertical', spacing=1)
   
        updownBox2 = BoxLayout(orientation ='horizontal') 
          
        btn3 = Button(text ="+", background_color = (0,1,0,1))
        btn3.bind(on_press=lambda a:self.go_up(height_values, height))
        btn4 = Button(text ="-", background_color = (1,0,0,1))
        btn4.bind(on_press=lambda a:self.go_down(height_values, height))

        updownBox2.add_widget(btn3) 
        updownBox2.add_widget(btn4)

        question_height = Label(text="Height (cm):")
        question_height.bold = True
        height = TextInput(text ="180")

        HeightBox.add_widget(question_height)
        HeightBox.add_widget(updownBox2)
        HeightBox.add_widget(height)
        

        #User weight details
        WeightBox = BoxLayout(orientation ='vertical', spacing=1)
   
        updownBox3 = BoxLayout(orientation ='horizontal') 
          
        btn5 = Button(text ="+", background_color = (0,1,0,1))
        btn5.bind(on_press=lambda a:self.go_up(weight_values, weight))
        btn6 = Button(text ="-", background_color = (1,0,0,1))
        btn6.bind(on_press=lambda a:self.go_down(weight_values, weight))

        updownBox3.add_widget(btn5) 
        updownBox3.add_widget(btn6)

        question_weight = Label(text="Weight (kg):")
        question_weight.bold = True
        weight = TextInput(text ="75")

        WeightBox.add_widget(question_weight)
        WeightBox.add_widget(updownBox3)
        WeightBox.add_widget(weight)        

        GenderBox = BoxLayout(orientation ='vertical', spacing=1)
   
        updownBox_gender = BoxLayout(orientation ='horizontal') 
          
        btn_m = Button(text ="M", background_color = (0,0.7,1,1))
        btn_m.bind(on_press=lambda a:self.go_male(gender))
        btn_f = Button(text ="F", background_color = (1,0.5,1,1))
        btn_f.bind(on_press=lambda a:self.go_female(gender))

        updownBox_gender.add_widget(btn_m) 
        updownBox_gender.add_widget(btn_f)

        question_gender = Label(text="Gender:")
        question_gender.bold = True
        gender = Label(text ="MALE")

        GenderBox.add_widget(question_gender)
        GenderBox.add_widget(updownBox_gender)
        GenderBox.add_widget(gender)

        StomachDetailsBox = BoxLayout(orientation ='horizontal', spacing=1, size_hint=(1,0.2))
        question_stomach = Label(text="Stomach:", size_hint=(0.4,1))
        stomach = Label(text ="EMPTY", size_hint=(0.2,1))
        btn_full = Button(text ="FULL", background_color = (0,0.7,1,1), size_hint=(0.2,1))
        btn_full.bind(on_press=lambda a:self.i_am_full(stomach))
        btn_empty = Button(text ="EMPTY", background_color = (1,0.5,1,1), size_hint=(0.2,1))
        btn_empty.bind(on_press=lambda a:self.i_am_empty(stomach))
        StomachDetailsBox.add_widget(question_stomach)
        StomachDetailsBox.add_widget(btn_full)
        StomachDetailsBox.add_widget(btn_empty)
        StomachDetailsBox.add_widget(stomach)

        PersonalDetailsBox.add_widget(AgeBox)
        PersonalDetailsBox.add_widget(HeightBox)
        PersonalDetailsBox.add_widget(WeightBox)
        PersonalDetailsBox.add_widget(GenderBox)       

        TimeDetailsBox = BoxLayout(orientation ='horizontal', spacing=1, size_hint=(1,0.6))
        StartBox = BoxLayout(orientation = 'vertical')
        StartButtonBox = BoxLayout(orientation = 'horizontal')
        
        updownBoxstarthr = BoxLayout(orientation ='horizontal')
        updownBoxstartmin = BoxLayout(orientation ='horizontal')
	
        question_start = Label(text="Time you started drinking:")
        question_start.bold = True
##        start_hour = Label(text ="6")
##        start_minute = Label(text ="30")
##        punctuation_time = Label(text =":")
        start_time = Label(text="6:30")
          
        btn7 = Button(text ="H+", background_color = (0,1,0,1))
        btn7.bind(on_press=lambda a:self.go_up_time(hour_values, start_time, "hour"))
        btn8 = Button(text ="H-", background_color = (1,0,0,1))
        btn8.bind(on_press=lambda a:self.go_down_time(hour_values, start_time, "hour"))

        updownBoxstarthr.add_widget(btn7) 
        updownBoxstarthr.add_widget(btn8)

        btn9 = Button(text ="M+", background_color = (0,1,0,1))
        btn9.bind(on_press=lambda a:self.go_up_time(minute_values, start_time, "minute"))
        btn10 = Button(text ="M-", background_color = (1,0,0,1))
        btn10.bind(on_press=lambda a:self.go_down_time(minute_values, start_time, "minute"))

        updownBoxstartmin.add_widget(btn9)
        updownBoxstartmin.add_widget(btn10)

        StartButtonBox.add_widget(updownBoxstarthr)
        StartButtonBox.add_widget(updownBoxstartmin)
        
        StartBox.add_widget(question_start)
        StartBox.add_widget(StartButtonBox)
        StartBox.add_widget(start_time)

        #Current time details
        CurrentBox = BoxLayout(orientation ='vertical')
        CurrentButtonBox = BoxLayout(orientation ='horizontal')
   
        updownBoxcurrenthr = BoxLayout(orientation ='horizontal')
        updownBoxcurrentmin = BoxLayout(orientation ='horizontal')
	
        question_current = Label(text="Time it is now:")
        question_current.bold = True
##        current_hour = Label(text ="6")
##        current_minute = Label(text ="30")
##        punctuation_time2 = Label(text =":")
        current_time = Label(text="6:30")
          
        btn11 = Button(text ="H+", background_color = (0,1,0,1))
        btn11.bind(on_press=lambda a:self.go_up_time(hour_values, current_time, "hour"))
        btn12 = Button(text ="H-", background_color = (1,0,0,1))
        btn12.bind(on_press=lambda a:self.go_down_time(hour_values, current_time, "hour"))

        updownBoxcurrenthr.add_widget(btn11) 
        updownBoxcurrenthr.add_widget(btn12)

        btn13 = Button(text ="M+", background_color = (0,1,0,1))
        btn13.bind(on_press=lambda a:self.go_up_time(minute_values, current_time, "minute"))
        btn14 = Button(text ="M-", background_color = (1,0,0,1))
        btn14.bind(on_press=lambda a:self.go_down_time(minute_values, current_time, "minute"))

        updownBoxcurrentmin.add_widget(btn13)
        updownBoxcurrentmin.add_widget(btn14)

        CurrentButtonBox.add_widget(updownBoxcurrenthr)
        CurrentButtonBox.add_widget(updownBoxcurrentmin)

        CurrentBox.add_widget(question_current)
        CurrentBox.add_widget(CurrentButtonBox)
        CurrentBox.add_widget(current_time)
        


        #Put time details together
        TimeDetailsBox.add_widget(StartBox)
        TimeDetailsBox.add_widget(CurrentBox)


        DrinkDetailsBox = BoxLayout(orientation ='vertical', spacing=1, size_hint=(1,1))
        DrinkDetailsLabelsBox = BoxLayout(orientation ='horizontal')
        DrinkInputBox = BoxLayout(orientation ='horizontal')
        details_label = Label(text = 'No drinks entered')
        
        DrinkDetailsBox.add_widget(details_label)

        BACResultsBox = BoxLayout(orientation = 'vertical', spacing=1, size_hint=(1,0.7))
        ADLabel = Label(text = "Alcohol digested: ")
        ARLabel = Label(text = "Alcohol remaining: ")
        BACLabel = Label(text = "Your BAC is 0")
        BACbtn = Button(text = "Calculate BAC", background_color = (1,1,0,0.5))
        BACbtn.bind(on_press=lambda a:self.update_bac(details_label, BACLabel, ADLabel, ARLabel, TimeToSober, age, height, weight, gender, stomach, start_time, current_time))
        TimeToSober = Label(text = "Time to 0.05: ")

        ADARBox = BoxLayout(orientation ='horizontal')
        ADARBox.add_widget(ADLabel)
        ADARBox.add_widget(ARLabel)
        
        BACResultsBox.add_widget(BACbtn)
        BACResultsBox.add_widget(ADARBox)
        BACResultsBox.add_widget(BACLabel)
        BACResultsBox.add_widget(TimeToSober)

        DrinkQuestionOneBox = BoxLayout(orientation ='horizontal')
        DrinkQuestionTwoBox = BoxLayout(orientation ='horizontal')
        DrinkQuestionThreeBox = BoxLayout(orientation ='horizontal')

        updownBox8 = BoxLayout(orientation = 'vertical')

        numdrinks_question = Label(text = "Number of\n drinks")
        DrinkDetailsLabelsBox.add_widget(numdrinks_question)
        NumberOfDrinks = Label(text = "0")
        btn15 = Button(text = "+", background_color = (0,1,0,1))
        btn15.bind(on_press=lambda a:self.go_up(drink_values, NumberOfDrinks))
        btn16 = Button(text ="-", background_color = (1,0,0,1))
        btn16.bind(on_press=lambda a:self.go_down(drink_values, NumberOfDrinks))

        drink_volume_q = Label(text="Volume of\n each drink(ml):")
        volume = TextInput(text ="375")
        DrinkDetailsLabelsBox.add_widget(drink_volume_q)
        DrinkQuestionTwoBox.add_widget(volume)

        alcohol_content_q = Label(text="Alcohol content\n of each drink(%):")
        alc_cont = TextInput(text ="4.5")
        DrinkDetailsLabelsBox.add_widget(alcohol_content_q)
        DrinkQuestionThreeBox.add_widget(alc_cont)

        updownBox8.add_widget(btn15)
        updownBox8.add_widget(btn16)
        DrinkQuestionOneBox.add_widget(NumberOfDrinks)
        DrinkQuestionOneBox.add_widget(updownBox8)

        add_drink_btn = Button(text = "Add drink")
        add_drink_btn.bind(on_press=lambda a:self.print_drink_info(details_label, NumberOfDrinks, volume, alc_cont))

        clear_drinks_btn = Button(text = "Clear all drinks")
        clear_drinks_btn.bind(on_press=lambda a:self.clear_drink_info(details_label, ADLabel, ARLabel, BACLabel, TimeToSober))

        CalculateBox = BoxLayout(orientation ='horizontal')

        DrinkInputBox.add_widget(DrinkQuestionOneBox)
        DrinkInputBox.add_widget(DrinkQuestionTwoBox)
        DrinkInputBox.add_widget(DrinkQuestionThreeBox)
        DrinkDetailsBox.add_widget(DrinkDetailsLabelsBox)
        DrinkDetailsBox.add_widget(DrinkInputBox)
        CalculateBox.add_widget(add_drink_btn)
        CalculateBox.add_widget(clear_drinks_btn)
        DrinkDetailsBox.add_widget(CalculateBox)

        MainBox.add_widget(PersonalDetailsBox)
        MainBox.add_widget(StomachDetailsBox)
        MainBox.add_widget(TimeDetailsBox)
        MainBox.add_widget(DrinkDetailsBox)
        MainBox.add_widget(BACResultsBox)
     
        return MainBox

    def go_up(self, array, ltxt):
        n = 0
        num_values = len(array)
        ltxtv = ltxt.text
        if is_it_a_number(ltxtv) == False:
            new_value = min(array)
            ltxt.text = str(new_value)
        else:
            ltxtv = float(ltxtv)
            ltxtv = int(ltxtv)
            if ltxtv < min(array):
                new_value = min(array)
            elif ltxtv > max(array):
                new_value = max(array)
            else:             
                if ltxtv < 0:
                    ltxtv = 0 - ltxtv
                for i in range(num_values):
                    if array[i] == ltxtv:
                        n = i
                nplus = n + 1
                if nplus > (len(array) - 1):
                    nplus = 0
                new_value = array[nplus]
            ltxt.text = str(new_value)

    def go_down(self, array, ltxt):
        n = 0
        num_values = len(array)
        ltxtv = ltxt.text
        if is_it_a_number(ltxtv) == False:
            new_value = min(array)
            ltxt.text = str(new_value)
        else:
            ltxtv = float(ltxtv)
            ltxtv = int(ltxtv)
            if ltxtv < min(array):
                new_value = min(array)
            elif ltxtv > max(array):
                new_value = max(array)
            else:
                if ltxtv < 0:
                    ltxtv = 0 - ltxtv
                for i in range(num_values):
                    if array[i] == ltxtv:
                        n = i
                nminus = n - 1
                if nminus < 0:
                    nminus = len(array) - 1
                new_value = array[nminus]
            ltxt.text = str(new_value)
            
    def go_up_time(self, array, ltxt, minute_or_hour):
        n = 0
        num_values = len(array)
        ltxtv = ltxt.text
        time_array = ltxtv.split(":")
        if minute_or_hour == "hour":
            val = int(time_array[0])
            x = 0
        else:
            val = int(time_array[1])
            x = 1
        if val < min(array):
            new_val = min(array)
        elif val > max(array):
            new_val = max(array)
        else:
            for i in range(num_values):
                if array[i] == val:
                    n = i
            nplus = n + 1
            if nplus > len(array) - 1:
                nplus = 0
            new_val = array[nplus]
        time_array[x] = str(new_val)
        if time_array[1] == "5" or time_array[1] == "0":            
            ltxt.text = str(time_array[0]) + ":0" + str(time_array[1])
        else:
            ltxt.text = str(time_array[0]) + ":" + str(time_array[1])

    def go_down_time(self, array, ltxt, minute_or_hour):
        n = 0
        num_values = len(array)
        ltxtv = ltxt.text
        time_array = ltxtv.split(":")
        if minute_or_hour == "hour":
            val = int(time_array[0])
            x = 0
        else:
            val = int(time_array[1])
            x = 1
        if val < min(array):
            new_val = min(array)
        elif val > max(array):
            new_val = max(array)
        else:
            for i in range(num_values):
                if array[i] == val:
                    n = i
            nminus = n - 1
            if nminus < 0:
                nminus = len(array) - 1
            new_val = array[nminus]
        time_array[x] = str(new_val)
        if time_array[1] == "5" or time_array[1] == "0":            
            ltxt.text = str(time_array[0]) + ":0" + str(time_array[1])
        else:
            ltxt.text = str(time_array[0]) + ":" + str(time_array[1])

    def go_male(self, ltxt):           
        ltxt.text = "MALE"

    def go_female(self, ltxt):
        ltxt.text = "FEMALE"

    def i_am_full(self, ltxt):           
        ltxt.text = "FULL"

    def i_am_empty(self, ltxt):
        ltxt.text = "EMPTY"

    def clear_drink_info(self, details_label, ADLabel, ARLabel, BACLabel, TimeToSober):
        details_label.text = "No drinks entered"
        ADLabel.text = "Alcohol digested: "
        ARLabel.text = "Alcohol remaining: "
        BACLabel.text = "Your BAC is 0"
        TimeToSober.text = "Time to 0.05: "

    def print_drink_info(self, details_label, NumberOfDrinks, volume, alc_cont):
        d_text = details_label.text
        if (d_text == "No drinks entered") or (d_text == "Entered numbers must be zero or more!"):
            total_number_drinks = 0
            combined_volume = 0
            average_content = 0
        else:
            s = []
            for t in d_text.split():
                try:
                    s.append(float(t))
                except ValueError:
                    pass
            total_number_drinks = s[0]
            combined_volume = s[1]
            average_content = s[2]

        n = int(NumberOfDrinks.text)
        ac = alc_cont.text 
        v = volume.text
        truecount = 0
        
        if is_it_a_number(ac) == True:
            truecount += 1
        if is_it_a_number(v) == True:
            truecount += 1
        if float(ac) > 0:
            truecount += 1
        if float(v) > 0:
            truecount += 1
        
        if  truecount < 4:
            details_label.text = "Entered numbers must be zero or more!"
        else:
            volume = int(volume.text)
            alc_cont = float(alc_cont.text)
            combined_volume += (volume*n)/1000
            average_content = ((average_content*total_number_drinks) + (alc_cont*n))/(total_number_drinks+n)
            average_content = round(average_content,2)
            total_number_drinks += n
            details_label.text = str(total_number_drinks) + " drinks, total volume consumed: " + str(combined_volume) + " L,\n average alcohol %: " + str(average_content)
        
    def update_bac(self, details_label, BACLabel, ADLabel, ARLabel, TimeToSober, age, height, weight, gender, stomach, start_time, current_time):

        age = age.text
        height = height.text
        weight = weight.text
        gender = gender.text

        truecount = 0
        if details_label.text != "Entered numbers must be zero or more!":
            truecount += 1
        if details_label.text != "No drinks entered":
            truecount += 1
        if is_it_a_number(age) == True:
            truecount += 1
        if is_it_a_number(height) == True:
            truecount += 1
        if is_it_a_number(weight) == True:
            truecount += 1
        age = float(age)
        height = float(height)
        weight = float(weight)
        if int(age) > 0:
            truecount += 1
        if int(height) > 0:
            truecount += 1
        if int(weight) > 0:
            truecount += 1

        if truecount < 7:
            BACLabel.text = "Can't calculate BAC!"
            ADLabel.text = "NA"
            ARLabel.text = "NA"
            TimeToSober.text = "NA"
        else:
            age = int(age)
            height = int(height)
            weight = int(weight)
            start_time = start_time.text
            start_time_array = start_time.split(":")
            start_hour = int(start_time_array[0])
            start_minute = int(start_time_array[1])
            
            current_time = current_time.text
            current_time_array = current_time.split(":")
            current_hour = int(current_time_array[0])
            current_minute = int(current_time_array[1])

            hours_elapsed = current_hour - start_hour
            if hours_elapsed < 0:
                hours_elapsed = (24-start_hour) + current_hour

            current_residual_hour = current_minute/60
            start_residual_hour = start_minute/60

            time_elapsed = hours_elapsed + current_residual_hour - start_residual_hour
            #print(time_elapsed)

            text_to_extract = details_label.text
            #print(text_to_extract.split())

            s = []
            for t in text_to_extract.split():
                try:
                    s.append(float(t))
                except ValueError:
                    pass
            #print(s)
            hours_since_start_drinking = time_elapsed
            stomach_status = stomach.text
            numdrinks = [1]
            drink_volumes = []
            drink_volumes.append(s[1]*1000)
            alcohol_percentages = [s[2]]

            bac, alcoholconsumed = calculate_bac(height, weight, age, gender, stomach_status, hours_since_start_drinking, numdrinks, drink_volumes, alcohol_percentages)
            
            tts = 0
            bac_sober = bac
            if bac_sober > 0.05:
                while bac_sober >= 0.05:
                    hours_elapsed = hours_since_start_drinking + tts
                    bac_sober, alcoholconsumed = calculate_bac(height, weight, age, gender, stomach_status, hours_elapsed, numdrinks, drink_volumes, alcohol_percentages)
                    tts += 0.05
                    #print(bac_sober)
                time_to_sober = tts
            else:
                time_to_sober = 0
                
            alcohol_ingested = 10*hours_since_start_drinking
            alcohol_remaining = alcoholconsumed - alcohol_ingested
            if alcohol_remaining < 0:
                alcohol_ingested = alcoholconsumed
                alcohol_remaining = 0
            alcohol_ingested = round(alcohol_ingested, 2)
            ADLabel.text = 'Alcohol digested: ' + str(alcohol_ingested) + "ml"
            alcohol_remaining = round(alcohol_remaining, 2)
            ARLabel.text = 'Alcohol remaining: ' + str(alcohol_remaining) + "ml"
            bac = round(bac, 3)

            if bac >= 0.05:
                BACLabel.text = 'Your BAC is ' + str(bac)
                BACLabel.color = (1,0,0,1)
                BACLabel.bold = True
            else:
                BACLabel.text = 'Your BAC is ' + str(bac)
                BACLabel.color = (0,1,0,1)
                BACLabel.bold = True

            #print(time_to_sober)
            if time_to_sober == 0:
                hours_to_sober = 0
                minutes_to_sober = 0
                TimeToSober.text = "You can drive now!"
                TimeToSober.color = (0,1,0,1)
                TimeToSober.bold = True
            else:
                hours_to_sober = int(time_to_sober)
                r = (time_to_sober - hours_to_sober)*60
                minutes_to_sober = int(r)
                if hours_to_sober == 1:
                    TimeToSober.text =  "To drive, wait for approximately " + str(hours_to_sober) + " hour and " + str(minutes_to_sober) + " minutes!"
                elif hours_to_sober == 1 and minutes_to_sober == 1:
                    TimeToSober.text =  "To drive, wait for approximately " + str(hours_to_sober) + " hour and " + str(minutes_to_sober) + " minute!"
                elif minutes_to_sober == 0:
                    TimeToSober.text =  "To drive, wait for approximately " + str(hours_to_sober) + " hours"
                elif minutes_to_sober == 0 and hours_to_sober == 1:
                    TimeToSober.text =  "To drive, wait for approximately " + str(hours_to_sober) + " hour"
                elif hours_to_sober == 0:
                    TimeToSober.text =  "To drive, wait for approximately " + str(minutes_to_sober) + " minutes!"
                elif hours_to_sober == 0 and minutes_to_sober == 1:
                    TimeToSober.text =  "To drive, wait for approximately " + str(minutes_to_sober) + " minute!"
                else:
                    TimeToSober.text =  "To drive, wait for approximately " + str(hours_to_sober) + " hours and " + str(minutes_to_sober) + " minutes!"
                TimeToSober.color = (1,0,0,1)
                TimeToSober.bold = True
                
# creating the object root for BoxLayoutApp() class   
root = BoxLayoutApp()  
    
# run function runs the whole program  
# i.e run() method which calls the  
# target function passed to the constructor.  
root.run() 

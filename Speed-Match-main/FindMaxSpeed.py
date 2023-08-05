
#Thomas Add Comments here about what your finding max speed script does.  Feel free to copy/paste from mine if you need info.
#This a quick script to determine what the top speed of a Loc is.
#This can also be used to validate your speed script hardware setup.
#
#In the full speed script, if you set the top speed too high, the script may run for some time (10-15 minutes) before you find out that Loc cannot reach the target speed.

#You should start the system console or script output before running this script. The status messages and final speed result will show there.

# Eric Bradford 3/9/3013
# Thomas Stpehens 3/10/2013
# thomas stephens 1/3/2016


#--------------------------------------------------------------- 
import java
import javax.swing
import jmri

class AutoSpeedTable(jmri.jmrit.automat.AbstractAutomaton) :


    # individual block section length (scale feet)
    blockN = float(133)  # 132.5778 feet  Phil's test track
    blockHO = float(62)  #  61.6264 feet  Phil's test track, Kato track

#	blockN = float(108)  # 108.?    feet  Kent's test track
#   blockHO = float(65)  #  65.312  feet  Kent's test track

#   blockHO = float(123)  #  123.2528 feet per two track sections TeamDigital
#   numBlocksHO = float(8) #  for TeamDigital

    long = False
# +++ TLS 3/17/12 more test numbers. was 5. Compensate for odd values on specific track sections
    countsensor = 7	# Use 1 for testing and 6 for running
# --- TLS

    # init() is called exactly once at the beginning to do
    # any necessary configuration.
    def init(self):

        self.sensor1 = sensors.provideSensor("CS1")
        self.sensor2 = sensors.provideSensor("CS2")
        self.sensor3 = sensors.provideSensor("CS3")
        self.sensor4 = sensors.provideSensor("CS4")
        self.sensor5 = sensors.provideSensor("CS5")
        self.sensor6 = sensors.provideSensor("CS6")
        self.sensor7 = sensors.provideSensor("CS7")
        self.sensor8 = sensors.provideSensor("CS8")
        self.sensor9 = sensors.provideSensor("CS9")
        self.sensor10 = sensors.provideSensor("CS10")
        self.sensor11 = sensors.provideSensor("CS11")
        self.sensor12 = sensors.provideSensor("CS12")
        self.sensor13 = sensors.provideSensor("CS13")
        self.sensor14 = sensors.provideSensor("CS14")
        self.sensor15 = sensors.provideSensor("CS15")
        self.sensor16 = sensors.provideSensor("CS16")

        self.memory1 = memories.provideMemory("1")
        self.memory2 = memories.provideMemory("2")
        self.memory3 = memories.provideMemory("3")
        self.memory4 = memories.provideMemory("4")
        self.memory5 = memories.provideMemory("5")
        self.memory6 = memories.provideMemory("6")
        self.memory7 = memories.provideMemory("7")
        self.memory8 = memories.provideMemory("8")
        self.memory9 = memories.provideMemory("9")
        self.memory10 = memories.provideMemory("10")
        self.memory11 = memories.provideMemory("11")
        self.memory12 = memories.provideMemory("12")
        self.memory13 = memories.provideMemory("13")
        self.memory14 = memories.provideMemory("14")
        self.memory15 = memories.provideMemory("15")
        self.memory16 = memories.provideMemory("16")
        self.memory20 = memories.provideMemory("20")
        self.memory21 = memories.provideMemory("21")
        self.memory22 = memories.provideMemory("22")
        self.memory23 = memories.provideMemory("23")
        self.memory24 = memories.provideMemory("24")
        self.memory25 = memories.provideMemory("25")

# Getting throttle

        self.status.text = "Getting throttle"

        dccnumber = int(self.dccaddress.text)   #EWB -- Used for file naming confusion and text file information
        if (dccnumber > 127) :
             self.long = True
        else :
             self.long = False
        self.throttle = self.getThrottle(dccnumber, self.long)
        if (self.throttle == None) :
             print "Couldn't assign throttle!"
        else :
            print
            print
            print
            print "Testing Locomotive with DCC Address",dccnumber

# Getting Programmer
#0#08/24/22 updated java call
        # self.programmer = programmers.getAddressedProgrammer(self.long, dccnumber)  ## outdated
        self.programmer = addressedProgrammers.getAddressedProgrammer(self.long, dccnumber)     ## CA 2022-08-19

        return
#----------------------------------------------------------------
    def measuretime(self,sensorlist,blocklength,starttime,stoptime) :

        """Measures the time between virtual blocks"""
        if starttime == 0 :
            self.waitChange(sensorlist)
            self.waitSensorActive(sensorlist)
            stoptime = java.lang.System.currentTimeMillis()	

        starttime = stoptime

        self.waitChange(sensorlist)
        self.waitChange(sensorlist)
        self.waitSensorActive(sensorlist)

        stoptime = java.lang.System.currentTimeMillis()
        runtime = stoptime - starttime
        return runtime, starttime, stoptime
#---------------------------------------------------------------
    def getspeed(self,targetspeed,block) :
        """converts time to speed, ft/sec - scale speed"""
        starttime = stoptime = 0	# Needed when using every block
        self.memory24.value = str(targetspeed)

        speedlist = []	# Clear Speedlist (speed list contains measured speeds for each run)

        for z in range(1,self.countsensor + 1) : # make <countsensor> speed measurements
            if int(targetspeed) >= 125 : #Used for determining max forward and reverse speeds
                if block == 133 :
                    blocklength = block * 12	# Phil's N scale loop has 12 blocks
                elif block == 123 :
                    blocklength = block * 8		# Bill's Ho scale loop has 8 blocks
                else :
                    blocklength = block * 16	# All other's have 16 blocks

                duration, starttime, stoptime = self.measuretime([self.sensor1],blocklength,starttime,stoptime)
            
                        
            if duration == 0 :
                print "Measurement #",z," duration = ",duration
                z = z - 1
                print "got a zero for duration" # this has occured when using a MS100
                print "        Measurement #",z
            else :

                speed = (blocklength / (duration / 1000.0)) * (3600.0 / 5280)	
                speedlist.append(speed)

                print "Measured Speed MPH =",round(speed,1) , " Measurement #",z
                self.status.text = "Measured Speed = " + str(round(speed,1)) + " MPH"

                if self.sensor1.knownState==ACTIVE:
                    self.memory1.value = str(round(speed))
                    self.memory7.value = " "
                    self.memory6.value = " "
                    print "[Block 1]"
                elif self.sensor2.knownState==ACTIVE:
                    self.memory2.value = str(round(speed))
                    self.memory8.value = " "
                    self.memory7.value = " "
                    print "[Block 2]"
                elif self.sensor3.knownState==ACTIVE:
                    self.memory3.value = str(round(speed)) 
                    self.memory9.value = " "
                    self.memory8.value = " "
                    print "[Block 3]"
                elif self.sensor4.knownState==ACTIVE:
                    self.memory4.value = str(round(speed)) 
                    self.memory10.value = " "
                    self.memory9.value = " "
                    print "[Block 4]"
                elif self.sensor5.knownState==ACTIVE:
                    self.memory5.value = str(round(speed)) 
                    self.memory11.value = " "
                    self.memory10.value = " "
                    print "[Block 5]"
                elif self.sensor6.knownState==ACTIVE:
                    self.memory6.value = str(round(speed)) 
                    self.memory12.value = " "
                    self.memory11.value = " "
                    print "[Block 6]"
                elif self.sensor7.knownState==ACTIVE:
                    self.memory7.value = str(round(speed)) 
                    self.memory1.value = " "
                    self.memory12.value = " "
                    print "[Block 7]"
                elif self.sensor8.knownState==ACTIVE:
                    self.memory8.value = str(round(speed)) 
                    self.memory2.value = " "
                    self.memory1.value = " "
                    print "[Block 8]"
                elif self.sensor9.knownState==ACTIVE:
                    self.memory9.value = str(round(speed)) 
                    self.memory3.value = " "
                    self.memory2.value = " "
                    print "[Block 9]"
                elif self.sensor10.knownState==ACTIVE:
                    self.memory10.value = str(round(speed)) 
                    self.memory4.value = " "
                    self.memory3.value = " "
                    print "[Block 10]"
                elif self.sensor11.knownState==ACTIVE:
                    self.memory11.value = str(round(speed)) 
                    self.memory5.value = " "
                    self.memory4.value = " "
                    print "[Block 11]"
                elif self.sensor12.knownState==ACTIVE:
                    self.memory12.value = str(round(speed)) 
                    self.memory6.value = " "
                    self.memory5.value = " "
                    print "[Block 12]"
                elif self.sensor13.knownState==ACTIVE:
                    self.memory13.value = str(round(speed)) 
                    self.memory7.value = " "
                    self.memory6.value = " "
                    print "[Block 13]"
                elif self.sensor14.knownState==ACTIVE:
                    self.memory14.value = str(round(speed)) 
                    self.memory8.value = " "
                    self.memory7.value = " "
                    print "[Block 14]"
                elif self.sensor15.knownState==ACTIVE:
                    self.memory15.value = str(round(speed)) 
                    self.memory9.value = " "
                    self.memory8.value = " "
                    print "[Block 15]"
                elif self.sensor16.knownState==ACTIVE:
                    self.memory16.value = str(round(speed)) 
                    self.memory10.value = " "
                    self.memory9.value = " "
                    print "[Block 16]"


        # EWB-- select the median from the list and use it as the measured speed speedlist.sort() 
        #EWB-- sorts the <countsensor> measurements from smallest to largest speed = speedlist.pop(3) 
        #EWB-- Chooses (numbered entry) in sorted "speedlist" set above NOT including first entry
        #EWB --Previous number was not choosing correct median value for set of measurements.

        return speed
#---------------------------------------------------------------

# handle() will only execute once here, to run a single test
#EWB -- Any "print" command starting from here will show up in the JMRI Sysem Console screen ("Help Tab" then "System console")
#TLS -- Will also show in script output screen. ("Panels" then "script output")
    def handle(self):
    
        print "Determining Maximum Speeds"

        self.status.text = "Locomotive Setup"
        self.memory25.value = "Preparing Locomotive for speed measurements"

#09/11/09
        # jmri.InstanceManager.powerManagerInstance().setPower(jmri.PowerManager.OFF)
        jmri.InstanceManager.getDefault(jmri.PowerManager).setPower(jmri.PowerManager.OFF)  ## CA 2022-08-19
        self.waitMsec(1000)
        # jmri.InstanceManager.powerManagerInstance().setPower(jmri.PowerManager.ON)
        jmri.InstanceManager.getDefault(jmri.PowerManager).setPower(jmri.PowerManager.ON)  ## CA 2022-08-19
        self.waitMsec(1000)
        self.throttle.speedSetting = 0.
        self.waitMsec(500)
        starttesttime = java.lang.System.currentTimeMillis()
        badlocomotive = False # will be true if locomotive will not go slow enough

        self.memory1.value = " "
        self.memory2.value = " "
        self.memory3.value = " "
        self.memory4.value = " "
        self.memory5.value = " "
        self.memory6.value = " "
        self.memory7.value = " "
        self.memory8.value = " "
        self.memory9.value = " "
        self.memory10.value = " "
        self.memory11.value = " "
        self.memory12.value = " "
        self.memory13.value = " "
        self.memory14.value = " "
        self.memory15.value = " "
        self.memory16.value = " "



        if self.Scale.getSelectedItem() == "N Scale" :
            block = self.blockN
        if self.Scale.getSelectedItem() == "HO Scale" :
            block = self.blockHO

        else :
            # if user forgets to click a scale button, then it's N scale
            block = self.blockN

        print self.Scale.getSelectedItem()
        print "Type of locomotive being tested is",self.Locomotive.getSelectedItem()
        print "-----"
        print "-----\n"
 
 #TLS 3/10/12 Disabled all CV writes. Testing Loc as-is. Expectation that Loc will be setup for everything except speed before running this script.
 # Expectation is that Loc will be returned to current state after speed matching, with only the speed settings altered from the script.

        # This will change FX Rate and Keep Alive on Digitrax Decoders
        # This will change Random Sound Max on ESU LokSound Decoders
# 08/25/08
# 09/22/08
#		if self.DecoderBrand == "QSI-BLI" :
#			self.programmer.writeCV(62, 0, None) # Turn off verbal reporting on QSI decoders
#			self.waitMsec(1000)
#
#		if self.DecoderBrand == "Digitrax" :
#			self.programmer.writeCV(57, 0, None) # Turn OFF Back EMF as per note above.
#			self.waitMsec(1000)
#			
#			self.programmer.writeCV(25, 0, None) # Turn off manufacture defined speed tables
#		self.waitMsec(750)
#
#		if self.long == True :			#turn off speed tables
#			self.programmer.writeCV(29, 34, None)
#		else:
#			self.programmer.writeCV(29, 2, None)
#
#		self.waitMsec(500)
#		#self.programmer.writeCV(2, 0, None)	#Start Voltage off (EWB--CV not changed due to high max forward/reverse speeds measured.  speeds > 225mph!)
#		#self.waitMsec(500)
#		self.programmer.writeCV(3, 0, None)	#Acceleration off
#		self.waitMsec(500)
#		self.programmer.writeCV(4, 0, None)	#Deceleration off
#		self.waitMsec(500)
#		self.programmer.writeCV(19, 0, None)	#Clear consist
#		self.waitMsec(500)
#		#self.programmer.writeCV(5, 0, None)	#Maximum Voltage off  (EWB--CV not changed due to high max forward/reverse speeds measured.  speeds > 225mph!)
#		#self.waitMsec(500)
#		#self.programmer.writeCV(6, 0, None)	#Mid Point Voltage off  (EWB--CV not changed due to high max forward/reverse speeds measured.  speeds > 225mph!)
#		#self.waitMsec(500)
#		self.programmer.writeCV(66, 0, None) #Turn off Forward Trim
#		self.waitMsec(500)
#		self.programmer.writeCV(95, 0, None) #Turn off reverse Trim
#		self.waitMsec(500)
#
        # Run Locomotive for 5 laps each direction to warm it up

        self.memory25.value = "Warming up Locomotive"
        self.status.text = "Warming up Locomotive"
        print
        print "Warming up Locomotive"
        print
        self.throttle.setIsForward(True)
        self.memory20.value = "Forward"

        self.throttle.setF0(True)
        self.throttle.setF8(True)

        # Warm up locomotive for 5 laps forward

#01/09/09	TCS decoder would not move when setting throttle to 1.0
 
        self.throttle.speedSetting = .99
        self.waitMsec(250)
        self.throttle.speedSetting = 1.0

        for x in range (1, 5) :
            self.waitChange([self.sensor1])
            self.waitSensorActive(self.sensor1)

        self.throttle.speedSetting = 0.0
        self.waitMsec(2000)
        
        # Warm up 5 laps reverse

#05/21/10	Removed reverse warmup and max speed measurement for Steam

        if self.Locomotive.getSelectedItem() == "Diesel" :
            self.throttle.setIsForward(False)
            self.memory20.value = "Reverse"
            self.throttle.speedSetting = 1.0

            for x in range (1, 5) :
                self.waitChange([self.sensor1])
                self.waitSensorActive(self.sensor1)

        # Find maximum speed reverse

            self.memory25.value = "Finding Maximum Speeds"
            self.throttle.speedSetting = 1.0
            self.waitMsec(500)
            revmaxspeed = self.getspeed(125,block)
            print
            print "Reverse Max Speed = ",round(revmaxspeed), "MPH"
            print
            self.throttle.speedSetting = 0.0
            self.status.text = "Max Reverse Speed = " + str(int(revmaxspeed))
            
            #09/15/09
            self.waitMsec(3000)

#05/21/10
        else :
            revmaxspeed = 0
        
        self.memory21.value = str(int(revmaxspeed))

        # Find maximum speed forward
#09/18/09
        self.throttle.setIsForward(True)
        self.waitMsec(500)
        self.throttle.setIsForward(True)
        self.waitMsec(500)
        self.memory20.value = "Forward"
        self.throttle.speedSetting = 1.0
        self.waitMsec(1000)
        fwdmaxspeed = self.getspeed(125,block)
        print
        print "Forward Max Speed = ",round(fwdmaxspeed), "MPH"
        print
        self.throttle.speedSetting = 0.0
        self.status.text = "Max Forward Speed " + str(int(fwdmaxspeed))
        self.memory22.value = str(int(fwdmaxspeed))
        self.waitMsec(1000)
        
        self.status.text = "Done"
        self.throttle.setF8(False)
        self.throttle.setF0(False)
        endtesttime = java.lang.System.currentTimeMillis()
        print
        print "Test Time = ",((endtesttime - starttesttime) / 1000) / 60, " min."		#Displays time it took to complete the speedmatching of locomotive.

        # done!

        self.throttle.release()
        #re-enable button
        self.startButton.enabled = True
        # and stop


        # cycle track power because some Digitrax decoders don't stop

        jmri.InstanceManager.powerManagerInstance().setPower(jmri.PowerManager.OFF)
        self.waitMsec(2000)
        jmri.InstanceManager.powerManagerInstance().setPower(jmri.PowerManager.ON)
        self.memory25.value = "Done - Ready for next locomotive"


        return 0
#---------------------------------------------------------------
    # define what buttons do when clicked and attach that routine to the button
    def whenMyButtonClicked(self,event) :
        self.start()
        # we leave the button off
        self.startButton.enabled = False

        return
#---------------------------------------------------------------

    # routine to show the user input panel, starting the whole process
    # the panel collects the locomotive address, scale being used, and the decoder type if known
    def setup(self):

  #		DecoderList = ["Digitrax", "TCS", "NCE", "MRC", "QSI-BLI", "SoundtraxxDSD", "Lenz Gen 5", "ESU", "Atlas/Lenz XF", "Tsunami"] 

        # create a frame to hold the button, set up for nice layout
        f = javax.swing.JFrame("Finding Maxium Speed Input Panel")		# argument is the frames title
        f.setLocation(200,50)
        f.contentPane.setLayout(javax.swing.BoxLayout(f.contentPane, javax.swing.BoxLayout.Y_AXIS))

        # create the DCC text field
        self.dccaddress = javax.swing.JTextField(5)	# sized to hold 5 characters, initially empty

        # put the text field on a line preceded by a label
        temppanel1 = javax.swing.JPanel()
        temppanel1.add(javax.swing.JLabel("          DCC Address"))
        temppanel1.add(self.dccaddress)

                
        # create the start button
        self.startButton = javax.swing.JButton("Start")
        self.startButton.actionPerformed = self.whenMyButtonClicked

        self.status = javax.swing.JLabel("Enter DCC Address and press Start")
        
        self.Scale = javax.swing.JComboBox()
        self.Scale.addItem("HO Scale")
        self.Scale.addItem("N Scale")
#       self.#Scale.setSelectedItem() = "HO Scale"

        self.Locomotive = javax.swing.JComboBox()
        self.Locomotive.addItem("Diesel")
        self.Locomotive.addItem("Steam")
#       self.#locomotive.setSelectedItem() = "Diesel"

  #     self.DecoderBrand = javax.swing.JComboBox(DecoderList)

        # Put contents in frame and display
        f.contentPane.add(temppanel1)
        temppanel2 = javax.swing.JPanel()
        f.contentPane.add(self.Scale)
        f.contentPane.add(self.Locomotive)
  #     f.contentPane.add(self.DecoderBrand)
        temppanel2.add(self.startButton)
        f.contentPane.add(temppanel2)
        f.contentPane.add(self.status)
        f.pack()
        f.show()

        return
#---------------------------------------------------------------
# create one of these
a = AutoSpeedTable()

# set the name, as a example of configuring it
a.setName("Automated Speed Table")

# and show the initial panel
a.setup()

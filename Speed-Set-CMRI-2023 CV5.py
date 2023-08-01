#First and foremost, this Speed matching script could not have been created without the help and previous work from the following people:
# Authors: Phil Klein, Version 2.14 copyright 2010
#           Thomas Stephens, Version SpeedTLSv5_B Copyright Jan 2013
#
#Both of the gentlemen above have laid a great foundation for which I was able to build upon.  
#This is not to take away from their work, only improve upon it by incorporating the above 2 scripts into 1 great speed matching script for all.
#I have taken the liberty to remove items that are no longer being used or I feel is not necessary.
#_____________________________________________________________________________________________________

#This Script will automatically build a speed table for a decoder using OPS mode programming and create a text file on your desktop for future use.
#
# Summary of how it works:
#   User enters info about locomotive and decoder such as Loco Number, DCC Address, Scale, Brand of decoder, CV3 and CV4 desired, 
#   direction to be tested, and Top speed desired on the input panel.
#   A throttle is created in JMRI to run the locomotive
#   The locomotive is warmed up for a few laps (in both directions if diesel is selected) 
#   The top speed of the locomotive is measured (in both directions for diesels)
#   Using the block detectors to measure time, it adjusts the throttle until the appropriate speed is found for the speed step
#   7 Speed steps are measured; the rest are interpolated. The measured ones are 4, 8, 12, 16, 20,24, and 28
#   These are written to the decoder , a text file is created on your Windows PC desktop, and the locomotive is release from the throttle and the throttle is discarded.
#
#   If something goes wrong and you need to start over; "Steal" it in another throttle and stop the locomotive.
#       Close the input panel.
#       Under the "Panels" tab, select "Thread Monitor" and "Kill" the script.   Or just close JMRI and reopen JMRI software.
#
#   Notes:
#       BEMF    Any adjustments should be made before running the script
#
#           TCS - May need to turn off BEMF since it is not adjustable. A speed jump may be present
#               and maybe very noticeable after the speedtable is created
#
#           Digitax -
#               CV57 default value 6 may prevent the locomotive from going below about 5 mph
#               setting this to 33 improves this. Or turn it off by setting it to zero.  This Speed Matching script will set it to zero for you.
#
#           NCE - some older n scale decoders will revert to 28 step mode instead of 128 step mode (this may happen in HO as well)
#
#       The locomotives speed should be approximately equivlent to what is displayed on a throttle if the maximum speed was set to 100.
#           (running by itself without a train)

# $Revision: 1.3 $ revision of AutomatonExample distributed with JMRI
#                    from which this script has been developed.
#
# 
#Authors: Phil Klein, Version 2.14 copyright 2010
#           Thomas Stephens, Version SpeedTLSv5_B Copyright Jan 2013
#           Eric Bradford, Version UltimateSpeedMatch_v1.0, Copyright Version 1.0 Feb 2013

#
#   Hardware tested with this script
#   Command Station - Digitrax DCS100, Digitrax Zypher 
#   Train Detection - BDL168 (Board Address 1),Team Digital SIC24 with DBD22's 
#   Computer Interface - MS100, Locobuffer II, PR3
#   JMRI Software 5.2 OR GREATER IS REQUIRED for this script to work.
#   By opening up the JMRI Sysem Console screen ("Help Tab" then "System console"), one can see what is being done on the track.  Useful for problem solving.
# You can also use the new Input SCript screen in JMRI to load a specific script, withour having to rely on button links, and allows scripts from any folder to load for testing.

#   Track - 12 pieces of Kato N scale 19" Radius Unitrak
#   Track - 16 pieces of Kato HO scale 21 5/8" Radius Unitrak
#   I used one sensor for each piece of HO scale track
#   I used one sensor for every 2 pieces of N scale track
#   The HO & N tracks share sensors 1 - 12
#   HO Track also uses sensors 13 - 16


#   Added step list for ESU decoders
#   Added redo time measurement when start time and stop time are the same when using the MS100
#   Fixed writing values higher than 255 to the decoder
#   Fixed writing values lower than 1
#   Added STEAM to input panel to see if that accomodates tender pickup issues
#       Steam locomotives should be placed on the track so that the wheels that pick up power
#       on the tenders front truck are on the rail that is detected to reduce errors.
#   Added the ability for the user to select the top speed
#   Added "Atlas" to user selectable decoders
#   05/28/08    Added CV25 = 0 If decoder was using a predefined table, can't get accurate measurements
#   08/18/08    Fixed Atlas...should have been Atlas/Lenz XF
#   08/25/08    Added waits after writing CV's 62, 25 and 29  possible issue with Zypher not sending write CV29 command
#   08/26/08    Changed speedtable setting for testing 128 support from 120 to 84
#   09/09/08    Seperated testing for 128 support for N scale and HO scale.
#   09/09/08    Changed speedtable setting for testing 128 support for HO from 84 to 80
#   09/11/08    Add displaying of throttle setting chosen for given speed step
#   09/22/08    Added "Done != True"  to fine measurement.  Was changing throttle setting even though we were done 
#   09/22/08    Increased wait times after writing CV's before warm up  QSI decoders weren't getting all of them  was 250msec, now 500
#   01/09/09    TCS decoders would not run after initial ops mode programming
#   01/09/09    TCS decoders stall when using values above 249 
#   06/15/09    Changed Soundtraxx to Soundtraxx DCD in preparation for adding Soundtraxx Tsunami 
#   06/26/09    Added Soundtraxx Tsunami
#   08/28/09    Increased wait time when writing table from 100ms to 150ms  DZ121 was getting zero written for every other entry 
#   09/11/09    Added cycling track power before starting.
#   09/15/09    Created new list for newer TCS decoders
#   09/15/09    Created test to determine which TCS list to use
#   09/15/09    Increased wait time when measuring max speed.  Tsunami was missing direction change
#   09/15/09    Added wait time when turning on speed table.  Tsunami was missing change to CV29
#   09/17/09    Removed "Unknown" from selection list.  Getting too hard to support 
#   09/17/09    fixed throttlesetting from being set above 127 
#   09/17/09    moved comparison of hithrottle & lowthrottle into coarse measurement
#   09/18/09    added a second forward statment when measuring fwd max speed. Sometimes doesn't execute
#   05/21/10    changed getOpsModeProgrammer to getAddressedeProgrammer something changed between 2.8 and 2.9.6
#   05/21/10    warmup for steam now only goes forward
#   03/17/12        Added prompts for acel/decel values (CV3/4), Sets value when done
#   03/17/12        added prompt for target direction. Replaces calculation based on max speed
#   03/17/12        increased numbers of values in countsensor to compensate for odd values on specific track sections
#   02/18/2013  Changed number of measurements from 1 to 4 for 100 mph by adding a "high speed array"..
#   02/18/2013  Corrected decoder lists for speed measurements.  Wrong list being used due to python coding issues.
#   02/18/2013  Set up that if user forgets to choose scale, default is N-SCALE.
#   02/18/2013  Text File now being created on windows PC desktop (at least for Win XP) for future use.
#   02/18/2013  Added comments by commands throughout the script to help others understand what is taking place.
#   01/12/2023  updated JYTHON commandds to new JMRI versions. Several obsolete function calls were replaced with current functions
#   01/12/2023  Altered speed calibration loop to use CV5 instead of speed table. this works witht he following decoder types:
#                   Loksounds (Lokspounds internally calculate speed steps from CV2 to CV5, using the speed table only to deviate from linear slope)
#                   Tsunami 2 
#                   Any decoder with CV5, about 80% of current decoders.
#                   



#--------------------------------------------------------------- 
import java
import javax.swing
import jmri
#
class AutoSpeedTable(jmri.jmrit.automat.AbstractAutomaton) :
    

    # individual block section length (scale feet)
    blockN = float(133)  # 132.5778 feet  Phil's test track
    blockHO = float(62)  #  61.6264 feet  Kato R550 track
    blockCount = 16 # max block count, determined by hardware used. Block length times block count = full diameter of tack loop

#   blockN = float(108)  # 108.?    feet  Kent's test track
#   blockHO = float(65)  #  65.312  feet  Kent's test track

#   blockHO = float(123)  #  123.2528 feet per two track sections TeamDigital
#   numBlocksHO = float(8) #  for TeamDigital


    long = False
# +++ TLS 3/17/12 more test numbers. was 5. Compensate for odd values on specific track sections
    countsensor = 7 # Use 1 for testing and 7 for running
# --- TLS
#---------
# function to write CV value, wait and print confirm.
    def outputCV (self, CVnum, CVvalue):
        self.programmer.writeCV( CVnum  , CVvalue, None )
        print "write - CV %s with %d" % (CVnum, CVvalue)
        self.waitMsec( 500 )
        return
# function to write indexed CV value, wait and print confirm.
    def outputIndexCV (self, CVnum, CVvalue, CV31 = 0, CV32 = 0):
        self.programmer.writeCV( "CV31"  , CV31, None )
        self.waitMsec( 200 )
        self.programmer.writeCV( "CV32"  , CV32, None )
        self.waitMsec( 200 )
        self.programmer.writeCV( CVnum  , CVvalue, None )
        print "write - CV %s with %d" % (CVnum, CVvalue)
        self.waitMsec( 500 )
        return
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



        #EWB--Used for 100 MPH (setting for Digitrax DT400 throttle)
        #EWB--Wanted to take 3-4 measurements at higher speeds instead of just 1 measurement per lap.
        self.HighSpeedArray = (
                self.sensor1,
                self.sensor5,
                self.sensor9,
                self.sensor13)

        #Used for speeds between 50 and 99 MPH
        #Uses 2 blocks for each measurement
        self.MediumSpeedArray = (
                self.sensor1,
                self.sensor3,
                self.sensor5,
                self.sensor7,
                self.sensor9,
                self.sensor11,
                self.sensor13,
                self.sensor15)

        # used below 50 MPH 
        #Uses single blocks for measurements
        self.LowSpeedArray = (
                self.sensor1,
                self.sensor2,
                self.sensor3,
                self.sensor4,
                self.sensor5,
                self.sensor6,
                self.sensor7,
                self.sensor8,
                self.sensor9,
                self.sensor10,
                self.sensor11,
                self.sensor12,
                self.sensor13,
                self.sensor14,
                self.sensor15,
                self.sensor16)



#       These speed steps are measured.  All others are calculated
#               CV  70  74  78  82  86  90  94
#       Speedsteps  4   8   12  16  20  24  28

#       These lists are percentages of full speed
        self.DigitraxStepList = [
                14, 29, 43, 57, 71, 86, 100]

        self.Lenz5GenStepList = [
                17, 30, 44, 57, 71, 84, 98]

        self.LenzXFStepList = [
                11, 26, 40.5,   55, 70, 84, 98.5]

        self.NCEStepList = [
                10.5,   25, 39.5,   54, 68, 83, 98]

        self.MRCStepList = [
                14, 29, 43, 57, 71, 86, 100]

        self.OldTCSStepList = [
                14.5,   28.5,   42.5,   57, 71.5,   86, 99]

        self.NewTCSStepList = [
                13, 25.5,   38, 50.5,   63, 75.5,   88]

        self.QSIStepList = [
                11, 26, 41, 55, 70, 85, 99]

        self.SoundtraxxDSDStepList = [
                14, 28, 42, 56, 70, 84, 99]

        self.TsunamiStepList = [
                14.5,   28.5,   42.5,   57, 71, 85, 99]

        self.ESUStepList = [100]
        self.XXXStepList = [
                14, 29, 43, 57, 71, 86, 100]


# Getting throttle
        
        self.status.text = "Getting throttle"

        dccnumber = int(self.dccaddress.text)   #throttle number, might be consist
        loconumber = int(self.locoaddress.text)  #programmer number
        if (dccnumber == 0):
            dccnumber = loconumber
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
            print "Locomotive number",loconumber, "with DCC Address",dccnumber
        if (loconumber > 127) :
             self.long = True
        else :
             self.long = False

# Getting Programmer
#05/21/10
        self.programmer = addressedProgrammers.getAddressedProgrammer(self.long, loconumber)

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
# calculate new CV5 value
    def AdjustCV5(self,diff, cv5):
        print "adj function"
        print diff
        print cv5
        if (abs(diff) > 10.0):
            adj5 = 15
        else:
            adj5 = 1
        print adj5
        if (diff < 0):
            cv5 = cv5 - adj5
        else:
            cv5 = cv5 + adj5
        print "new CV5"
        print cv5
        return cv5
        

#---------------------------------------------------------------
    def getspeed(self,targetspeed,block) :
        """converts time to speed, ft/sec - scale speed"""
        print "get speed()"
        print targetspeed
        #print block
        print ""
        starttime = stoptime = 0    # Needed when using every block
        self.memory24.value = str(targetspeed)

        speedlist = []  # Clear Speedlist (speed list contains measured speeds for each run)

        self.waitSensorInactive(self.LowSpeedArray)     #Making sure locomotive is at the correct starting position

        for z in range(1,self.countsensor + 1) : # make <countsensor> speed measurements
            if int(targetspeed) >= 123 : #Used for determining max forward and reverse speeds

                blocklength = block * blockCount   # 
                duration, starttime, stoptime = self.measuretime([self.sensor1],blocklength,starttime,stoptime)
            
            elif int(targetspeed) >= 100 :  # EWB -- Used for final speed step and for finding max forward and reverse speeds.
                blocklength = block * 4  #16 divided into 4 virtual blocks 
                duration, starttime, stoptime = self.measuretime(self.HighSpeedArray,blocklength,starttime,stoptime)#makes 4-block measurements

            elif int(targetspeed) >= 50 :   # EWB -- Used for speed steps between 50 and 99 mph.
                blocklength = block * 2 #16 divided into 8 virtual blocks
                duration, starttime, stoptime = self.measuretime(self.MediumSpeedArray,blocklength,starttime,stoptime)# makes 2-block measurements
            else :
                blocklength = block * 1     #EWB -- Used for speed steps 10 and 49 mph. 
                # use all blocks for low speed, smallest virtual block size
                duration, starttime, stoptime = self.measuretime(self.LowSpeedArray,blocklength,starttime,stoptime) #makes 1-block measurements
            
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


        # EWB-- select the median from the list and use it as the measured speed
        speedlist.sort() #EWB-- sorts the <countsensor> measurements from smallest to largest
        speed = speedlist.pop(3) #EWB-- Chooses (numbered entry) in sorted "speedlist" set above NOT including first entry
        #EWB --Previous number was not choosing correct median value for set of measurements.

        return speed
#---------------------------------------------------------------

# handle() will only execute once here, to run a single test
#EWB -- Any "print" command starting from here will show up in the JMRI Sysem Console screen ("Help Tab" then "System console")
    def handle(self):
    
        print "SpeedMatch_v2.1 --- TLS 10/1/2022"

        screendisplay = float(self.MaxSpeed.text)   #used for display purposes
#        topspeed = float(self.MaxSpeed.text)/100    # Used for calculation purposes
        newspeed = float(self.MaxSpeed.text)    # Used for calculation purposes
        print "Top Speed is ",screendisplay, "MPH"
        self.status.text = "Locomotive Setup"
        self.memory25.value = "Preparing Locomotive for speed measurments"
        cv5setting = 255

#09/11/09
        jmri.InstanceManager.getDefault(jmri.PowerManager).setPower(jmri.PowerManager.OFF)  ## CA 2022-08-19
        self.waitMsec(1000)
        jmri.InstanceManager.getDefault(jmri.PowerManager).setPower(jmri.PowerManager.ON) ## CA 2022-08-19
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
            # if user forgets to click a scale button, then it's HO scale
            block = self.blockHO

        print self.Scale.getSelectedItem()
        print "Decoder Brand is", self.DecoderBrand.getSelectedItem()
        self.memory23.value = self.DecoderBrand.getSelectedItem()
        decodertype = self.DecoderBrand.getSelectedItem()
        print "CV3 will be set to",self.cv3.text
        print "CV4 will be set to",self.cv4.text

        print "Speed Matching Direction is set to", self.SetDirection.getSelectedItem()
        print "-----\n"
 
        # This will change FX Rate and Keep Alive on Digitrax Decoders
        # This will change Random Sound Max on ESU LokSound Decoders
# 08/25/08
# 09/22/08
#        if decodertype == "QSI-BLI" :
#            self.programmer.writeCV(62, 0, None) # Turn off verbal reporting on QSI decoders
#            self.waitMsec(1000)

#        if decodertype == "Digitrax" :
#            self.outputCV( "57", 0)
#            self.waitMsec(1000)
            
#            self.programmer.writeCV(25, 0, None) # Turn off manufacture defined speed tables
#        self.waitMsec(750)

        if self.long == True :          #turn off speed tables
            #self.programmer.writeCV(29, 34, None)
            self.outputCV( "29", 34)
        else:
            #self.programmer.writeCV("29", 2, None)
            self.outputCV( "29", 2)


        #self.programmer.writeCV(2, 0, None)    #Start Voltage off (EWB--CV not changed due to high max forward/reverse speeds measured.  speeds > 225mph!)
        #self.waitMsec(500)
        #self.programmer.writeCV("3", 0, None) #Acceleration off
        self.outputCV( "3", 0)

        #self.programmer.writeCV("4", 0, None) #Deceleration off
        self.outputCV( "4", 0)
#        self.outputCV( "19", 0) # may use this for throttle
        #self.programmer.writeCV("19", 0, None)    #Clear consist # not turned off as thie might be the DCC address.
        self.outputCV( "5", cv5setting)
        self.outputCV( "6", 0)
        self.outputCV( "66", 128) # remove trim
        self.outputCV( "95", 128) # remove trim



        # Run Locomotive for 10 laps each direction to warm it up

        self.programmer.writeCV("5", 255, None) #set to max speed
        self.waitMsec(500)

        self.memory25.value = "Warming up Locomotive"
        self.status.text = "Warming up Locomotive"
        print
        print "Warming up Locomotive"
        print
        self.throttle.setIsForward(True)
        self.memory20.value = "Forward"
        self.throttle.speedSetting = 1.0

        self.throttle.setF0(True)
        #self.throttle.setF8(True)

        # Warm up locomotive for 10 laps forward


        for x in range (1, 10) :
            self.waitChange([self.sensor1])
            self.waitSensorActive(self.sensor1)
            print x

        self.throttle.speedSetting = 0.0
        self.waitMsec(2000)
        
        # Warm up 10 laps reverse

#05/21/10   Removed reverse warmup and max speed measurement for Steam

        if self.Locomotive.getSelectedItem() == "Diesel" :
            self.throttle.setIsForward(False)
            self.memory20.value = "Reverse"
            self.throttle.speedSetting = .98

            for x in range (1, 5) :
                self.waitChange([self.sensor1])
                self.waitSensorActive(self.sensor1)
                print x

        # Find maximum speed reverse

            self.memory25.value = "Finding Maximum Speeds"
            self.throttle.speedSetting = .98
            self.waitMsec(500)
            revmaxspeed = self.getspeed(125,block)
            print
            print "Reverse Max Speed = ",round(revmaxspeed), "MPH"
            print
            #self.throttle.speedSetting = 0.0
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
        self.throttle.speedSetting = .98
        self.waitMsec(1000)
        fwdmaxspeed = self.getspeed(125,block) #125 MPH as tartet speed. Only EU Loks can go faster
        print
        print "Forward Max Speed = ",round(fwdmaxspeed), "MPH"
        print
        self.status.text = "Max Forward Speed " + str(int(fwdmaxspeed))
        self.memory22.value = str(int(fwdmaxspeed))
        self.waitMsec(1000)
        
        self.memory23.value = decodertype
        print "Decoder Brand Installed is ",decodertype

        self.throttle.speedSetting = 0.0 #stop
        self.waitMsec(2000)


        #we are now ready to build a speedtable
        if decodertype <> "Unknown" :

            self.memory25.value = "Measuring Speeds"
            print "building 1"

            #Turn off speed table for measurements
            if self.long == True :
                #self.programmer.writeCV(29, 34, None)
                self.outputCV( "29", 34)
            else:
                #self.programmer.writeCV(29, 2, None)
                self.outputCV( "29", 2)

#set direction based on user selection
# ++ TLS
            if self.SetDirection.getSelectedItem() == "Forward" :
                self.throttle.setIsForward(True)
                self.memory20.value = "Forward"
            else:
                self.throttle.setIsForward(False)
                self.memory20.value = "Reverse"
            steplist = self.ESUStepList
            # for tables, Step list is list of percentages to calc intermediate speed table values. 
            #targetspeed = newspeed

            print self.memory20.value
# -- TLS

            #Find throttle setting that gives desired speed

             #initializing all variables for next measured speed step
            Done = False
            speed = 1000
            minimumdifference = 2.0
            beenupone = False
            beendownone = False
            lowspeed = 0    
            hispeed = 1000
            hithrottle = 1.0
            stepvaluelist = [0]
            cv5setting = 155 # set to 255 to start at top speed, and adjust down. 155 is center value, might adjust up or down.
            lowthrottle = 2

#            for speedvalue in steplist :    
            print
            print
            print "TARGET SPEED BEING MEASURED IS: ",newspeed, " MPH"
            print
            print

            stepvaluelist.extend([0,0,0]) #create spots in list for calculated speed steps



            #05/21/10
            if ((self.Locomotive.getSelectedItem() == "Diesel") and (newspeed > revmaxspeed)) or newspeed > fwdmaxspeed :
                print
                print "Locomotive can not reach ",newspeed, " MPH"
                print
                Done = True
                self.throttle.speedSetting = .98 2 # some decoders will not start at speed 1.0.
                self.waitMsec(500)
                self.throttle.speedSetting = 1.0

#main speed adjustment loop
            while Done == False:
                #Update CV5 to update speed
                
                self.outputCV( "5", cv5setting)
                jmri.InstanceManager.getDefault(jmri.PowerManager).setPower(jmri.PowerManager.OFF)  ## CA 2022-08-19
                self.waitMsec(1000)
                jmri.InstanceManager.getDefault(jmri.PowerManager).setPower(jmri.PowerManager.ON) ## CA 2022-08-19
                self.waitMsec(1000)
                self.throttle.speedSetting = .98
                self.waitMsec(500)
                self.throttle.setSpeedSettingAgain(1.0) # use function instead of direct write

                # Measure speed
    
                self.waitMsec(100)
                print
                print "CV5 value Setting ",cv5setting
                speed = self.getspeed(newspeed,block)

                # compare it to desired speed and decide whether or not to test a different throttle setting
                difference = newspeed - speed
                print "Difference = ",round(speed - newspeed,1), "MPH at throttle setting ",cv5setting
                print

                if (minimumdifference > abs(difference)) :
                    Done = True
                else :
                    newcv5setting = self.AdjustCV5(difference,cv5setting)
                    if (newcv5setting == cv5setting):
                        Done = True
                    else:
                        cv5setting = newcv5setting
	
                if (cv5setting < 1) :
                    print
                    print "Cannot create speedtable"
                    print "Locomotive has mechanical or decoder problem"
                    print
                    Done = True
                    badlocomotive = True
                    throttlesetting = 1

                if (cv5setting > 255) :
                    print
                    print "Locomotive can not reach ",newspeed, " MPH"
                    print
                    Done = True
                    badlocomotive = True
                    cv5setting = 255

            

            # Stop locomotive

            self.throttle.speedSetting = 0.0
            self.waitMsec(3000)

            #Calculate speed step values inbetween measured ones

            if badlocomotive == False :
                print
                print "Process Complete"
                #print stepvaluelist
                print


                print"Turn on acceleration and deceleration"    # Turn on acceleration and deceleration 
                print "Writing value to CV3: ",self.cv3.text
                self.outputCV( "3", int(self.cv3.text))
                #self.programmer.writeCV(3, int(self.cv3.text), None)    #Acceleration changed to user setting from input panel.
                
                print "Writing value to CV4: ",self.cv4.text
                self.outputCV( "4", int(self.cv4.text))
                #self.programmer.writeCV(4, int(self.cv4.text), None)    #Deceleration changed to user setting from input panel.
                #self.waitMsec(250)

                print
                #print "All Speed Table CV Values"
                #print stepvaluelist     #Displays whole range of speed table values on JMRI system console.
                #print
                #print "Writing Speed Table CV Values to Locomotive"

                #print "Turn on speed table"
                print
                print "set - CV %s with %d" % (5, cv5setting)
                self.outputCV( "5", cv5setting) # update CV5 one last time with calculated value.
#06/28/09
                

                #self.outfilename = "C:\\Download\\update\\" + "Loco_" + self.locoaddress.text + "_""DCC#_" + self.dccaddress.text + "_" +decodertype + ".txt"
                ##Creates a file on USB Stick in the following manner:  "Loco 1234_DCC# 4321_Digitrax.txt"
                #print""
                #print "Transferring Data to a Text File for future use: ",self.outfilename
                #print""
                #self.ofl = open(self.outfilename, "a")
                #self.ofl.write (self.Scale.getSelectedItem() + "\n")    #Records scale used in text file.
                #self.ofl.write ("-----\n")                              # New line created.
                #self.ofl.write ("-----\n")
                #self.ofl.write ("-----\n")

                #self.ofl.write ("CV3 is set to " + self.cv3.text + "\n")    #Records what CV3 was set to as per input panel.
                #self.ofl.write ("CV4 is set to " + self.cv4.text + "\n")    #Records what CV4 was set to as per input panel.
                #self.ofl.write ("\n")
                #self.ofl.write ("Speed Matching Direction is set to " + self.SetDirection.getSelectedItem()  + "\n")    #Records loco direction used for speed matching.
                #self.ofl.write ("\n")
                #self.ofl.write ("Max Forward Speed is " + str(int(fwdmaxspeed))+ " MPH" + "\n") #Records max forward speed obtained.
                #self.ofl.write ("Max Reverse Speed is " + str(int(revmaxspeed)) + " MPH" + "\n")        #Records max reverse speed obtained.
                #self.ofl.write ("-----\n")
                #self.ofl.write ("-----\n")
                #self.ofl.write ("set - CV %s with %d" % (5, cv5setting))
                #self.ofl.write ("Speed Table Values" + "\n")        
                #self.ofl.write ("\n")
                #self.ofl.flush()
                #self.ofl.close()
                                
                #self.status.text = "Done"
            else :
                self.status.text = "Done - Locomotive has decoder or mechanical problem; cannot create speed table"

        else :
            self.status.text = "Done - Unknown Decoder Cannot Proceed"
    
        
        
        self.throttle.setF8(False)
        self.throttle.setF0(False)
        endtesttime = java.lang.System.currentTimeMillis()
        print
        print "Test Time = ",((endtesttime - starttesttime) / 1000) / 60, " min."       #Displays time it took to complete the speedmatching of locomotive.

        # done!

#        self.throttle.release(null)
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

        DecoderList = ["ESU", "Digitrax", "TCS", "NCE", "MRC", "QSI-BLI", "Soundtraxx", "Lenz Gen 5", "Atlas/Lenz XF", "Tsunami"] 
    
        # create a frame to hold the button, set up for nice layout
        f = javax.swing.JFrame("Speed Matching Table Input Panel")      # argument is the frames title
        f.setLocation(120,50)
        f.contentPane.setLayout(javax.swing.BoxLayout(f.contentPane, javax.swing.BoxLayout.Y_AXIS))

        # create the DCC text field
        self.dccaddress = javax.swing.JTextField(5) # sized to hold 5 characters, initially empty

        # put the text field on a line preceded by a label
        temppanel1 = javax.swing.JPanel()
        temppanel1.add(javax.swing.JLabel("      DCC Address (consist)"))
        temppanel1.add(self.dccaddress)

        # create the LOCO text field
        self.locoaddress = javax.swing.JTextField(5)    # sized to hold 5 characters, initially empty

        # put the LOCO text field on a line preceded by a label
        temppanel5 = javax.swing.JPanel()
        temppanel5.add(javax.swing.JLabel("         Locomotive number"))
        temppanel5.add(self.locoaddress)
        
# create the momentum value fields
        self.cv3 = javax.swing.JTextField(3)    # sized to hold 3 characters, initially empty
        self.cv4 = javax.swing.JTextField(3)    # sized to hold 3 characters, initially empty

        # put the text field on a line preceded by a label
        temppanel4 = javax.swing.JPanel()
        temppanel4.add(javax.swing.JLabel("  cv3 "))
        temppanel4.add(self.cv3)
        temppanel4.add(javax.swing.JLabel("  cv4 "))
        temppanel4.add(self.cv4)
        self.cv3.setText("1")       #Prefer to have at least a little Acceleration momentum as a standard.
        self.cv4.setText("1")       #Prefer to have at least a little Deceleration momentum as a standard.

                
        # create the start button
        self.startButton = javax.swing.JButton("Start")
        self.startButton.actionPerformed = self.whenMyButtonClicked

        self.status = javax.swing.JLabel("Enter Locomotive and DCC Addresses and press Start")
        
        self.Scale = javax.swing.JComboBox()
        self.Scale.addItem("Choose a Scale")
        self.Scale.addItem("N Scale")
        self.Scale.addItem("HO Scale")

        self.Locomotive = javax.swing.JComboBox()
        self.Locomotive.addItem("Diesel")
        self.Locomotive.addItem("Steam")

        self.SetDirection = javax.swing.JComboBox()
        self.SetDirection.addItem("Forward")
        self.SetDirection.addItem("Reverse")

        self.MaxSpeed = javax.swing.JTextField(3)

        temppanel3 = javax.swing.JPanel()
        temppanel3.add(javax.swing.JLabel("Target Speed"))
        temppanel3.add(self.MaxSpeed)

        self.DecoderBrand = javax.swing.JComboBox(DecoderList)

        # Put contents in frame and display
        f.contentPane.add(temppanel5)
        f.contentPane.add(temppanel1)
        temppanel2 = javax.swing.JPanel()
        f.contentPane.add(self.Scale)
        f.contentPane.add(self.Locomotive)
        f.contentPane.add(self.DecoderBrand)
        f.contentPane.add(temppanel4)
        f.contentPane.add(self.SetDirection)
        f.contentPane.add(temppanel3)
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

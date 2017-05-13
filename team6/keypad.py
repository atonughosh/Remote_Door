#code to interface keypad, change password and open door using password through keypad

while(True):
	import RPi.GPIO as GPIO
	import time

	GPIO.setmode(GPIO.BOARD)


	#commands to change password & open door
	change_pass = '*#AB'
	open_door = '0#C*'


	#keypad initialize
	MATRIX = [[1, 2, 3, 'A'],
	          [4, 5, 6, 'B'],
	          [7, 8, 9, 'C'],
	          ['*', 0, '#', 'D']]

	ROW = [11, 12, 13, 15]
	COL = [37, 35, 33, 31]

	for j in range(4):
	    GPIO.setup(COL[j], GPIO.OUT)
	    GPIO.output(COL[j], 1)

	for i in range(4):
	    GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.setup(29, GPIO.OUT)
	GPIO.output(29,GPIO. LOW)

	#function to capture key press
	def key_press():
	    key_entered = []
	    try:
	        while (True):
	            for j in range(4):
	                GPIO.output(COL[j], 0)

	                for i in range(4):
	                    if GPIO.input(ROW[i]) == 0:
	                        time.sleep(0.2)
	                        print(MATRIX[i][j])
	                        key_entered.append(MATRIX[i][j])
	                        time.sleep(0.2)
	                        while (GPIO.input(ROW[i]) == 0):
	                            time.sleep(0.2)
	                            pass

	                GPIO.output(COL[j], 1)
	            if len((key_entered)) == 4:
	                cmd = ''.join(str(e) for e in key_entered)
	                return cmd

	    except KeyboardInterrupt:
	        GPIO.cleanup()


	key_pressed = key_press()



	#code to change password
	if key_pressed == change_pass:
	        file = open("app.txt", "r+")
	        file_content = file.read(4)
	        file.close()
	        print("Enter current password")
	        pass_input = key_press()
	        if file_content == pass_input:
	                print("Enter new password :")
	                new_pass = key_press()
	                print("Re-enter new password :")
	                new_pass_confirm = key_press()
	                if new_pass == new_pass_confirm:
	                        file = open("app.txt", "w")
	                        file.write(new_pass)
	                        file.close()
	                        print("Password change successful")
	                else:
	                        print("New password & Re-enter password doesn't match. Try again")
	        else:
	                print("Incorrect current password")


	#code to open door using keypad
	if key_pressed == open_door:
	        print("Enter password to unlock door : ")
	        open_token = key_press()
	        file = open("app.txt", "r+")
	        file_content = file.read(4)
	        if open_token == file_content:
	                GPIO.output(29, GPIO.HIGH)
	                print("Door Unlocked.........")
	                time.sleep(10)
	                GPIO.output(29, GPIO.LOW)
	                print("Door Locked.........")
	        else:
	                print("Incorrect password entered")

#Shahaddin Gafarov. UFID: 3053-9258
#COP 5536 Project 1: Gator Air Traffic Slot Scheduler
#main.py: primary file, processes input output and the terminal/console related matters


#importing the logic class
from logic import logic_class

#sys for easy input reading
import sys

#main function
def main():
    #if the input count is not 2(which comes after python so the executable and the text file input)
    if(len(sys.argv) != 2):
        #reminder for the user
        print("$ python3 gatorAirTrafficScheduler file_name")
        return
    
    #the input file is the latter of the two
    input_file = sys.argv[1]

    #I did not add extensive erro handling with wrong text file input names
    #so I am assuming the user will add a file that ends with .txt
    output_file = ""
    
    #the loop is looking for . t x t characters from the input file name, and when it finds one it stops,
    #thus getting the file name itself without the .txt extension
    for i in range (len(input_file)-3):
        if(input_file[i]=='.' and input_file[i+1] == 't' and input_file[i+2]=='x' and input_file[i+3] == 't'):
            break
        output_file += input_file[i]
    #the input file name + _output_file.txt = output file name
    output_file += "_output_file.txt"

    #logic class is initialized
    logic = logic_class()

    #output is for keeping a record of all outputs the project handles, for a later write operation
    output = []

    #r for readinf the input file, file_in is the name for what's being read
    with open(input_file, "r") as file_in:
        #divide the entire block of text into respective lines
        for line in file_in:
            line = line.strip()
            #I added this so my code won't read "" as wrong answer(making the reading less agressive)
            if(line==""):
                continue
            
            #if it is in the proper format that has ( and ) parenthesis
            if "(" in line and ")" in line:
                #the function name is whatever that is before the opening parenthesis
                line_command = line.split("(")
                #again, make the reading less agressive: for ex. quit() = QUIT() = Quit()
                line_command = line_command[0].lower()

                #this hols whatever the numbers are withing the parenthesis
                line_contents = []
                
                #what index the parenthesis start and end
                start_parenthesis = line.find("(")
                end_parenthesis = line.find(")")


                #This is more strict not allowing any space after ), so I ditched it to be less sensitive
                # if(end_parenthesis!=len(line)-1):
                #     output.append("Invalid Input.")
                #     continue


                #the last letter of input must be ) so no quit() 5
                #thoguht I made it so that quit() may have blank space after, again to make it less agressive with inputs
                xxxx=0
                temp = end_parenthesis+1
                #checks if there are non-empty space characters coming after the first end parenthesis(which should be the only one)
                while(temp<len(line)):
                    if(line[temp]!= " "):
                        xxxx = 1
                    temp= temp+1
                if(xxxx==1):
                    output.append("Invalid Input.")
                    continue
                
                #if the starting point parenthesis is not starting right after the function name, then there is something wrong
                #but this line_command = line.split("(") likely make sure this check is not triggered in the first place
                if(start_parenthesis!=len(line_command)):
                    output.append("Invalid Input.")
                    continue
                
                #olds the record of the numbers between two parenthesis:
                i = start_parenthesis

                #Reprioritize(608, 8, 11) - > [608,8,11]
                while i<end_parenthesis:
                    number = ""
                    #makes sure the characters are digits and hold them into single number until next non-digit character is seen which
                    #usually is comma or end parenthesis: 6 + 0 + 8 = 608
                    while (line[i].isdigit() == True):
                        number += str(line[i])
                        i += 1
                        if(i==len(line)):
                            break
                    if(i==len(line)):
                        break
                    if(len(number)!= 0):
                        line_contents.append(int(number))
                    i +=1
                # print(line)
                # print(line_command)
                # print(line_contents)


                #if the format is wrong:
            else:
                output.append("Invalid Input.")
                continue

            
            #All function's respective argument count requirement which if met, will be recorer to the output array:

            #initialize function must take only 1 element
            if(line_command == "initialize"):
                if(len(line_contents) != 1):
                    # print("Invalid output.")
                    output.append("Invalid output.")
                else:
                    output.append(logic.initialize_runways(line_contents[0]))

            #submitflight function must take 5 elements
            elif(line_command == "submitflight"):
                if(len(line_contents) != 5):
                    # print("Invalid output.")
                    output.append("Invalid output.")
                else:
                    output.extend(logic.submitflight(line_contents[0], line_contents[1], line_contents[2], line_contents[3], line_contents[4]))
            
            #printschedule function must take 2 elements
            elif(line_command == "printschedule"):
                if(len(line_contents) != 2):
                    # print("Invalid output.")
                    output.append("Invalid output.")
                else:
                    temp_array = logic.printschedule(line_contents[0], line_contents[1])
                    #the test cases dont want brackets with if case's output
                    for i in temp_array:
                        if(i== "There are no flights in that time period"):
                            output.append(f"{i}")
                        else:
                            output.append(f"[{i}]")

            #reprioritize function must take 3 elements
            elif(line_command == "reprioritize"):
                if(len(line_contents) != 3):
                    # print("Invalid output.")
                    output.append("Invalid output.")
                else:
                    output.extend(logic.reprioritize(line_contents[1], line_contents[0], line_contents[2]))

            #groundhold function must take 3 elements
            elif(line_command == "groundhold"):
                if(len(line_contents) != 3):
                    # print("Invalid output.")
                    output.append("Invalid output.")
                else:
                    output.extend(logic.groundhold(line_contents[0], line_contents[1], line_contents[2]))

            #addrunways function must take 2 elements
            elif(line_command == "addrunways"):
                if(len(line_contents) != 2):
                    # print("Invalid output.")
                    output.append("Invalid output.")
                else:
                    output.extend(logic.addrunways(line_contents[0], line_contents[1]))
            
            #cancelflight function must take 2 elements
            elif(line_command == "cancelflight"):
                if(len(line_contents) != 2):
                    output.append("Invalid output.")
                else:
                    output.extend(logic.cancelflight(line_contents[0], line_contents[1]))

            #tick function must take only-1 element
            elif(line_command == "tick"):
                if(len(line_contents) != 1):
                    output.append("Invalid output.")
                else:
                    output.extend(logic.tick(line_contents[0]))

            #printactive function must take no element
            elif(line_command == "printactive"):
                if(len(line_contents) != 0):
                    output.append("Invalid output.")
                else:
                    output.extend(logic.printactive())
            
            #quit function must take no element
            elif(line_command == "quit"):
                if(len(line_contents) != 0):
                    output.append("Invalid output.")
                #break the code once quit() happens
                else:
                    break
            else:
                output.append("Invalid Input.")

    #write all the appended/extended outputs into the output file
    #w stands for write
    with open(output_file, "w") as file_out:
        for line in output:
            #add endline to make sure they don't get printed side by side
            file_out.write(str(line) + "\n")
        file_out.write("Program Terminated!!\n")

#call the main function
if __name__ == "__main__":
    main()
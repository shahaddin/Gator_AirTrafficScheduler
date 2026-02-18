#Shahaddin Gafarov. UFID: 3053-9258
#COP 5536 Project 1: Gator Air Traffic Slot Scheduler
#Makefile: creates an executable for the main function(gatorAirTrafficScheduler.py -> gatorAirTrafficScheduler)


#Python Makefile tutorial that I got the main idea from: https://earthly.dev/blog/python-makefile/

#the python version, the executable, and the source file
PYTHON := python3
exec:= gatorAirTrafficScheduler
exec_python := gatorAirTrafficScheduler.py


all: $(exec)
#executable is linked to the source file
$(exec): $(exec_python)
#default location
	@echo '#!/usr/bin/env $(PYTHON)' > $(exec)
#gets the main function logic like a library
	@echo 'from gatorAirTrafficScheduler import main' >> $(exec)
#and calls it to execute(start the code)
	@echo 'if __name__ == "__main__": main()' >> $(exec)
	@chmod +x $(exec)

#the ordering of the inputs, with python version first
#then the executable
#and then the input .txt file read as input
run: $(exec)
	@$(PYTHON) $(exec_python) $(FILE)

#cleanup
clean:
	@rm -rf __pycache__
	@rm -f $(exec)

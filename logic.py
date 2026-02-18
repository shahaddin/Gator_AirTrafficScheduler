#Shahaddin Gafarov. UFID: 3053-9258
#COP 5536 Project 1: Gator Air Traffic Slot Scheduler
#logic.py: all the logical decision making is happening here, and where the fucntions are being handled


# import data_structures.py and its 3 classes
from data_structures import maxpairingheap, binaryminheap, flight_class
from typing import Dict, Optional

#logic which computes all the logical operations of the project
class logic_class:
    #initialize with current time at 0, 0 runways, and flight calling the flight class
    def __init__(self):
        self.current_time = 0
        self.total_runways = 0
        self.flight: Dict[int, flight_class] = {}

    #phase1, which is for settling the completions, takes the new time as input
    def phase1(self, updated_time):
        #change the time to the updated time
        self.current_time = updated_time
        #list of earlier flights
        flights_earlier = []

        #go through every flight and look for the ones that:
        for flight in self.flight.values():
            #have an eta which is earlier that the time now, and has the status of either scheduled or inprogerss
            if flight.end_time != None:
                if flight.end_time<=self.current_time and (flight.status == "scheduled" or flight.status == "inprogress"):
                    #and add it to the list of flights_earlier
                    flights_earlier.append((flight.end_time, flight.flight_id))
            
            #if the flight has started with no ETA or ETA after the current time
            #they get marked as inprogress
            if flight.start_time != None:
                if (flight.end_time == None and flight.start_time<=self.current_time) or (flight.end_time != None and flight.start_time<=self.current_time<flight.end_time):
                    flight.status = "inprogress"
        
        #sort the flights by the eta per assignment requirement
        flights_earlier.sort(key=lambda flights_earlier:(flights_earlier[0], flights_earlier[1]))

        #this is the list of landed flights
        landed_list = []

        #the ones that were in flights earlier(eta<=current time)
        #gets marked as landed
        for endtime_eta, flight_id in flights_earlier:
            #flight is fetched based on itts unique flight id:
            flight = self.flight[flight_id]
            if(flight != None):
                #ad status is changed
                flight.status = "landed"
                landed_list.append(f"Flight {flight_id} has landed at time {endtime_eta}")
                self.flight.pop(flight_id, None)
            else:
                continue
        #all the landed flights printed with their respective output message
        return landed_list


    #phase2. which is for rescheduling all the flights that are still unsatisfied
    def phase2(self):
        #list of flights to be rescheduled
        reschedule = []
        # flight_end_times = []

        #older flight_end times to be printed
        flight_end_times = {}
        reschedule_check = 0
        for flight in self.flight.values():
            #for all pending/scheduled flights and those without a start_time or with start time after the current time: 
            if(flight.status == "pending") or ((flight.status == "scheduled") and (flight.start_time == None or flight.start_time-self.current_time>0)):
                #they all get updated to pending, and wait to be assigned the other 3 values
                old_end_time = flight.end_time
                flight.status, flight.runway_id, flight.start_time, flight.end_time = "pending", None, None, None
                reschedule.append(flight)
                #the flight's old eta/end_time gets added here based on its unique flight_id
                flight_end_times[flight.flight_id] = old_end_time
                reschedule_check = 1

        #if no reschedule happens we got an empty list reschedule[]
        if reschedule_check == 0:
            return []
        #if there is one:
        else:
            #I dont need it now since the for loop above does that
            # for flight in reschedule:
            #     flight.status = "pending"
            #     flight.runway_id, flight.start_time, flight.end_time = None, None, None

            #assume all of them are available right now
            when_available = [self.current_time] * ((self.total_runways) + 1)
            
            #switch the ones that are in progress to their actual ETA for when available
            for flight in self.flight.values():
                if(flight.status == "inprogress"):
                    if(flight.runway_id != None):
                        if(flight.end_time != None):
                            if(flight.end_time >= when_available[flight.runway_id]):
                                when_available[flight.runway_id] = flight.end_time
            
            #initilize and populate the runway pool which is a binary min heap
            #with runway_ids and when they are gonna be available
            runway_pool = binaryminheap()
            for runway_id in range(1, self.total_runways+1):
                runway_pool.insert((when_available[runway_id], runway_id))
            
            #initilize and populate the pending flight queue which is a max parining heap
            #with the ones with highest priority are on top
            pending_flights_queue = maxpairingheap()
            for flight in reschedule:
                #Project Requirement: Key (max pairing heap over a triple): (priority, -submitTime, -flightID)
                tuple_of_priority = (flight.priority, -flight.submit_time, -flight.flight_id)
                pending_flights_queue.insert(flight.flight_id, tuple_of_priority)

            #forever going loop until
            xxx = 1
            while xxx == 1:
                #if either of root_max or root_min is false(which means there are either no runways or pending flights)
                #then there is nothing to reschedule

                #the root_max, which is the highest priority flight at the moment
                root_max = pending_flights_queue.getmax()
                if root_max == False:
                    xxx = 0
                    break
                
                #the root_min, which is the earliest runway which will be available
                root_min = runway_pool.getmin()
                if root_min == False:
                    xxx = 0
                    break

                #if both of them exist then we can get the values on their roots and delete root_max
                flight_id, key = root_max
                start_time, runway_id = root_min
                pending_flights_queue.deletemax()

                #make sure whether there is an actual flight corresponding to root_max's flight_id
                checkiest_checker_checker_been = 0
                flightiest_flight = flight_class()
                for flight in self.flight.values():
                    if(flight.flight_id == flight_id):
                        checkiest_checker_checker_been = 1
                        flightiest_flight = flight
                #if not here, look at the new root_max. pair
                if(checkiest_checker_checker_been == 0):
                    continue
                
                #I delete the root_min once I am actually sure that root_max is a legitimate flight
                runway_pool.deletemin()

                #update the time of the flight to be the later of the two, and update the runway_id
                flightiest_flight.start_time = max(self.current_time, start_time)
                flightiest_flight.end_time = max(self.current_time, start_time) + flightiest_flight.duration
                flightiest_flight.runway_id = runway_id

                #if flight is to be scheduled in the future the status is cheduled
                #if not(so it has already started or started right now then it is in progress)
                if(flightiest_flight.start_time-self.current_time>0):
                    flightiest_flight.status = "scheduled"
                else:
                    flightiest_flight.status = "inprogress"

                #now that we have used the runway, add/reinsert the flight's ETA and runyway number
                runway_pool.insert((flightiest_flight.end_time, flightiest_flight.runway_id))


            #the list of flights with changed ETAs
            flight_updated_end_times = []
            who_is_the_most_checker_of_them_all = 0
            for flight in self.flight.values():
                if flight.status == "scheduled" or flight.status == "inprogress":
                    # prev = flight_end_times.get(flight.flight_id, None)
                   if flight_end_times.get(flight.flight_id) != None and flight_end_times.get(flight.flight_id)  != flight.end_time:
                    # if flight_end_times.get(flight.flight_id)  != flight.end_time:
                        if(flight.end_time == None):
                           #flight_updated_end_times.append(-1, -1)?
                            flight_updated_end_times.append((flight.flight_id, -1))
                            who_is_the_most_checker_of_them_all = 1
                        else:
                           flight_updated_end_times.append((flight.flight_id, flight.end_time))
                           who_is_the_most_checker_of_them_all = 1

            #if there is no flight that had an ETA change nothing to return, empty list
            if(who_is_the_most_checker_of_them_all == 0):
                return []
            else:
            #if there are flights with updated ETAs:
                #sort them by flight_id per project requirements
                flight_updated_end_times.sort(key=lambda flight_updated_end_times: flight_updated_end_times[0])

                #merge them all in the desired format
                phase2_output = "Updated ETAs: ["
                counter33 = 1
                for flight_id, end_time in flight_updated_end_times:
                    phase2_output += f"{flight_id}: {end_time}"
                    #counter33 makes sure that the last flight won't have a comma after
                    if(len(flight_updated_end_times) != counter33):
                        phase2_output += ", "
                        counter33 += 1
                phase2_output += "]"

                #and return the output
                return [phase2_output]
        

    #start the system with x amount of runways
    def initialize_runways(self, num_runways):
        
        if(num_runways<1):
            return "Invalid input. Please provide a valid number of runways."

        #update the total runway count, which will all be available immediately()
        self.total_runways = num_runways
        self.current_time = 0
        

        #designated print message
        # print(f"{self.total_runways} Runways are now available")
        return f"{self.total_runways} Runways are now available"
    
    #print all flights with etas within the given range
    def printschedule(self, t1, t2):
        #the flights with ETAs within
        scheduled_within_interval = []
        noflights = 0

        #if the flightr is to be scheduled and has an end time within the range, add it to the list
        for flight in self.flight.values():
            # if((flight.status == "scheduled") and (flight.start_time != None and flight.start_time-self.current_time>0) and (t1<=flight.start_time<=t2)):
            # if((flight.status == "scheduled") and (flight.start_time != None) and (t1<=flight.start_time<=t2)):
            if((flight.status == "scheduled") and (flight.end_time != None) and (t1<=flight.end_time<=t2)):
                scheduled_within_interval.append((flight.end_time, flight.flight_id))
                # scheduled_within_interval.append((flight.flight_id))
                noflights=1

        #if there is no such flight return empty list and print the message accordingly
        if(noflights == 0):
            # print("There are no flights in that time period")
            scheduled_within_interval.append("There are no flights in that time period")
            return scheduled_within_interval
        
        #if there is one print the flights of interval [t1,t2]
        else:
            scheduled_within_interval.sort()
            scheduled_within_interval_without_ETA = []
            for x, y in scheduled_within_interval:
                scheduled_within_interval_without_ETA.append(y)
            # print(f"{scheduled_within_interval}")
            return scheduled_within_interval_without_ETA

    #prints all flights in system
    def printactive(self):
        #list of active flights to be printed
        print_active = []

        #get the list of all flights
        print_active2 = []
        checker_printactive = 0
        for flight in self.flight.values():
            print_active2.append(flight)
            checker_printactive = 1

        # if the list is empty then print no active flights
        if(checker_printactive==0):
            print_active.append("No active flights")
            return print_active
        #and sort it based on flight_id per project requirement
        #https://docs.python.org/3/howto/sorting.html
        print_active2.sort(key=lambda print_active2: print_active2.flight_id)

        #from the sorted list of all flights
        for active_flights in print_active2:
            #if either runway_id or end_time/eta or the start_time is None, print -1 instead(x,y,z are temps so that the actual None structure the flights have won't be damaged)
            if(active_flights.runway_id == None):
                x = -1
            else:
                x = active_flights.runway_id

            if(active_flights.end_time == None):
                y = -1
            else:
                y = active_flights.end_time

            if(active_flights.start_time == None):
                z = -1
            else:
                z = active_flights.start_time

            #print the list of sorted active flights
            # print(f"[flight{active_flights.flight_id}, airline{active_flights.airline_id}, runway{x}, start{z}, ETA{y}]")
            print_active.append(f"[flight{active_flights.flight_id}, airline{active_flights.airline_id}, runway{x}, start{z}, ETA{y}]")
        
        #output returned as final result
        return print_active

    #since this is the base idea of most if not all functions, instead of doing them one by one in each function I call tick instead
    #advancing the tyme of the system into the current time
    def tick(self, current_time):
        #update time
        self.current_time = current_time
        #run settle/phase1 with the new current time
        x = self.phase1(current_time)
        #do the reschedule/phase2
        x += self.phase2()
        return x

    #the number of new runways, which will be available at time point "time"
    def addrunways(self, new_count, time):
        #if there is no positive number of runways on first input, then print error
        if(new_count<=0):
            # print("Invalid input. Please provide a valid number of runways.")
            return ["Invalid input. Please provide a valid number of runways."]
        
        #if there is add the runway
        else:
            #do the current_time/settle/reschedule using tick()
            landed_list = self.tick(time)

            #update the number of total runways by adding up to it
            self.total_runways = self.total_runways + new_count
            #print(f"Additional {new_count} Runways are now available")

            #print the project required message
            landed_list.append(f"Additional {new_count} Runways are now available")
            
            #and do another reschedule now that there are new runways
            landed_list += self.phase2()
            return landed_list
        

    #submitting a new flight into the system, which takes all obligatory data for flight to initialize
    def submitflight(self, flight_id, airline_id, submit_time, priority, duration):
        #update the time and do settle + reschedule
        self.current_time = submit_time
        submit_flight = self.tick(self.current_time)
        checker_check_checker = 0

        #if there is a flight_id with same value, then we have a duplicate error
        for flight in self.flight.values():
            if(flight.flight_id == flight_id):
                checker_check_checker = 1
        if(checker_check_checker == 1):
            # print("Duplicate FlightID")
            submit_flight.append("Duplicate FlightID")

            return submit_flight
        #if not, we can assign create a new "flight" and assign its values accordingly
        else:
            new_flight = flight_class()
            new_flight.flight_id = flight_id
            new_flight.airline_id = airline_id
            new_flight.submit_time = submit_time
            new_flight.priority = priority
            new_flight.duration = duration
            #the default status will be pending
            new_flight.status = "pending"
            #rest is defined optional in data_structure.py

            #add the new flight to the list of flights
            self.flight[flight_id] = new_flight

            #unlike the rest of the functions doing reschedule later causes the list of print statements to get confused
            #so I do phase2/reschedule beforehand here and save its results
            temporary_phase2_saver = self.phase2()
            
            #print the new added flight with it's supposed ETA/end_time
            if(new_flight.end_time == None):
                # print(f"Flight {flight_id} scheduled - ETA : -1")
                submit_flight.append(f"Flight {flight_id} scheduled - ETA: -1")
            else:
                #print(f"Flight {flight_id} scheduled - ETA : {new_flight.end_time}")
                submit_flight.append(f"Flight {flight_id} scheduled - ETA: {new_flight.end_time}")

            #we can now update with the result from phase2(rescheduling)
            submit_flight += temporary_phase2_saver
            return submit_flight

    #change the priority of the flight
    def reprioritize(self,current_time, flight_id, updated_priority):
        #do the update_time, settle, reschedule
        reprioritize = self.tick(current_time)


        #a default value assigned to flight to check whether the flight exists in the first place
        the_flight = -67
        for flight in self.flight.values():
            if(flight.flight_id == flight_id):
                the_flight = flight

        if(the_flight == -67):
            # print(f"Flight {flight_id} not found")
            reprioritize.append(f"Flight {flight_id} not found")
            return reprioritize
        if(the_flight.status == "inprogress" or the_flight.status == "landed"):
            # print(f"Cannot reprioritize. Flight {flight_id} has already departed")
            reprioritize.append(f"Cannot reprioritize. Flight {flight_id} has already departed")
            return reprioritize
        
        #update the priority to the new number
        the_flight.priority = updated_priority
        
        #Print the project required statement
        # print(f"Priority of Flight {flight_id} has been updated to {updated_priority}")
        reprioritize.append(f"Priority of Flight {flight_id} has been updated to {updated_priority}")

        #and do the reschedule based on the update
        reprioritize += self.phase2()
        return reprioritize
    
    #cancel the flight, only needs the flight_id
    #and the time to make sure cancellation can happen in the first place
    def cancelflight(self, flight_id, current_time):
        #do the time update, settle, and reschedule
        cancelflight = self.tick(current_time)

        #random number, if not changed, means there were no such flight_id in the list
        the_flight = -505
        for flight in self.flight.values():
            if(flight.flight_id == flight_id):
                the_flight = flight
        if(the_flight == -505):
            # print(f"Flight {flight_id} does not exist")
            cancelflight.append(f"Flight {flight_id} does not exist")
            return cancelflight
        
        #if the flight is already inprogress or finished you can't really cancel it as it's too late
        if(the_flight.status == "inprogress" or the_flight.status == "landed"):
            # print(f"Cannot cancel. Flight {flight_id} has already departed")
            cancelflight.append(f"Cannot cancel. Flight {flight_id} has already departed")
            return cancelflight
        
        #print the flight to be cancelled
        # print(f"Flight {flight_id} has been canceled")
        cancelflight.append(f"Flight {flight_id} has been canceled")

        #delete the flight from the list of flights
        self.flight.pop(flight_id)
        #self.flight.pop(flight_id, None??)

        #and do another reschedule based on the new updates
        cancelflight += self.phase2()
        return cancelflight
    
    #hold the flights whose airline_id within the given range
    def groundhold(self, airline_low, airline_high, current_time):

        #possible invalid input
        if(airline_high<airline_low):
            groundhold = []
            # print("Invalid input. Please provide a valid airline range.")
            groundhold.append("Invalid input. Please provide a valid airline range.")
            return groundhold
        
        #if the input is valid:
        else:
            #do the current_time, settle, and reschedule

            #groundhold will hold the prints, groundhold2 is the actual list of flights that will be held
            groundhold = self.tick(current_time)
            groundhold2 = []

            #the flight needs to be pending/scheduled and needs to be not have been started already
            #when these conditions have been met, we can add the airline_ids that are in the interval
            for flight in self.flight.values():
                if(flight.status == "pending" or flight.status == "scheduled") and (flight.start_time == None or flight.start_time - current_time>0):
                    if flight.airline_id>=airline_low and flight.airline_id<= airline_high:
                        groundhold2.append(flight.flight_id)
            
            #pop all the flights in the interval
            for flight_id in groundhold2:
                self.flight.pop(flight_id, None)
            
            #the print statement
            # print(f"Flights of the airlines in the range {[airline_low, airline_high]} have been grounded")
            groundhold.append(f"Flights of the airlines in the range {[airline_low, airline_high]} have been grounded")
            
            #reschedule based on the update
            groundhold += self.phase2()
            return groundhold

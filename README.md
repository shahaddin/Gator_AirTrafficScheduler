# Gator Air Traffic Slot Scheduler

A command-driven simulator that schedules flight takeoff/landing requests across multiple runways. The scheduler advances “system time”, lands completed flights, and (re)builds a deterministic schedule for all *unsatisfied* flights using priority + tie-break rules.

## Key features

* Deterministic greedy scheduling:

  * Picks the next flight by **highest priority**, then **earlier submit time**, then **smaller flightID**
  * Assigns it to the runway with **earliest nextFreeTime**, tie-breaking by **smaller runwayID**
* Supports operations:

  * `Initialize(runwayCount)`
  * `SubmitFlight(flightID, airlineID, submitTime, priority, duration)`
  * `CancelFlight(flightID, currentTime)`
  * `Reprioritize(flightID, currentTime, newPriority)`
  * `AddRunways(count, currentTime)`
  * `GroundHold(airlineLow, airlineHigh, currentTime)`
  * `PrintActive()`
  * `PrintSchedule(t1, t2)`
  * `Tick(t)`
  * `Quit()`

## Data structures (from-scratch where required)

* Max Pairing Heap (two-pass) for pending-flight priority ordering
* Binary Min-Heap for runway availability ordering
* Binary Min-Heap for completion/timetable ordering
* Hash tables for flight lookup and airline indexing

## Build

This project is intended to be built via `make` and produce an executable named:

* `gatorAirTrafficScheduler`

```bash
make
```

## Run

The program takes the **input file name as a command-line argument**.

### Python

```bash
python3 gatorAirTrafficScheduler path/to/test1.txt
```

## Input format

* A plain text file
* **One operation per line**, formatted like `OperationName(arg1, arg2, ...)`
* The program stops when it encounters `Quit()`

Example:

```text
Initialize(2)
SubmitFlight(201, 1, 0, 5, 4)
Tick(4)
Quit()
```

## Output format

* All output is written to a text file named:

  * `<input_filename>_output_file.txt`
* Example: `test1.txt` → `test1_output_file.txt`

## Notes

* Run on UF’s environment (or any Linux/macOS setup with the appropriate compiler/interpreter).
* Output must match the exact formatting expected by the autograder.

## Academic integrity

This repository contains an academic course project. Please do not copy/paste it for graded submissions.

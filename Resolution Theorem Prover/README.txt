 The code is written in python:
How to compile the code?
1. For running Two pointer based resolution
		prover.py <method> <theorem> <goal> 
		<theorem> = rr, custom, harmonia, howl, test
		<method> =  two_pointer
		<goal> = a number
		For eg: prover.py two_pointer rr 6
				prover.py two_pointer harmonia 6
				prover.py two_pointer howl 6
				prover.py two_pointer custom 6
				prover.py two_pointer test 4

2. For running Two pointer based resolution
		prover.py <method> <theorem> 
		<theorem> = rr, custom, harmonia, howl, test
		<method> =  two_pointer
		For eg: prover.py unit rr 
				prover.py unit harmonia 
				prover.py unit howl 
				prover.py unit custom 
				prover.py unit test 
	where:
		rr stands for Coyote and Roadrunner
		custom stands for Drug dealer and customs official
		howl stands for howling hounds
		harmonia stands for Harmonia
		test stands for my theorem
		two_pointer: Two pointer based resolution
		unit: unit preference based resolution



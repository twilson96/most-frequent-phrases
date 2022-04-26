This Python (3.8) program prints the 100 most common three word sequences from a text file, ignoring punctuation.
Text files containing the novel Moby Dick are provided as an example, but any text file can be used.

** How to run from command line
	Docker:

		1. (Optional) Copy any text files to parse to the project directory (contains moby_dick.txt and moby_dick_unicode.txt by default)
		2. From the project directory, build docker image (docker build . -t sequences)
		3. Run in docker container (docker run -t sequences python main.py <file path> <any additional file paths separate by spaces>)

	Python:

		python main.py <file path> <any additional file paths separate by spaces>

	Linux stdin to Python:

		cat <file path> <any additional file paths separate by spaces> | python main.py

The project directory contains moby_dick.txt, so you can, for example, run:

	docker run -t sequences python main.py moby_dick.txt

...which will have the following output on the first three lines:

	the sperm whale - 85
	the white whale - 76
	of the whale - 70

Or, if you wanted to try it with multiple files, you can run:

	docker run -t sequences python main.py moby_dick.txt moby_dick.txt

...which will have the following output on the first three lines:

	the sperm whale - 170
	the white whale - 152
	of the whale - 140

It can also parse unicode! For example, if running with the provided moby_dick_unicode.txt (which replaces 'a' with 'ä'), the first three lines are:

	the sperm whäle - 85
	the white whäle - 76
	of the whäle - 70
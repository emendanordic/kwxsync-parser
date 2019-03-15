README: kwxsync_parser.py

Uses itertools.combinations to convert a single kwxsync command into many kwxsync commands.
sleep and progress indicator features exists to allow you to pause between commands and echo progress to the console log.

Developed with Python v2.7.10

Example usage (Mac OS):

 $ python kwxsync_parser.py -c '--statuses "Analyze","Ignore","Not a problem","Fix","Fix in Next Release","Defer","Filter" --last-sync "05-03-2016 00:00:00" --host example.host --port 8080' -p 'PROJ_1 PROJ_2 PROJ_3 PROJ_4'
 
Example usage (Windows):

 $ python kwxsync_parser.py -c "--statuses 'Analyze','Ignore','Not a problem','Fix','Fix in Next Release','Defer','Filter' --last-sync '05-03-2016 00:00:00' --host example.host --port 8080" -p "PROJ_1 PROJ_2 PROJ_3 PROJ_4"

This will write 6 kwxsync commands to the file 'kwxsync_commands.out' in the same directory as the command was run. Each command is unique and performs a kwxsync over two projects.

Known limitations:
    - The script is not currently OS agnostic, requiring different inputs depending on the OS in use (note the differing use of " and ' above)
    - The script currently only outputs 2-length combinations.


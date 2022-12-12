Presentation Video URL:
https://www.youtube.com/watch?v=hfLegmG0gpQ

Demo Video URL:
https://www.youtube.com/watch?v=oi3uoW_KC-c

Code URL:
https://github.com/zhifeil/VotingSystem


This is a decentralized e-voting application based on Homomophoc encryption-pallier, implemented by Python

# Environment

Python 3

# library

inquirer
random
gmpy2
time
hashlib

# Compile and run

This command works for Linux.

1. Clone git project file and make a command window directory as this file location
2. On the command line window, run the command  "python3 VotingSystem.py"

(you may need to use the commands: pip3 install inquirer; pip3 install gmpy2 to install  inquirer library and gmpy2 library)

If you finished an election and want to start another new election, please remember to delete encrypted_votes.txt before start another new election.


# Local storage

For each election, there is a 'encrypted_votes.txt' file to store encrypted votes and hash value.

# Structure of vote

Suppose there are two candidates C_1,C_2,  then the vote is a hex num V=V_1||V_2. 
For example, V=0001||0010 represents one vote for C_1 and two votes for C_2.
Therefore, for our case, each candidate can receive a maximum of 15 votes.


If you have any quesitons, please check our demo video https://www.youtube.com/watch?v=oi3uoW_KC-c about two test cases(1. normal voting process and 2. if someone has already tampered with encrypted_votes.txt file) or contact us at zhifeil@sfu.ca

Thanks a lot.



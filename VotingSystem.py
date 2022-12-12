import inquirer
import random
import gmpy2 as gy
import time
import hashlib
def Gen_key(length):
	s = gy.random_state(int(time.time()))
	p=gy.mpz_urandomb(s,length)
	if not gy.is_prime(p):
		p=gy.next_prime(p)
	q=gy.mpz_urandomb(s,length)
	if not gy.is_prime(q):
		q=gy.next_prime(q)
	n=p*q
	g=n+1
	Lambda=(p-1)*(q-1)
	L=gy.powmod(g,Lambda,n**2)
	mu=gy.invert(gy.mpz((L-1)//n),n)
	Pk=(n,g)
	Vk=(Lambda,mu)
	return (Pk,Vk)

def clearTerminal():
    print(chr(27) + "[2J") # clear terminal
    
def print_Votes(Votes): # print result table according to integer Votes
	votes=[0 for i in range(8)]
	for i in range(8):
		votes[7-i] = Votes&0b1111
		Votes=Votes>>4
	clearTerminal()
	print("The tabulation of the election results:")
	print("+------------------------------------+")
	print("|","Candiate    "," | ", "Number of votes")
	print("+------------------------------------+")
	for i in range(8):
		print("|",'candidate ',str(i+1)," |     ",votes[i])
	print("+------------------------------------+")
# encrypt value using Public key Pk 
def paillier_encrypt( Pk , value):
	n,g = Pk
	random_number=gy.mpz_random(gy.random_state(int(time.time())), n )
	while gy.gcd(random_number,n)!=1:
		random_number=random_number+1
	ciphertext = (gy.powmod(g, value, n ** 2) * gy.powmod(random_number, n, n ** 2) % (n ** 2))
	return ciphertext

#decrypt value using private key vk 
def paillier_decrypt(Vk,PK,ciphertext):
	(Lambda,mu)= Vk
	(n,g) = Pk
	m = gy.mpz((gy.powmod(ciphertext, Lambda, n ** 2)-1)//n)*mu % n
	return m
# Voters vote for candidates
def Vote(Pk):
	while (True):
		votes=[0b0000 for i in range(8)] # initialization
		print("===================================")
		print("Voting System")
		print("===================================")
		print("Welcome voter!")
        	#Candiate 1 , Candiate 2 ..... Candiate 8
		choices=['Candidate 1', 'Candidate 2','Candidate 3','Candidate 4','Candidate 5','Candidate 6','Candidate 7','Candidate 8']
		selected_candidate = inquirer.list_input("Select your choice for Mayor ?",choices=choices)
		clearTerminal()
		print("You have  selected : " + selected_candidate)
		
		#1 generate the vote
		votes[choices.index(selected_candidate)]=0b0001
		Vote=0
		for i in range(8):
			Vote=(Vote<<4)+votes[i]
		#print(bin(Vote))
		encrypted_vote=paillier_encrypt( Pk, Vote )
		digest=hashlib.sha256(str(encrypted_vote).encode()).hexdigest()
		#3 add hexdigest by SHA256
		print("Here is copy of your encrypted vote")
		print(encrypted_vote)
		with open("encrypted_votes.txt", "a") as f:
			f.write(str(encrypted_vote)+" "+digest+"\n")
			print("We've encrypted your vote and stored it and its hash value in file: enctypted_votes.txt" , end="\n")
			time.sleep(2)
			print("ok!",flush=True)
		if_continue = inquirer.list_input("Whether the voting process is finished ?",choices=['Yes','No'])
		if if_continue=='Yes':
			return
		for i in range(2):
			time.sleep(1)
			print("\rThe terminal will reset in : {:d} seconds".format(2-i),end="", flush=True)
		clearTerminal()
#Voters vote for candidates		
def count(Pk,Vk):
	encrypted_Votes=1
	n,g = Pk
	with open("encrypted_votes.txt", "r") as f:
		for line in f.readlines():
			line = line.strip('\n')
			encrypted_vote,digest=line.split()
			if hashlib.sha256(str(encrypted_vote).encode()).hexdigest()!=digest:
				print("Wrong! file has been modified!")
				return
			encrypted_vote=int(encrypted_vote)
			#print(vote)
			encrypted_Votes=encrypted_vote*encrypted_Votes%n**2
	print("Yes! File has not been modified!")
	Votes=paillier_decrypt(Vk,Pk,encrypted_Votes)
	print_Votes(Votes)
if __name__ == '__main__':
	(Pk,Vk)=Gen_key(100)
	Vote(Pk)
	count(Pk,Vk)

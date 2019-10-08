import random,sys,copy
iterations = 0
possible = True
randomRestarts = 0
stepsClimbedInRestartStrategy = 0
passedboard = None

#Printing the configuration of the N-Queen Puzzle 
def Print_config(state):
   for l in range(0,N):
          for m in range(0,N):
              if m < N-1:
                  print(state[l][m], end=" ")
              elif(m == N-1):
                  print(state[l][m], end="\n") 
 
#Class for the Queen
class queen_puzzle:
  def __init__(self, search_type, iterations, possible):
    #Initializing the required variables and counters
    self.totalruns = iterations
    self.totalsucc = 0
    self.totalfail = 0
    self.stepforsucc = 0
    self.stepforfail = 0
    self.sidemove = 0
    
    self.possible = possible
    for i in range(0,iterations):
      if self.possible == True:
        print ("\n============================")
        print ("OUTPUT FOR RUN:",i+1)
        print ("============================")
      self.queen_board = board(passedboard)
      self.cost = self.attack_pair_calc(self.queen_board)
      #Call for each type of hill climbing algorithm
      if (search_type == 1):
          self.hill_Climbing()
      elif (search_type == 2):
          self.sideways_Move()
      elif (search_type == 3):
          self.random_Restart_without_sidemove()
      elif (search_type == 4):
          self.random_Restart_with_sidemove()
 
#Definition for the Steepest hill climbing Algorithm
  def hill_Climbing(self):
    totalnumsteps = 0
    while 1:
      current_attacks = self.cost
      #Breaking if the random initial state itself is a sucess state
      if self.cost == 0:
          break
      #Call to generare the lower cost sucessesor
      self.get_lowercost_board()
      if (current_attacks == self.cost):
        self.totalfail += 1
        self.stepforfail += totalnumsteps
        if totalnumsteps == 0:
            self.stepforfail += 1
        break
      totalnumsteps += 1
      if self.possible == True:
        print ("\nNumber of attack pairs:", (int)(self.attack_pair_calc(self.queen_board)))
        Print_config(self.queen_board.board)
      if (self.cost == 0):
          break
    # If Failure is encountered
    if self.cost != 0:
      if self.possible == True:
        print ("\n*****NO SOLUTION FOUND*****")
    # If Sucess is encountered
    else:
      if self.possible == True:
        print ("\n*****SOLUTION FOUND*****")
      self.totalsucc += 1
      self.stepforsucc += totalnumsteps
    return self.cost

#Definition for the Sideways hill climbing Algorithm
  def sideways_Move(self):
    totalnumsteps = 0
    sidemove = 0
    while 1:
      current_attacks = self.cost
      current_board = self.queen_board
      #Breaking if the random initial state itself is a sucess state
      if self.cost == 0:
          break
      #Call to generare the sucessesor board
      #This can return both equal heuristic board or lower heuristic board
      self.get_sucessor_board()
      if current_board == self.queen_board:
          self.stepforfail += totalnumsteps
          self.totalfail += 1
          if totalnumsteps == 0:
            self.stepforfail += 1
          break
      if current_attacks == self.cost:
        sidemove += 1
        if sidemove == 100:
            self.stepforfail += totalnumsteps
            self.totalfail += 1
            break
      elif(current_attacks > self.cost):
          sidemove = 0
      totalnumsteps += 1
      if self.possible == True:
        print ("\nNumber of attack pairs:", (int)(self.attack_pair_calc(self.queen_board)))
        Print_config(self.queen_board.board)
      if self.cost == 0:
        break
    if self.cost != 0:
      if self.possible == True:
        print ("\n*****NO SOLUTION FOUND*****")
    else:
      if self.possible == True:
        print ("\n*****SOLUTION FOUND*****")
      #Incrementing the count for number of success incurred and total steps taken for each successful iteration
      self.totalsucc += 1
      self.stepforsucc += totalnumsteps
    return self.cost

#Definition for the Random Restart without sideways allowing  hill climbing Algorithm  
  def random_Restart_without_sidemove(self): 
      while 1:        
        current_attacks = self.cost
        current_board = self.queen_board
        #Breaking if the random initial state itself is a sucess state
        if self.cost == 0:
            break
        #Call to generare the sucessesor board
        self.get_lowercost_board()
        #Check and logic for random Restart
        if (current_board == self.queen_board) or ((current_attacks == self.cost) & (self.cost != 0)):
          self.queen_board = board(passedboard)
          global randomRestarts
          #Increment the Random Restarts counter
          randomRestarts += 1 
          self.cost = self.attack_pair_calc(self.queen_board)               
        elif (self.cost < current_attacks):  
            if self.possible == True:
                print ("\nNumber of attack pairs:", (int)(self.attack_pair_calc(self.queen_board)))
                Print_config(self.queen_board.board)
        global stepsClimbedInRestartStrategy
        #Increment the Steps counter in Random restart Hill climbing algorithm
        stepsClimbedInRestartStrategy += 1 
        if self.cost == 0:
          break     
      if self.possible == True:
          print ("\n*****SOLUTION FOUND*****")
           #Incrementing the count for number of success incurred
      self.totalsucc += 1     
      return self.cost
  
#Definition for the Random Restart with sideways allow hill climbing Algorithm  
  def random_Restart_with_sidemove(self):
      sidemove = 0
      while 1:        
        current_attacks = self.cost
        current_board = self.queen_board
        #Breaking if the random initial state itself is a sucess state
        if self.cost == 0:
            break
        #Call to generare the sucessesor board
        self.get_sucessor_board()
        #Check and logic for random Restart
        if current_board == self.queen_board:
          self.queen_board = board(passedboard)
          global randomRestarts
          #Increment the Random Restarts counter
          randomRestarts += 1 
          self.cost = self.attack_pair_calc(self.queen_board) 
        if current_attacks == self.cost:
          sidemove += 1
          if sidemove == 100:
            self.queen_board = board(passedboard)
            #Increment the Random Restarts counter
            randomRestarts += 1 
            self.cost = self.attack_pair_calc(self.queen_board)
        elif(current_attacks > self.cost):
          sidemove = 0
        global stepsClimbedInRestartStrategy
        #Increment the Steps counter in Random restart Hill climbing algorithm
        stepsClimbedInRestartStrategy += 1    
        if self.possible == True:
          print ("\nNumber of attack pairs:", (int)(self.attack_pair_calc(self.queen_board)))
          Print_config(self.queen_board.board)
        if self.cost == 0:
          break     
      if self.possible == True:
          print ("\n*****SOLUTION FOUND*****")
           #Incrementing the count for number of success incurred
      self.totalsucc += 1     
      return self.cost
 
    #Print Definition exclsive to each type of Hill climbing algorithm
  def print_stats(self):
    print ("\nTotal Runs: ", self.totalruns)
    print ("Total Success: ", self.totalsucc)
    print ("Success Percentage: ", (float(self.totalsucc)/float(self.totalruns))*100,"%")
    
    #Print statements for Steepest Hill climbing Algorithm 
    # & Sideways Hill climbing Algorithm
    if(search_type == 1) or (search_type == 2):
        print ("Total Fail: ", self.totalfail)
        print ("Fail Percentage: ", (float(self.totalfail)/float(self.totalruns))*100,"%")
        if(self.totalsucc >= 1):
          print ("Average number of steps in sucess: ", float(self.stepforsucc)/float(self.totalsucc))
          print ("Total Steps for Success: ", self.stepforsucc)
        if(self.totalfail >= 1):
          print ("Total Steps for Fail: ", self.stepforfail)
          print ("Average number of steps in fail: ", float(self.stepforfail)/float(self.totalfail))
          
    #Print statements for Random Restart Hill climbing Algorithm
    if(search_type == 3) or (search_type == 4):
        print ("Number of random restarts:", randomRestarts)
        print ("Average number of random restarts: ", float(randomRestarts)/float(self.totalruns))
        print ("Average number of steps: ", float(stepsClimbedInRestartStrategy)/float(self.totalruns));
    
   #Definition for calculating the number of attack pairs     
  def attack_pair_calc(self, temp_board):
    #these are separate for easier debugging
    straight_attacks = 0
    diagonal_attacks = 0
    for i in range(0,N):
      for j in range(0,N):
        #if this node is a queen, calculate all attacks pairs
        if temp_board.board[i][j] == "Q":
          #We will subtract the total cost by 2 so that we don't count the self state
          straight_attacks -= 2
          for k in range(0,N):
            if temp_board.board[i][k] == "Q":
              straight_attacks += 1
            if temp_board.board[k][j] == "Q":
              straight_attacks += 1
          #calculation of all diagonal attacks
          k, l = i+1, j+1
          while k < N and l < N:
            if temp_board.board[k][l] == "Q":
              diagonal_attacks += 1
            k +=1
            l +=1
          k, l = i+1, j-1
          while k < N and l >= 0:
            if temp_board.board[k][l] == "Q":
              diagonal_attacks += 1
            k +=1
            l -=1
          k, l = i-1, j+1
          while k >= 0 and l < N:
            if temp_board.board[k][l] == "Q":
              diagonal_attacks += 1
            k -=1
            l +=1
          k, l = i-1, j-1
          while k >= 0 and l >= 0:
            if temp_board.board[k][l] == "Q":
              diagonal_attacks += 1
            k -=1
            l -=1
    return ((diagonal_attacks + straight_attacks)/2)
 
  #this function tries moving every queen to every spot, with only one move
  #and returns the move that has the least number of attacks pairs
  def get_lowercost_board(self):
    least_cost = self.attack_pair_calc(self.queen_board)
    most_desirable = self.queen_board
    #We move one queen at a time
    for q_col in range(0,N):
      for q_row in range(0,N):
        if self.queen_board.board[q_row][q_col] == "Q":
          #We get the lowest cost configuration by moving each queen in its respective column
          for m_row in range(0,N):
              if self.queen_board.board[m_row][q_col] != "Q":
                #Queen is placed in empty slot of each column
                test_board = copy.deepcopy(self.queen_board)
                test_board.board[q_row][q_col] = "."
                test_board.board[m_row][q_col] = "Q"
                test_board_cost = self.attack_pair_calc(test_board)
                if test_board_cost < least_cost:
                  least_cost = test_board_cost
                  most_desirable = test_board
    self.queen_board = most_desirable
    self.cost = least_cost
 
  def get_sucessor_board(self):
    equal_h_count = 0
    equi = {}
    presentcost = self.attack_pair_calc(self.queen_board)
    least_cost = self.attack_pair_calc(self.queen_board)
    most_desirable = self.queen_board
    #move one queen at a time, the optimal single move by brute force
    for q_col in range(0,N):
      for q_row in range(0,N):
        if self.queen_board.board[q_row][q_col] == "Q":
          #get the lowest cost by moving this queen
          for m_row in range(0,N):
              if self.queen_board.board[m_row][q_col] != "Q":
                #try placing the queen here and see if it's any better
                test_board = copy.deepcopy(self.queen_board)
                test_board.board[q_row][q_col] = "."
                test_board.board[m_row][q_col] = "Q"
                test_board_cost = self.attack_pair_calc(test_board)
                if test_board_cost < least_cost:
                  least_cost = test_board_cost
                  most_desirable = test_board
                if test_board_cost == presentcost:
                  equi[equal_h_count] = test_board
                  equal_h_count += 1
    if least_cost == presentcost:
        print("Successors with hueristic same as that of the current state:", equal_h_count)
        if(equal_h_count == 1):
            most_desirable = equi[0]
        elif(equal_h_count > 1):
            rand_ind = random.randint(0,equal_h_count - 1)
            print("Random index to choose one of the same heuristic ssuccessor:", rand_ind)
            most_desirable = equi[rand_ind]
    self.queen_board = most_desirable
    self.cost = least_cost
 
class board:
  def __init__(self, list=None):
    if list == None:
      self.board = [["." for i in range(0,N)] for j in range(0,N)]
      #initialize queens at random places
      for j in range(0,N):
        rand_row = random.randint(0,N-1)
        if self.board[rand_row][j] == ".":
          self.board[rand_row][j] = "Q"
      print("Initial State:")
      Print_config(self.board)
    


if __name__ == "__main__":
  print ("\n**********Welcome to N Queen Solver*********\n")
  print ("Choose \"1\" if you wish to solve default 8-queens puzzle, or choose \"2\" to assign your desired puzzle.")
  choice = int(input())
  if (choice == 1):
      N = 8      
  elif (choice ==2):
      print ("\nPlease Enter the required N size: ")
      N = int(input())
  else:
      print ("\nInvalid Choice")
      print ("\nTaking the default 8-queens puzzle\n")
  print ("\nChoose \"1\" if you wish to solve the puzzle for 100 runs, or choose \"2\" to assign your desired number of run interations. ")
  iterationChoice = int(input())
  if (iterationChoice == 1):
      iterations = 100      
  elif (iterationChoice == 2):
      print ("\nPlease Enter the required number of runs: ")
      iterations = int(input())
  else:
      print ("\nInvalid Choice")
      print ("\nTaking the default value of 100 iterations: \n")
  print ("\nChoose \"1\" Steepest Ascent Hill Climbing, or \"2\" Hill Climbing with Sideways Move, or \"3\" Random-Restart Hill Climbing without Sidemove,or \"4\" Random-Restart Hill Climbing with Sidemove")
  searchStrategy = int(input())
  if (searchStrategy == 1):
      search_type = 1      
  elif (searchStrategy == 2):      
      search_type = 2
  elif (searchStrategy == 3):      
      search_type = 3   
  elif (searchStrategy == 4):
      search_type = 4
  else:
      print ("\nInvalid Choice")
      print ("\nTaking the default value of 100 iterations: \n")
 
  queen_board = queen_puzzle(search_type, iterations, possible)
  queen_board.print_stats()

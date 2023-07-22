# P4-HTN-Planning-for-Minecraft
**P4: HTN Planning for Minecraft**  
  - **Team Member**
    - Zhuo Chen
    - Yuanzheng Ji
   
  - **Requirements for this assignment**  
    - [x] (1) Solve and submit a solution for this task:  
                ●	Given {}, achieve {'wood': 12} [time <= 46]
    - [ ] (2) Create HTN operators from the supplied json scripts
    - [ ] (3) Create HTN methods from the supplied json scripts
    - [ ] (4) Create a mechanism to turn json problem descriptions into HTN problems by initializing initial resource state and goals (top level task).
    - [ ] (5) Solve and submit solutions for these test cases. Your code must programmatically generate operators and methods using make_operator and make_method, as described in (2) and (3) above.
    - [ ] (6)  (Extra Credit) Define the most complicated case your HTN planner can solve in 30 seconds of real-world time.
  - **Submission**  
    -	manualHTN.py, which should solve case (1) from the section above.  
    -	autoHTN.py, which should solve cases in (5) from the section above.  
        -	autoHTN.py must programmatically create methods and operators
    - A README file that describes the heuristics you chose/programmed.  
    - (Optional Extra Credit) A file custom_case.txt that states your chosen problem for (6) in the format “Given x, achieve y” and the solution found by your HTN planner.  You should identify the task, the solution, the time cost in recipe time and the time cost in real-world time.    
        - You can build on  provided test cases, but do not reuse one as is.
  
  - **Code Modified**
    - **For manualHTN.py**  
      - We modified some code and improved the program. Now, the program can run Task 1 perfectly.  
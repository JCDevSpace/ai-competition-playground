## Self-Evaluation Form for Milestone 1

### General 

We will run self-evaluations for each milestone this semester.  The
graders will evaluate them for accuracy and completeness.

Every self-evaluation will go out into your Enterprise GitHub repo
within a short time afrer the milestone deadline, and you will have 24
hours to answer the questions and push back a completed form.

This one is a practice run to make sure you get


### Specifics 


- does your analysis cover the following ideas:

  - the need for an explicit Interface specification between the (remote) AI 
    players and the game system?
    
    Yes, in part three of our milestone we have a plan to integrate running arbitrary code to generate moves for the AI players. We were under the impression that the people entering the tournament would submit a snippet of code to our server and at the time of the tournament, we would run the submitted code along with all other entries to get the results of the game. Our plan to do this was to "run submitted code safely in a separate process" (milestone 3, pt2).

  - the need for a referee sub-system for managing individual games
  
  No, we did not specify a referee subsystem because we thought it was too low leel for the project. Based on our interpretation, we beleived that this ai tournament server would be able to host several games besides just fish so we did not get in to the specifics of the logic for different games that would run on the server.    


  - the need for a tournament management sub-system for grouping
    players into games and dispatching to referee components
    
    Yes we specified the need for tournament management subsystem. In the controller portion of our system.pdf we stated: "The server also handles the scheduling and running of the tournaments. Every so often it will check to see if a tournament has closed its sign up and then it will run the tournament." Even though do not say the words "tournament management sub-system" this is clearly in reference to that.

- does your building plan identify concrete milestones with demo prototypes:

  - for running individual games
  
  Yes in part 3 of our milestone, part of the plan is to construct actual game logic. We say "Build a game that allows for the integration of arbitrary code."

  - for running complete tournaments on a single computer 
  
  Yes, we planned to set up a system for running a tournament on the server in part 2 of our milestones. In that portion, we planned to build an "endpoint for clients to upload their AI code" and then later in milestone 3 we planned to build out the logic to run a tournament with the submitted code.


  - for running remote tournaments on a network
  
  No, we did not plan for this because we planned for users to upload code to our server which the server would run locally when the tournament entry closed. Since the code would be run locally on our server, there would be no reason for the clients to keep a connection up while the tournament was running.


- for the English of your memo, you may wish to check the following:

  - is each paragraph dedicated to a single topic? does it come with a
    thesis statement that specifies the topic?

  Yes, we break up our paragraphs into seperate concerns in our system.pdf. One for the model, one for the view, and one for the controller.

  - do sentences make a point? do they run on?
  
  Yes, we believe we were very concise in our description of the system and milestones.


  - do sentences connect via old words/new words so that readers keep
    reading?
    
    We believe that we drew the reader in with enticing words so that they continue to read such as "client code" and "database". later, we echoed these words when we more fully described them as part of a whole.


  - are all sentences complete? Are they missing verbs? Objects? Other
    essential words?
    
    Yes, we wrote in English sentences.


  - did you make sure that the spelling is correct? ("It's" is *not* a
    possesive; it's short for "it is". "There" is different from
    "their", a word that is too popular for your generation.)
    
    For the most part yes, but we did have one misuse of its in part 3 of our milestone. :)

The ideal feedback are pointers to specific senetences in your memo.
For PDF, the paragraph/sentence number suffices. 

For **code repos**, we will expect GitHub line-specific links. 



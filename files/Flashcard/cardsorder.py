# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 23:41:55 2020

@author: Anton
"""
import random
import _logging.log_module as log
import Flashcard.fc_functions as f2
def DetermineCardorder(self,USERINPUT):
    """
    USERINPUT: boolean, 
    - TRUE it will ask the user for input to determine
           the order in which the cards should be displayed.
    - FALSE, it will display them chronologically without userinput.
    """
    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC MODULE: nrcards = {len(self.CardsDeck)}")
    
    try:        
        """CARD ORDER"""
        ## determine cardorder based on user given input
        if USERINPUT == False:
            self.cardorder = range(self.nr_questions)  
        else:
            
            if not hasattr(self,'continueSession'): #look if variable even exists./ should be initialized
                self.continueSession = False
                        
            if self.continueSession == False:
                if self.nr_questions < len(self.CardsDeck):   
                    if self.chrono:
                        self.cardorder = range(self.nr_questions)    
                    else:
                        self.cardorder = random.sample(range(len(self.CardsDeck)),self.nr_questions) 
                else: 
                    ## If there are more questions than cards
                    # we would like to get every question about the same number of times, to do this we do sampling without
                    # replacement, then we remove a question if it is immediately repeated.
                    if self.chrono:
                        self.cardorder = list(range(len(self.CardsDeck)))*self.nr_questions
                        self.cardorder = self.cardorder[:self.nr_questions]
                    else:
                        cardorder = []
                        for i in range(len(self.CardsDeck)):   # possibly way larger than needed:
                            cardorder.append(random.sample(range(len(self.CardsDeck)),len(self.CardsDeck)))
                        cardorder = [val for sublist in cardorder for val in sublist]
                        SEARCH = True
                        index = 0
                        # remove duplicate numbers
                        while SEARCH:
                            if index == len(cardorder)-2:
                                SEARCH = False
                            if cardorder[index] == cardorder[index+1]:
                                del cardorder[index+1]
                                index += 1
                            index += 1    
                        self.cardorder = cardorder[:self.nr_questions] 
            else:
                f2.load_stats(self)  
        self.CardsDeck.set_cardorder(self.cardorder)            
    except:
       log.ERRORMESSAGE("Error: couldn't put the cards in a specific order")
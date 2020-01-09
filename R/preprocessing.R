
getParticipantData <- function(group, participant) {
  
  # home-target distance in pixels: 433.548
  
  rawparticipantdf <- read.csv(sprintf('data/%s/p%03d/COMBINED_%s_p%03d.csv', group, participant, group, participant), stringsAsFactors = FALSE)  
  rawparticipantdf$showcursor_bool <- as.logical(rawparticipantdf$showcursor_bool)
  rawparticipantdf$doaiming_bool <- as.logical(rawparticipantdf$doaiming_bool)
  
  ppdf <- NA
  
  unique.trials <- unique(participantdf$cutrial_no)
  
  for (trialno in unique.trials) {
    trialdf <- participantdf[which(participantdf$cutrial_no == trialno),]
    
    if (trialdf$showcursor_bool[1]) {
      # trim with a reach target criterion
      trialdf <- trimReach(trialdf = trialdf,
                           )
    } else {
      # trim with a hold criterion
      trialdf <- trimReach(trialdf = trialdf,
                           )
      
      
    }
    
    # get reach deviation
    
    # get aiming deviation (if any...)
    
    
    if (is.data.frame(ppdf)) {
      # when at least one trial is already added
      ppdf <- rbind(ppdf, trialdf)
    } else {
      # when it is still NA
      ppdf <- trialdf
    }
  }
  

  
  return(ppdf)
  
}
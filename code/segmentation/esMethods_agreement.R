library(tidyverse)
library(seewave)

## Gaussian Smooth Data
smooth_responses <- function(time_series, bandwidth, time = NULL, normalize = FALSE) {
  
  if (is.null(time)){
    time = 0:(length(time_series) - 1)
  }
  
  smoothed <- ksmooth(x = time, time_series, 'normal', bandwidth)
  
  if (normalize == FALSE){
    smoothed$y <- smoothed$y / max(smoothed$y, na.rm = TRUE)
  }
  
  return(smoothed$y)
}

## Calculate Peakiness

peakiness = function(y_vect, story_dur, adj.size = 0.1, bw = 'SJ', dens_hz = 1){
  
  # Get Distribution for Minimum Rugosity
  total_bps = length(y_vect)
  even_bps = seq(from = 0, to = story_dur, length.out = total_bps)
  
  # Get Distribution for Minimum and Actual Data
  temp = density(y_vect, bw = bw, adjust = 1, kernel = 'gaussian', n = story_dur * dens_hz, 
                 from = 1 / dens_hz, to = story_dur)
  
  pad_ts = ceiling(temp$bw * 2)
  y_dens = density(y_vect, bw = bw, adjust = adj.size, kernel = 'gaussian', n = ceiling((story_dur + 2 * pad_ts) * dens_hz), 
                   from = 1 / dens_hz - pad_ts, to = story_dur + pad_ts)
  min_y_dens = density(even_bps, bw = bw, adjust = adj.size, kernel = 'gaussian', n = ceiling((story_dur + 2 * pad_ts) * dens_hz), 
                       from = 1 / dens_hz - pad_ts, to = story_dur + pad_ts)
  
  # Calculate Rugosity
  min_rugosity = rugo(min_y_dens$y)
  act_rugosity = rugo(y_dens$y)
  peakiness = act_rugosity / min_rugosity
  
  result = list(density = y_dens, metrics = c(min_rugosity, act_rugosity, peakiness))
  return (result)
}


## Agreement Index

agreement_index = function(sample, group){
  
  # Calculate the correlation between sample and group timeseries
  corr = cor(sample, group, method = 'spearman')
  
  return (corr)
}

## Agreement Index

adjusted_agreement = function(sample, group){
  
  # Calculate the correlation between sample and group timeseries
  corr = cor(sample, group, method = 'spearman')
  
  # Calculate maximum possible correlation
  maxcorr = cor(sample[order(-sample)], group[order(-group)], method = 'spearman')
  
  # Calculate minimum possible correlation
  mincorr = cor(sample[order(sample)], group[order(-group)], method = 'spearman')
  
  # Calculate Agreement
  agreement = (corr - mincorr) / (maxcorr - mincorr)
  
  return (c(mincorr, maxcorr, corr, agreement))
}

##  Function to find the word number for a given time
find_word_number = function(time, word_times) {
  match_index = which(time >= word_times$time_start & time <= word_times$time_end)
  
  if (length(match_index) > 0) {
    return(word_times$word_number[match_index[1]])  # Take the first match if multiple
  } else {
    # No exact match found, find the nearest word
    diffs = pmin(abs(time - word_times$time_start), abs(time - word_times$time_end))
    min_diff_index = which.min(diffs)
    
    return(word_times$word_number[min_diff_index])
  }
}


## Produce Time Series

produce_time_series = function(responses, story_dur, step){
  
  # Calculate Sequence
  series = seq(0, story_dur[1], step)
  
  # Create Time Series
  responses = ifelse(series %in% round(responses, digits = 0), 1, 0)
  
  return (responses)
}


## Get Story Duration

story_duration = function(story_id, type){
  story1_word = 1669
  story2_word = 1521
  story3_word = 1740
  
  story_dur <- case_when(
    type == 'word' & story_id == 1 ~ story1_word,
    type == 'word' & story_id == 2 ~ story2_word,
    type == 'word' & story_id == 3 ~ story3_word,
  )
  
  return (story_dur)
}


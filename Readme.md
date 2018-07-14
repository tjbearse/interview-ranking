This script attempts to identify how interviewers are calibrated relative to eachother. The general approach is to use disagreement between interviewers in a loop to attempt to give them rough sorting to interviewer difficulty. Disagreements are directional and help to apply a rating to each interviewer (+ softer /- harder). Additional weighting and normalization helps to apply sorting transitively.

Interesting challenges with the problem:

* Interview loops are varied groups with a high number of judges. Rarely do we see the same pair of interviewers interview a large pool of candidates. It's hoped that transative comparison, while fuzzy, will help produce a ranking in such a dataset.
* True values of the bar and candidate skill are not discoverable. It's not possible to say from these comparisons where the bar is or which interviewers are most successful in relation to assessing the bar.
* Interviewers are not perfect judges, they are assumed to have some variance in their judgements. TODO to attempt to rate this based on comparisons.

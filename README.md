This script was made strictly for the purposes of reducing the likelihood of having the output of a Large Language Model bear a strong resemblance to the source material or prompt that was used to generate a given response.

I've found that by simply comparing the n-grams of the start (prompt) and finish (response) in the ballpark of, say, n-gram orders 2 through 10, one can easily identify substring similarities from the aforementioned prompt and response very quickly.

This is great for instances in which a user may use the output of an LLM to start the creative process (blog, letter, etc.) with the ultimate goal being to have the resultant piece bear little to no resemblance to the prompt(s) used to make the response(s).

LLM responses, at the time of this writing, are prone to have n-grams of orders 2 or more in common with the prompts used to generate them. This doesn't happen all the time. In fact, it happens very infrequently. However, when it does happen, and a piece of writing fails an LLM smell test, it can lead to unintended consequences on the part of the prompt engineer.

Prompts which involve quotes or the user (prompt-maker) presenting the LLM with text for the sake of comparison are the most likely to result in this reduction of LLM-response-heterogeneity.

Use-case(s):

#0:

Prompt: Write a(n) [insert document type here] about [insert topic here] as it pertains to the following: [insert excerpt from a pre-existing sample text]
Response: [insert response here]

Import both Prompt and Response to local .txt files, run the script (replacing the paths for prompt, response and output .csv respectively), and then make note of what is similar in both the prompt and response as detailed in the output .csv.

#1:

If you are 1) an LLM developer or 2) if you have access to the training data inputs utilized that an LLM used to produce a particular output then you could, ostensibly, compare any relevant training data and any associated prompts to an LLM's subsequent output.

#2:

If you are in a situation in which you must compare multiple drafts of, say, marketing materials for a commercial to be read or showcased using an electronic medium such as a podcast, radio or YouTube show and your ultimate objective is to sift out often used terminologies between said drafts with the goal of identifying potential weak points or areas in which draft(s) can be improved or altered.


This script was made strictly for the purposes of reducing the likelihood of having the output of a Large Language Model bear a strong resemblance to the source material or prompt that was used to generate the response.

I've found that by simply comparing the n-grams of the start (prompt) and finish (response) in the ballpark of, say, n-gram orders 2 through 10, one can easily identify substring similarities from the aforementioned prompt and response very quickly.

This is great for instances in which you may use the output of an LLM to start the creative process (blog, letter, etc.) and your ultimate goal is to have the resultant piece bear little to no resemblance to the prompts used to make the responses.

LLM responses, at the time of this writing, are prone to have n-grams of orders 2 or more in common with the prompts used to generate them. This doesn't happen all the time. In fact, it happens very infrequently. However, when it does happen, and a piece of writing fails an LLM smell test, it can lead to unintended consequences on the part of the prompt engineer.

Prompts which involve quotes or the user (prompt-maker) presenting the LLM with text for the sake of comparison are the most likely to result in this reduction of LLM-response-heterogeneity.

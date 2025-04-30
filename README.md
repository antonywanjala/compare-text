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

#3:

A key part of the process of feature extraction is finding the similarities between a representation of a file or piece of data and a known feature set. This script can aid in the process of performing these comparisons and arriving at what these common features are in, at the very least, a rudimentary yet effective capacity. Feature extraction is a process common to conventional compression and preprocessing techniques.

#4:

In the event that a subroutine has been identified as the culprit in a recent security breach, identifying which other parts of a codebase either 1) reference said subroutine or 2) implement parts of said subroutine's functionality can be isolated, at least in part, through this script's invocation. 

#5:

Finding redundancies in a codebase is an important part of making subroutines more efficient. The process of reducing the amount of time involved in finding any redundancies present in a codebase can be supplemented by this script.

#6:

The comparison of new content against a database of existing content and, in addition, the identification of copied, pirated or plagiarised material, thereby protecting intellectual property, are crucial facets of any organization's pipeline - especially those dealing with user generated content. Comparing items in these aforementioned databases is something that can be addressed by my script.

#7:

This script can identify recurring themes or sequences in user generated content, search queries or button input maps which all play a hand in the process of curating content recommendations for viewers.

#8:

Identifying duplicates or near-duplicates within large content libraries is also something that this scrip can address.

#9:

Contracts from different vendors sometimes share common clauses, obligations or verbiage. A script such as this one can aid in expediting the process of contract review and ensures key terms are consistently met.

#10:

Analysis of customer feedback from different channels (emails, surveys, reviews, etc.) for common issues or praise, processes addressed by this script, can help improve product quality and customer satisfaction.

#11

Have one of the files supplied to the script be a list of words, phrases or statements which the user wishes to evaluate the presence of (eg. strings commonly found in fraudulent documentation, common discrepancies, etc.) in any one of the remaining file arguments to be supplied to the script. The resultant output would reflect which items are common of the supplied documents.

#12

Determining popular elements in a series (akin to finding which n-grams two or more documents have in common) can also aid in the determination of which of these aforementioned elements are to remain in their decompressed state so as to reduce the amount of compute costs relegated to their subsequent decompression upon purchase by a given user or upon being accessed by a given user. Popular items being left in a decompressed state and less popular items being left in a compressed state. The aforementioned process can also be used to respond to seasonal trends, fads, etc. Elements that are in a compressed format incur lower costs when it comes to the amount of bandwidth required for their download. To add, in the event that these elements are made available in a digital storefront, a compressed format would also result in lower costs as far as server-side storage is concerned as well. 

#13

If you were making a blog article auto-publisher, you could use this script as a quality control measure, avoiding the publishing of articles which possess the repetition (over-emphasis, if you will) of phrases that are, say, 5 words in length or more. The reason why is because LLM's have a tendency to include generated titles within the title-article matricies they generate from time to time. Making a function that returns TRUE in the event a resultant title-article matrix falls into such a category can be a means of avoiding such a quality from making its way into a published blog timeline.

Script Overview: N-Gram Similarity & Redundancy Analysis
This script was developed to mitigate "output leakage" in Large Language Models (LLMs). It identifies instances where an LLM’s response bears a high structural resemblance to the user's prompt or source material.
By comparing n-gram sequences (orders 2 through 10) between the prompt (start) and response (finish), the tool quickly isolates substring overlaps. While infrequent, these overlaps can cause a piece of writing to fail the "LLM smell test," leading to unintended consequences for prompt engineers who require high-heterogeneity outputs.
Primary Workflow
1.	Identify: Isolate prompts containing quotes or reference texts, as these are most prone to mirroring.
2.	Process: Export the Prompt and Response to .txt files.
3.	Analyze: Run the script to generate a .csv output detailing specific similarities.
________________________________________
Applied Use Cases
I. Creative & Technical Writing
•	Draft Optimization (#2, #13): Compare multiple drafts of marketing materials (scripts for YouTube, podcasts, etc.) to identify repetitive terminology or "weak points" that require variation.
•	Quality Control (#13): In automated publishing, use the script as a gatekeeper. If an article repeats phrases of 5+ words (often caused by the LLM accidentally including the title within the body), the system flags the content as a "fail."
II. Development & Security
•	Codebase Maintenance (#4, #5, #18): Locate redundancies to improve efficiency or map the impact of a compromised subroutine by finding where its logic is replicated elsewhere in the codebase.
•	Model Evaluation (#1): For LLM developers, compare model outputs against specific training data subsets to measure "memorization" versus "generalization."
•	Feature Extraction (#3): Use n-gram comparison as a rudimentary but effective method for identifying common features during data preprocessing and compression.
III. Intellectual Property & Compliance
•	Plagiarism Detection (#6, #8): Protect IP by comparing user-generated content against databases of existing material to flag pirated or copied text.
•	Contract Review (#9): Expedite legal reviews by identifying standardized clauses and ensuring verbiage remains consistent across multiple vendor agreements.
•	Fraud Detection (#11, #15): Use "watchlist" files (containing known fraudulent strings or suspicious patterns) to scan documents for discrepancies or algorithmic domain-purchasing behavior.
IV. Resource Management & Data Strategy
•	Storage Optimization (#12): Identify high-frequency elements in a series to determine which should remain decompressed for fast access and which should be compressed to save bandwidth and server-side costs.
•	Corporate Strategy (#14, #16): Use terminology frequency distribution to ensure corporate strategy documents are sufficiently diverse, preventing "node sequence decay" and ensuring varied strategic outputs.
•	Customer Insights (#10, #15): Aggregate feedback across emails and reviews to identify recurring themes, complaints, or praise to guide product development.
________________________________________
Special Application: High-Volume Data Access System (#17)
•	Concept: A decentralized architecture for concurrent data retrieval using public platforms (like Google Blogger) as storage nodes.
•	Technical Pipeline: * Serialization: Source $\rightarrow$ Binary $\rightarrow$ Base64.
o	Encryption: The stream is segmented and secured via Fernet symmetric encryption.
o	Obfuscation: Encrypted chunks are interspersed with AI-generated text (e.g., "How to create a cryptocurrency") to bypass automated spam filters.
•	Metrics: Using 10 accounts with 100 posts each (approx. 20 MB per post), the system can manage a 2 GB daily stream, totaling ~730 GB annually.
•	Critical Security Note: This method publishes data to the open web. For proprietary data, users must utilize Draft Mode to ensure privacy. This architecture is intended for bandwidth efficiency an



#17

A Proprietary High-Volume Data Access System providing concurrent data retrieval and optimized bandwidth usage, suitable for retrieving files of any size.
Capacity: The system provides access to a concurrent data stream totaling 2 GB per day, yielding an annual potential of nearly 730 GB of data. Access Structure: This daily capacity is shared across a base of 10 user accounts, allowing
200 MB of access per user. The system leverages high-limit consumer platforms (Google Blogger) to decentralize
storage and maximize volume capacity. Data Pipeline Serialization and Encoding: The source file is converted to binary, then
encoded into Base64 format. Encryption and Segmentation: The Base64 stream is segmented into chunks, each secured using Fernet symmetric encryption. The decryption key is retained for later download. Publication: The encrypted Fernet chunks are published onto Google Blogger posts across multiple accounts.
The daily 2 GB capacity is based on the following metrics: $$10 \text{ accounts} \times 100 \text{ posts/account} \times 20 \text{ MB/post} = 2,000
\text{ MB (2 GB)}$$ This is feasible because: Each Google Blogger post is estimated to handle a minimum of 15 million characters,
which equates to approximately 20 MB of data. Each account can sustain about 100 published posts.
Anti-Spam Mitigation To prevent automated spam filters from flagging the long sequences of encrypted data: The encrypted Fernet chunks are interspersed with AI-generated, coherent text related to
cryptography (e.g., "How to make a cryptocurrency"). This contextual placement is intended to reduce the likelihood of the encrypted data being interpreted as malicious or non-human spam, thereby mitigating the risk of account bans. Security and Scaling Caveat The system's scalability is severely limited by a critical security flaw: Security Risk: The published post approach requires user data to be published to the open web, making the architecture unacceptable for confidential or proprietary data. Secure Alternative: The only secure implementation path is storing the chunks as draft posts, which hides the user data from the public web. While Blogger drafts encourage high volume (1,000+ per account is possible), this approach may introduce volume constraints not present with published posts. The system is designed for maximum bandwidth efficiency during retrieval, which involves
noting the character-to-character offset of each segment across the posts for seamless
reassembly and decryption. Note: This method is subject to scrutiny because of its reliance on a public forum (eg. Blogger). In other words, I do not condone the publication of customer information without premeditated consent on either the purveyor of goods and/or services or said customer's part. Also, aside from an internet-capable device and an internet connection, every aspect of said method (detailed in the post) is completely free of charge to the average user.
This use case pertains to the following scripts: base64converter.py, base64tobinary.py, binarytofernet.py, and fernettooriginal.py. In brief, file to base64 to fernet encryption and then back again or file to base64 to binary to fernet encryption and then back again.
The following link can guide user on how to use the Blogger API to accomplish this programmatically: "https://developers.google.com/blogger/docs/3.0/using".

#18

To ensure efficient utilization of system resources—both local and remote—duplicate checking is critical. This process is implemented using duplicate_string_finder5.py.

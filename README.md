# UsernameHunter

For dev work tracking down bad usernames on Lichess. Takes a list of blacklisted words and searches for exact strings in a list of given usernames. Checks a vetting document to see if the account is modclosed. Returns statistics on how accurate a blastlisted word is based off of the proportion of accounts containing that word were closed. Generates an optimized list of blacklisted words to minimize false positives.

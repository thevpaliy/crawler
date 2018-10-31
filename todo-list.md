
1. The user can extract different kinds of data.
 - Files (PDF, images, etc)
 - JavaScript source files
 - Links (Internal and external)
 - Contact information (emails, phone numbers)
 - Specific information (regex, keywords)
  * Website - information

2. Where to store this?
 - Files
 - Database ?


3. Actors:
 - Looper (waits for a new URL to come, makes a request, notifies every extractor with the response)
 - Extractor (waits for a response for a URL, extracts useful data, sends this to the processor)
 - Processor (waits for processed data, saves data)
 - Provider (a specific kind of processor)
    * Waits for links
    * Sorts out the duplicates or used links
    * Stores the links
    * Sends the filtered links to the Looper

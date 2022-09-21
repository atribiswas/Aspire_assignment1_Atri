## Assignment sub-1
Please find the following assignment submission for 1st half of Aspire Assignment by Atri Biswas.

**Requirements for the assignment-**
- concurrent inserts (2k)
- use any mysql connector
- insert 5gb csv file
- focus- exec time
- 5 columns


**Instructions-**
 1. install requirements
 2. run main.py
 3. provide the required parameters

The comments inside the files elaborate on each module in detail.

**Insights**

 - I realized that file-management with pandas is essential to the insertion of huge chunks of data into a database, thanks the pandas chunk-size parameter.
 - Concurrent insertion of 10,000 rows is done using executemany() function.
 - There is an option to create however big file required with number of rows as parameter.
 - I've used a template of 10 rows with randomized input to fill up the csv file.
 - The entire process is mostly O(n) time complexity... yet optimized to reduce processing time
 - The user interface configuration and making sure the user doesn't think the system is stuck due to large size of file is essential.

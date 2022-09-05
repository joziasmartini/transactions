# Transaction
A transaction code in Python and PostgreSQL.

### Introduction
This project aims to analyze how transactions work within a database, as well as analyze the speed of data insertion.

For this, we used a huge data file and inserted the information contained in `data.csv` through stress, calculating the time with the `timeit` library.

Thus, we were able to monitor the time that hundreds of thousands of insertions took, as well as the possible errors that appeared in this process.

### Running
- Clone the repository `git clone https://github.com/joziasmartini/transaction.git`
- Start the PostgreSQL database `sudo service postgresql start`
- Run the transaction algorithm `python3 transaction.py`

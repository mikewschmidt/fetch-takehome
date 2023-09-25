# That's SO Fetch - takehome test

### Let's make Fetch a thing!
**Fetch Rewards - Data Engineering Take Home: ETL off of a SQS Queue**

**What it does in a nutshell**
1. EXTRACTS: The program reads from a mock AWS SQS (Simple Queue Service) queue
2. TRANSFORMS: Checks for valid data and masks the PII data
3. LOADS: Loads the data into a Postgres database

#### The Output ####
Prints out the unmasked messages from the SQS queue. There is 1 dataset that does not fit the format (schema) and was NOT inserted into the database.

Running the `verify.py` file queries the database to check the information is masked for columns "masked_ip" and "masked_device_id"



## Questions

How would you deploy this application in production?
- The obvious location for production would be on AWS. I would use SQS and set a trigger to use Lambda whenever a new message is in the queue. Lambda will transform and load it into a Postgres AWS RDS database.

What other components would you want to add to make this production-ready?

- I would do a lot more testing for various performance metrics, system/connection failures, and test for bugs.
- Tuning it for better performance, like batch loading into the database instead of doing it one at a time.
- Add/set up more security around the system.
- Good quality documentation.
- Error handling and logging.
- Backup, recovery, and failover.

How can this application scale with a growing dataset?

- With RDS you can increase the storage when needed and also use auto-scaling to scale horizontality.

How can PII be recovered later on?

- I hashed the values that are unrecoverable but it will have the same output for the same input (deterministic). We could encrypt the values but most encryption is not deterministic, then we can not compare the ciphertext. I assumed that if we needed it, we load it into a different table or database with encryption set up.

What are the assumptions you made?

- I assumed the PII did not need to be recovered and was only needed for comparison by analysts.
- I'm assuming the person reading this will like my personality **MORE** than my code and will hire me. 😉



## Want to try it on your system?

Open a terminal and navigate to a location where you want to put the project files.

Run the following commands:

```
git clone https://github.com/mikewschmidt/fetch-takehome.git
cd fetch-takehome
docker compose up -d
```

Now let's create a virtual environment, so we can cleanly run the program and delete it when you're done.

`python3 -m venv fetch-venv`

Active the new virtual environment.
Run the one that matches your environment:

**Windows - CMD**   
  `fetch-venv\Scripts\activate.bat`

**Linux/Mac**   
  `source fetch-venv/bin/activate`

Let's install the dependent packages and run the program
```
pip install -r requirements.txt
python main.py
```

Run the test.py file to query the database and see the masked information for columns "masked_ip" and "masked_device_id"

  `python verify.py`

## Next Steps
If I had more time, I would figure out a deterministic encryption method for masking the PII data.
And some of the other things mentioned in the "make this production-ready" question above.

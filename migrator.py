from Migrators.HumanDiseaseTextMining.humanDiseaseTextMiningMigrator import humanDiseaseTextMiningMigrator


from typedb.client import *
from typedb.client import TypeDB, SessionType, TransactionType
from schema.initialise import initialise_database
from timeit import default_timer as timer
import argparse
import csv


def migrator_parser():
    parser = argparse.ArgumentParser(
        description='Define bio_covid database and insert data by calling separate migrate scripts.')
    parser.add_argument("-n", "--num_threads", type=int,
                        help="Number of threads to enable multi-threading (default: 8)", default=8)
    parser.add_argument("-c", "--commit_batch", help="Sets the number of queries made per commit (default: 50)",
                        default=50)
    parser.add_argument("-d", "--database", help="Database name (default: bio-covid)", default="bio_covid")
    parser.add_argument("-f", "--force",
                        help="Force overwrite the database even if a database by this name already exists (default: False)",
                        default=False)
    parser.add_argument("-a", "--address", help="Server host address (default: localhost)", default="localhost")
    parser.add_argument("-p", "--port", help="Server port (default: 1729)", default="1729")
    parser.add_argument("-v", "--verbose", help="Verbosity (default: False)", default=False)
    return parser




start = timer()
if __name__ == "__main__":
    parser = migrator_parser()
    args = parser.parse_args()

    # This is a global flag toggling counter and query printouts when we want to see less detail
    verbose = args.verbose

    # parameters hard coded
    #uri = args.address + ":" + args.port
    uri = "localhost:1729"

    #database = args.database
    database = "willtun-playground"
    
    client = TypeDB.core_client(uri)

    initialise_database(client=client, database=database, force=True)

    with client.session(database, SessionType.DATA) as session:
        humanDiseaseTextMiningMigrator(session=session, num_threads=1, batch_size=25)

end = timer()
time_in_sec = end - start
print("Elapsed time: " + str(time_in_sec) + " seconds.")

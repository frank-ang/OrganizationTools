from pprint import pprint
import time

def glue_main(region_name, session, delete=False):
    '''main function called by nuke'''

    glue = session.client('glue', region_name=region_name);

    jobs = glue.get_jobs()['Jobs'];
    for job in jobs:
    	Name = job['Name']
    	print("Found Job: %s" % Name)
    	if delete:
    		print("Deleting Job : %s" % Name)
    		response = glue.delete_job(JobName=Name)

    crawlers = glue.get_crawlers()['Crawlers'];
    for crawler in crawlers:
        Name = crawler['Name']
        print("Found Crawler: %s" % Name)
        if delete:
            print("Deleting Crawler : %s" % Name)
            response = glue.delete_crawler(Name=Name)

    databases = glue.get_databases()['DatabaseList']
    for database in databases:
        DatabaseName = database["Name"]
        print("Found Database: %s" % DatabaseName)
        # TODO convert to batch
        tables = glue.get_tables(DatabaseName=DatabaseName)['TableList'];
        for table in tables:
            Name = table['Name']
            print("Found Table: %s" % Name)
            if delete:
                print("Deleting Table : %s" % Name)
                response = glue.delete_table(DatabaseName=DatabaseName, Name=Name)
        if delete:
            print("Deleting Database : %s" % DatabaseName)
            response = glue.delete_database(Name=DatabaseName)
import csv
from typedb.client import TypeDB, SessionType, TransactionType
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from Migrators.Helpers.batchLoader import write_batch

def humanDiseaseTextMiningMigrator(session, num_threads, batch_size):
    print('  ')
    print('Opening human disease texting mining dataset...')
    print('  ')

    with open('Dataset/Jensenlab/human_disease_textmining_filtered.tsv', 'rt', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        raw_file = []
        n = 0
        for row in csvreader:
            n = n + 1
            if n != 1:
                raw_file.append(row)

    print('  Starting the batch process.')
    batch = []
    batches = []
    total = 0

    gene_set = set()
    disease_set = set()


    for row in raw_file:
        # print(row)
        gene_identifier = row[0]
        gene_name = row[1]
        disease_identifier = row[2]
        disease_name = row[3]
        z_score = row[4]
        confidence_score = row[5]

        # INSERT GENES
        if gene_name not in gene_set:
            typeql = f'''insert $g isa gene, has gene_name "{gene_name}", has gene_identifier "{gene_identifier}";'''
            batch.append(typeql)
            total += 1
            gene_set.add(gene_name)
        else:
            pass 
        
    
        # INSERT DISEASES
        if disease_name not in disease_set:
            typeql = f'''insert $d isa disease, has disease_identifier "{disease_identifier}", has disease_name "{disease_name}";'''
            batch.append(typeql)
            total += 1
            disease_set.add(disease_name)
        else:
            pass 

        
        ## INSERT RELATIONSHIPS -> need to be done separately after running above tql query
        ## note. in the migrator.py script, you also need to comment out the "initialise database" function 
        ##       which is currently has a parameter that forces the previous schema + associated data to be overwritten 
        #typeql = f'''
        #match
        #    $g isa gene, has gene_name "{gene_name}";
        #    $d isa disease, has disease_name "{disease_name}";
        #    insert $gda (gene: $g, disease: $d) isa gene-disease-association;
        #    $gda has z_score "{z_score}";
        #'''


        if len(batch) == batch_size:
            batches.append(batch)
            batch = []
    
    pool = ThreadPool(num_threads)
    pool.map(partial(write_batch, session), batches)
    pool.close()
    pool.join()
    print(f'  Genes inserted! ({total} entries)')

    session.close()
    #client.close()

import pysolr

def create_core(core_name):
    admin = pysolr.SolrCoreAdmin('http://localhost:8983/solr/admin/cores')
    resp = admin.create(core_name)
    print(resp)

def create_document(core, doc_id, doc_title):
    solr = pysolr.Solr('https://localhost:8983/solr/' + core, always_commit=True)

    document = {
        'id': doc_id,
        'title': doc_title,
    }

    solr.add(document)

    results = solr.search('title:local')
    for result in results:
        print(f"ID: {result['id']}, Title: {result['title']}")

if __name__ == "__main__":
    create_core("test")



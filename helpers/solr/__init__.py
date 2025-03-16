import pysolr

solr = pysolr.Solr('http://localhost:8983/solr/gettingstarted', always_commit=True)

document = {
    'id': '1',
    'title': 'My first document with local configs',
}
solr.add([document])

results = solr.search('title:local')
for result in results:
    print(f"ID: {result['id']}, Title: {result['title']}")

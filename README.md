# Queries to EUR-LEX Sparql access point

It is possible to retrieve data from the EUR-LEX portal using the sparql queries system **Virtuoso SPARQL Query Editor**

http://publications.europa.eu/webapi/rdf/sparql



The `sparqlQuery.csv` file contains the result of the following query:

  ```
  prefix cdm: <http://publications.europa.eu/ontology/cdm#> select distinct?work?doc_id
  where
  {
  ?work a cdm:treaty; cdm:work_id_document?doc_id.
  FILTER not exists{?work a cdm:fragment_resource_legal}. }
  ```

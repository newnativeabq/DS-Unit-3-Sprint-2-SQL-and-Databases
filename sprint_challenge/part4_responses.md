# Part 4 Responses

Answer the following questions, baseline ~3-5 sentences each, as if they were
interview screening questions (a form you fill when applying for a job):

-
-
-

## In the Northwind database, what is the type of relationship between the `Employee` and `Territory` tables?

In the Northwind database, the employee and territory tables are indirectly connected through employee territories.  The key pair associating each table is stored in the intermediate **EmployeeTerritories** table.  This indirect relationship with foreign keys EmployeeID (matching Employees data) and TerritoryID (matching Territories) is one way to prevent duplicate data with the cost of added join complexity.

## What is a situation where a document store (like MongoDB) is appropriate, and what is a situation where it is not appropriate?

Document stores like MongoDB are fantastic for scaling.  Becaue they store binary json, sharding the data and collecting records from multiple servers is much easier (though PostgreSQL is coming up close).  Document stores are also useful when developers are unsure of schema or want a query-based schema in which they can load as many tags to each record as they care for and define what data is relational, how it's pulled, etc. when they run queries.

## What is "NewSQL", and what is it trying to achieve?

NewSQL is an attempt by database developers and researchers to create relational databases with ACID assurety that scale like document stores.  PostgreSQL's sharding is one example.  These technologies vary widely under the ood.  Some only keep subsets of data and requre querying across multiple stores.  Others emulate the SQL API while builing more flexible CRUD engines in the background.


===================
Connector 20Bananas
===================

This module make the connection with the API of 20bananas

**Table of Content**

.. contents::
  :local:

Components
----------
These are the components that we inherit from the OCA module *connector*, those have been adapted to be used in 20Bananas

Backend Adapter (CRUD)
~~~~~~~~~~~~~~~~~~~~~~
It contains basic operations for the connection (CRUD operations), that will be used by the backend.

It is responsible for making requests to the API.
This compose by the next methods:
  * READ / SEARCH: In charge of searching the data through a GET request
  * CREATE: Responsible for creating the records in the api in case they do not already exist through a POST request
  * WRITE: In charge of overwriting an api record, to update the values through a PUT request
  * DELETE: In charge of deleting an api record that has been deleted through a DELETE request

By the othe hand, we create an AbstracClass that make the request to the api, to do it easily

Binder
~~~~~~

We use this component to include the Bindings that we create for each model, they are the link between the odoo register and the external object.

Exporter
~~~~~~~~

This is the base for the exporter class which we will use in each model, where we run the method to export data for the external object.

Importer
~~~~~~~~

This is the base for the importer class which we will use in each model, where we run the method to import data from the external object.

Mapper
~~~~~~

This is the base for the mapper class which we will use in each model, where we will link each attribute in the model of odoo with the attribute of the external object.

Models
------

These are the models that we will adapt and use to make the link and synchronize with 20 Bananas.

Binding
~~~~~~~

This is the base for the binding class which we will use in each model, where we will link the model of odoo with the external object.

Bananas Backend
~~~~~~~~~~~~~~~

This is the backend which is use as an interface between the external object and odoo, it's contain all the information that we required to the connectation wjth the API.
It also have the methods to synchronize the data, it can be manual or automatic, creating a cron with a wizard from this interface.

Res Partner
~~~~~~~~~~~

The res partner model has been adapted, adding a binder to associate it with the external objects of 20Bananas, also an importer class to synchronize the data and a mapper to associate the attributes of the external objects with those of odoo.
On the other hand, a new model has been created to associate the delivery days that come from the 20bananas customer object and compare it in the contacts.

Product
~~~~~~~

The product model has been adapted, adding a binder to associate it with the external objects of 20Bananas, also an importer class to synchronize the data and a mapper to associate the attributes of the external objects with those of odoo.

Price List
~~~~~~~~~~

The pricelist model has been adapted, adding a binder to associate it with the external objects of 20Bananas, also an importer class to synchronize the data and a mapper to associate the attributes of the external objects with those of odoo.

Sale
~~~~

The sale order and the order line model has been adapted, adding a binder to associate it with the external objects of 20Bananas, also an importer class to synchronize the data and a mapper to associate the attributes of the external objects with those of odoo.




Projects
========

Methods for drawing down, editing and uploading data about DocumentCloud
projects. A project is a group of documents.

Retrieval
---------

.. method:: client.projects.get(id=None, title=None)

   Return the project with the provided DocumentCloud identifer. You can
   retrieve projects using either the `id` or `title`. ::

        >>> from documentcloud import DocumentCloud
        >>> client = DocumentCloud(USERNAME, PASSWORD)
        >>> # Fetch using the id
        >>> obj = client.projects.get(id='816')
        >>> obj
        <Project: The Ruben Salazar Files>
        >>> # Fetch using the title
        >>> obj = client.projects.get(title='The Ruben Salazar Files')
        >>> obj
        <Project: The Ruben Salazar Files>

.. method:: client.projects.get_by_id(id)

   Return the project with the provided id. Operates the same as
   `client.projects.get`.

.. method:: client.projects.get_by_title(title)

   Return the project with the provided title. Operates the same as
   `client.projects.get`.

.. method:: client.projects.all(**params)

   Return all projects for the authorized DocumentCloud account.
   Please see the full `API documentation
   <https://beta.documentcloud.org/help/API/>`_ for available parameters. ::

        >>> from documentcloud import DocumentCloud
        >>> client = DocumentCloud(USERNAME, PASSWORD)
        >>> obj_list = client.projects.all()
        >>> obj_list[0]
        <Project: Ruben Salazar>

.. method:: client.projects.list(**params)

   List all projects.
   Please see the full `API documentation
   <https://beta.documentcloud.org/help/API/>`_ for available parameters.

Editing
-------

.. method:: project_obj.put()

   Save changes to a project back to DocumentCloud. You must be authorized to
   make these changes. Only the
   :attr:`description`,
   :attr:`document_list`,
   :attr:`private`,
   and :attr:`title`,
   attributes may be edited. ::

        >>> obj = client.projects.get('816')
        >>> obj.title = "Brand new title"
        >>> obj.put()

.. method:: project_obj.delete()

   Delete a project from DocumentCloud. You must be authorized to make these
   changes. ::

        >>> obj = client.projects.get('816')
        >>> obj.delete()

.. method:: project_obj.save()

    An alias for :meth:`put` that saves changes back to DocumentCloud.

Creation
--------

.. method:: client.projects.create(title, description="", private=True, document_ids=None)

   Create a new project on DocumentCloud. You must be authorized to do this.
   Returns the object representing the new record you've created.

        >>> from documentcloud import DocumentCloud
        >>> client = DocumentCloud(USERNAME, PASSWORD)
        >>> obj = client.projects.create("New project")
        >>> obj
        <Project: New project>

.. method:: client.projects.get_or_create_by_title(title)

   Fetch the project with provided name, or create it if it does not exist. You
   must be authorized to do this. Returns a tuple. An object representing the
   record comes first. A boolean that reports whether or not the objects was
   created fresh comes second. It is true when the record was created, false
   when it was found on the site already.

        >>> from documentcloud import DocumentCloud
        >>> client = DocumentCloud(USERNAME, PASSWORD)
        >>> # The first time it will be created and added to documentcloud.org
        >>> obj, created = client.projects.get_or_create_by_title("New project")
        >>> obj, created
        <Project: New project>, True
        >>> # The second time it will be fetched from documentcloud.org
        >>> obj, created = client.projects.get_or_create_by_title("New project")
        >>> obj, created
        <Project: New project>, False

Metadata
--------

.. attribute:: project_obj.created_at

.. attribute:: project_obj.description

    A summary of the project. Can be edited and saved with a put command.

.. attribute:: project_obj.document_ids

    A list that contains the unique identifier of the documents assigned to
    this project. Cannot be edited. Edit the document_list instead.

        >>> obj = client.projects.get('816')
        >>> obj.document_ids
        [19419, 19420, 19280, 19281, ...

.. attribute:: project_obj.document_list

    A list that documents assigned to this project. Can be expanded by
    appending new documents to the list or cleared by reassigning it as an
    empty list and then issuing the put command.

        >>> obj = client.projects.get('816')
        >>> obj.document_list
        [<Document: Times Columnist Ruben Salazar Slain by Tear-gas Missile>, <Document: Salazar's Legacy Lives On>, <Document: Cub Reporter Catches Attention of El Paso FBI>, ...

.. attribute:: project_obj.documents

    Alias for :attr:`document_list`.

.. attribute:: project_obj.edit_access

.. method:: project_obj.get_document(id)

        Retrieves a particular document from the project using the provided
        DocumentCloud identifer.

.. attribute:: project_obj.id

    The unique identifer of the project in DocumentCloud's system. Typically
    this is a number.

.. attribute:: project_obj.private

.. attribute:: project_obj.slug

.. attribute:: project_obj.title

    The name of the project. Can be edited and saved with a put command.

.. attribute:: project_obj.updated_at

.. attribute:: project_obj.user

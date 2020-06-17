Sections
========

Methods for drawing down, editing and creating sections of documents.

SectionClient
-------------

.. class:: documentcloud.sections.SectionClient

   The section client gives access to retrieval and creation of sections on a
   given document.  It is accessed as ``doc_obj.sections``.  The section
   client supports iteration, length and indexing so that it can be used
   directly as a sequence of the existing sections. ::

      >>> for section in doc_obj.sections:
      >>>     print(section)
      >>> section_count = len(doc_obj.sections)
      >>> second_section = doc_obj.sections[1]

   .. method:: all(self, **params)

       An alias for :meth:`list`.

   .. method:: create(self, title, page_number)

      Create a new section on this document.  There may only be one section per
      page.

   .. method:: get(id_)

      Return the section with the provided identifier.

   .. method:: list(self, **params)

      Return a list of all sections on this document, possibly filtered by
      the given parameters.  Please see the full `API documentation`_ for
      available parameters.

Section
-------

.. class:: documentcloud.sections.Section

   Sections of the documents earmarked by users.

   .. method:: put()

      Save changes to a section back to DocumentCloud. You must be authorized to
      make these changes. Only the
      :attr:`page_number`,
      and :attr:`title`,
      attributes may be edited.

   .. method:: delete()

      Delete a section from DocumentCloud. You must be authorized to make
      these changes.

   .. method:: save()

       An alias for :meth:`put` that saves changes back to DocumentCloud.

   .. attribute:: title

       The name of the section.

   .. attribute:: page

       The page where the section begins.

   .. attribute:: page_number

       Alias to :attr:`page`.

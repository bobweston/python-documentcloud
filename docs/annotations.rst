Annotations
===========

Methods for drawing down, editing and creating annotations on documents.  

AnnotationClient
----------------

.. class:: documentcloud.annotations.AnnotationClient

   The annotation client gives access to retrieval and creation of notes on a
   given document.  It is accessed as ``doc_obj.annotations``.  The annotation
   client supports iteration, length and indexing so that it can be used
   directly as a sequence of the existing notes. ::

      >>> for note in doc_obj.annotations:
      >>>     print(note)
      >>> note_count = len(doc_obj.annotations)
      >>> second_note = doc_obj.annotations[1]

   .. method:: all(self, **params)

       An alias for :meth:`list`.

   .. method:: create(self, title, page_number, content="", access="private", x1=None, y1=None, x2=Non2, y2=Non2)

      Create a new annotation on this document.  You may leave all coordinates
      blank to specify a full page note, or you must specify all documents in
      percentage of the page, a number between 0 and 1.

   .. method:: get(id_)

      Return the annotation with the provided identifier.

   .. method:: list(self, **params)

      Return a list of all annotations on this document, possibly filtered by
      the given parameters.  Please see the full `API documentation`_ for
      available parameters.

Annotation
----------

.. class:: documentcloud.annotations.Annotation

   A note left on a document.

   .. method:: put()

      Save changes to an annotation back to DocumentCloud. You must be authorized to
      make these changes. Only the
      :attr:`access`,
      :attr:`content`,
      :attr:`page_number`,
      :attr:`title`,
      :attr:`x1`,
      :attr:`x2`,
      :attr:`y1`,
      and :attr:`y2`,
      attributes may be edited.

   .. method:: delete()

      Delete an annotation from DocumentCloud. You must be authorized to make
      these changes.

   .. method:: save()

       An alias for :meth:`put` that saves changes back to DocumentCloud.

   .. attribute:: access

       The privacy level of the annotation within the DocumentCloud system. It
       will be ``public``, ``private``, or ``organization``.  ``organization``
       will extend access to the note to any user with edit access to the
       document the note is attached to, including project collaborators.

   .. attribute:: content

       Space for a lengthy text block that will be published below the highlighted
       text in the DocumentCloud design.

   .. attribute:: created_at

      The date and time this annotation was created.

   .. attribute:: description

       Alias for :attr:`content`.

   .. attribute:: edit_access

      A boolean indicating whether or not you have the ability to save this
      annotation.

   .. attribute:: id

       The unique identifer of the annotation in DocumentCloud's system.

   .. attribute:: location

      .. deprecated:: 2.0.0

       The location of where the annotation appears on the document's page.
       Defined by :class:`documentcloud.annotations.Location`.

   .. attribute:: organization

      The ID of the organization which owns this note.

   .. attribute:: page

       The page where the annotation appears.

   .. attribute:: page_number

       Alias for :attr:`page`.

   .. attribute:: title

       The name of the annotation, which appears in the table of contents and
       above the highlighted text when published by DocumentCloud.

   .. attribute:: updated_at

      The date and time of when this annotation was last updated.

   .. attribute:: user

      The ID of the user who created this annotation.

   .. attribute:: x1
   .. attribute:: x2
   .. attribute:: y1
   .. attribute:: y2

      The coordinates for the annotation, in percentage of the page.  They will
      be floats between 0 and 1. `x1` corresponds to the left, `x2` to the
      right, `y1` to the top, and `y2` to the bottom coordinate.


Location
--------

.. class:: documentcloud.annotations.Location

   The location where an :class:`documentcloud.annotations.Annotation` is
   placed within a document.  The coordinates are in pixels, normalized for a
   700 pixel width page.

   .. deprecated:: 2.0.0

      The new API directly exposes the top level attributes
      :attr:`documentcloud.annotations.Annotation.x1`,
      :attr:`documentcloud.annotations.Annotation.x2`,
      :attr:`documentcloud.annotations.Annotation.y1`, and
      :attr:`documentcloud.annotations.Annotation.y2`, which are in percentage
      of page.  New code should use those instead of the location object.

   .. attribute:: bottom

       The value of the bottom edge of an annotation.

   .. attribute:: left

       The value of the left edge of an annotation.

   .. attribute:: right

       The value of the right edge of an annotation.

   .. attribute:: top

       The value of the top edge of an annotation.

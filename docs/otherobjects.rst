Other objects
=============

Other types of data provided by the DocumentCloud system.

.. _annotations:

Annotations
-----------

.. class:: Annotation

Notes left in documents.

.. attribute:: annotation_obj.access

    The privacy level of the resource within the DocumentCloud system. It will
    be either ``public`` or ``private``.

.. attribute:: annotation_obj.content

    Space for a lengthy text block that will be published below the highlighted
    text in the DocumentCloud design.

.. attribute:: annotation_obj.created_at

.. attribute:: annotation_obj.description

    Alias for :attr:`content`.

.. attribute:: annotation_obj.edit_access

.. attribute:: annotation_obj.id

    The unique identifer of the document in DocumentCloud's system.

.. attribute:: annotation_obj.location

    The location of where the annotation appears on the document's page.
    Defined by the :ref:`locations` class.

.. attribute:: annotation_obj.organization

.. attribute:: annotation_obj.page

    The page where the annotation appears.

.. attribute:: annotation_obj.page_number

    Alias for :attr:`page`.

.. attribute:: annotation_obj.title

    The name of the annotation, which appears in the table of contents and
    above the highlighted text when published by DocumentCloud.

.. attribute:: annotation_obj.updated_at

.. attribute:: annotation_obj.user

.. XXX in document percantage
.. attribute:: annotation_obj.x1
.. attribute:: annotation_obj.x2
.. attribute:: annotation_obj.y1
.. attribute:: annotation_obj.y2

.. _locations:

Locations
---------

The location where :ref:`annotations` are placed within a document.

.. XXX in pixels assuming 700 pixel width
.. attribute:: location_obj.bottom

    The value of the bottom edge of an annotation.

.. attribute:: location_obj.left

    The value of the left edge of an annotation.

.. attribute:: location_obj.right

    The value of the right edge of an annotation.

.. attribute:: location_obj.top

    The value of the top edge of an annotation.

.. _mentions:

Mentions
--------

Mentions of a search keyword found in one of the documents.

.. attribute:: mention_obj.page

    The page where the mention occurs.

.. attribute:: mention_obj.text

    The text surrounding the mention of the keyword.

.. _sections:

Sections
--------

Sections of the documents earmarked by users.

.. attribute:: section_obj.title

    The name of the section.

.. attribute:: section_obj.page

    The page where the section begins.

.. attribute:: section_obj.page_number

    Alias to :attr:`page`.

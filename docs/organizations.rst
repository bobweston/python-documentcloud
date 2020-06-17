Organizations
=============

Organizations using the DocumentCloud service.

OrganizationClient
------------------

.. class:: documentcloud.organizations.OrganizationClient

   The organization client gives access to retrieval of organizations.  It is
   generally accessed as ``client.organizations``.

   .. method:: all(self, **params)

       An alias for :meth:`list`.

   .. method:: get(id_)

      Return the organization with the provided DocumentCloud identifer.

   .. method:: list(self, **params)

      Return a list of all organizations, possibly filtered by the given parameters.
      Please see the full `API documentation`_ for available parameters.

Organization
------------

.. class:: documentcloud.organizations.Organization

   .. attribute:: avatar_url

      A URL pointing to an image representing the organization

   .. attribute:: id

       The unique identifer of the organization in DocumentCloud's system. This
       is a number.

   .. attribute:: individual

      A boolean indicating whether this organization is for the exclusive use of
      an indivudal user.

   .. attribute:: name

      The organization's name

   .. attribute:: slug

      A URL friendly representation of the organizations's name.

   .. attribute:: uuid

      A unique identifier used across all of MuckRock's sites.

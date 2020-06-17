Users
=====

Users of the DocumentCloud service.

UserClient
----------

.. class:: documentcloud.users.UserClient

   The user client gives access to retrieval of users.  It is generally
   accessed as ``client.users``.

   .. method:: all(self, **params)

       An alias for :meth:`list`.

   .. method:: get(id_)

      Return the user with the provided DocumentCloud identifer.

   .. method:: list(self, **params)

      Return a list of all users, possibly filtered by the given parameters.
      Please see the full `API documentation`_ for available parameters.

User
----

.. class:: documentcloud.users.User

   .. attribute:: avatar_url

      A URL pointing to an image representing the user

   .. attribute:: id

       The unique identifer of the user in DocumentCloud's system. This is a number.

   .. attribute:: name

      The user's full name.

   .. attribute:: organization

      The ID of the user's active organization

   .. attribute:: organizations

      A list of IDs of all of the organizations this user is a part of.

   .. attribute:: username

      The user's username

   .. attribute:: uuid

      A unique identifier used across all of MuckRock's sites.

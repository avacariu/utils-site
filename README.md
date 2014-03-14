Utils
=====

A site that provides a few simple utilities over the web.

Currently supported are:

 * External IP address
 * User agent string
 * Request body (responds with body of request)
 * Request headers (responds with headers of request)
 * md5 sum
 * sha-X (you can choose X)
 * fortune

None of the above are formatted in any way in HTML; you get exactly the output
the relevant functions produce.

*Note:* uses Python 2.7. Python 3 support will arrive when Ubuntu 14.04
arrives.

Deployment
----------

A simple deployment script using Capistrano is provided, but not recommended.
It is specific to my setup, so it might not be appropriate for yours. It
partially relies on the use of the Puppet config in the [Jo
repository](http://github.com/vlad003/jo).

If you decide to go that way, you'll need to install the following gems:

    gem install capistrano
    gem install capistrano-virtualenv -v 1.9.1

Version 1.9.1 of `capistrano-virtualenv` is required because 1.10 is backwards
incompatible.

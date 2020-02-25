==============================================================================
cloud-init-nocloud
==============================================================================

:date:  2020-02-21
:tags: cloud-init deployment
:file: README.rst
:author: Gábor Nyers

.. sectnum::
   :start: 1
   :suffix: .
   :depth: 2

.. contents:: Contents:
   :depth: 2
   :backlinks: entry
   :local:

Agenda
======

Why containers
==============

... and not virtual machines?

#. Convenience

   Docker Hub is similar to the "AppStore" concept, i.e.:

   - Wide variety of functions being provided
   - Installation is relatively easy, that is: a set of generic steps to
     install all kinds of applications.
   - No or limited experience required to install and use the apps.
   - Maintenance of the app can be outsourced to the app vendor (requires
     trust).

#. Interoperability

   Docker containers (at least on Linux) work and can be used by and large the
   same way.

#. Isolation and security

   While VMs provide better isolation, except for highly security-concious
   environments containers can provide fair isolation. The Linux kernel
   provides two different technologies to limit what a container can do: 

   - Capabilities: limit certain kernel features, e.g.:

     - change the system's clock (``CAP_SYS_TIME``)
     - reboot the system (``CAP_SYS_BOOT``)
     - re-prioritize processes, that is: giving a process more or less CPU
       (``CAP_SYS_NICE``)
     - override file permissions (``CAP_DAC_OVERRIDE``)
     - etc...

   - Name spaces: separate "lists" to keep track of:

     - PIDs (process id's),
     - Users (UIDs and GIDs),
     - IP addresses, routing information, firewall rules,
     - hostname 
     - filesystem mounts

#. Light weight

   - Containers are **much** more lighter-weight in terms of overhead
     and less opaque than VMs.


Application
===========

This is a demo Flask application to provide ``meta-data`` and ``user-data``
for ``cloud-init`` instances.

The ``cloud-init`` project (`https://cloud-init.io/
<https://cloud-init.io/>`_) is used by many IaaS service providers to
configure newly deployed VM or even container instances. (e.g.: AWS, Azure,
Google Cloud or a local data center)

(Demo)

Usage examples:

#. Start server with default configuration, i.e.: port 5001 and  no debug: ::

    docker run -d -p 5001:5001  cloud-init-data

#. Start server on a custom port (7002) with debugging: ::

    docker run -d -e BIND_PORT=7002 -e DEBUG=y -p 7002:7002  cloud-init-data


How to "Dockerize" an application?
==================================

Run-time environment
--------------------

What run-time environment (i.e.: Linux distribution) is needed to run the
application?

  - Supported Linux distribution? (e.g.: Red Hat, SUSE or Oracle)
  - Minimalistic versions of well-known Linux distro's (or Just Enough
    Operating System, JeOS)?
  - Specialized Linux distribution for containers? (e.g. Alpine Linux)

Specific example: Alpine Linux

- Stripped down version of Libc ("MUSL Libc")
- Security-conscious: hardened kernel, e.g. protection against
  "buffer-overflows"


Passing parameters to container
-------------------------------

Parameters to control the features and configuration, e.g.:

- What port to bind to?
- Share files and/or directories from the host in the container? (e.g.: back
  up application data from host)
- Pass on secrets to the container, e.g. passwords or keys
- Passing on TLS CA and server certificates.


To pass on parameters containers usually use environment variables. So the
application has to be able to pick parameters from environment variables: ::

In Python: ::

 import os

 # String value:
 PASSWD = os.environ.get('PASSWD', 'secret')

 # Integer value:
 try              : BIND_PORT = int(os.environ.get('BIND_PORT', 0)) or 5001
 except ValueError: BIND_PORT = 5001

In the demo application:

- ``BIND_PORT``: 

How to pass parameters: ::

 docker run -d -e BIND_PORT=7002 -p 7002:7002  cloud-init-data

Where:

- ``-e BIND_PORT=7002``: create environment variable inside the container with
  the value ``7002``
- ``-p 7002:7002``: expose port 7002 of the container (2nd 7002) via port
  ``7002`` (first 7002) of the Docker host.

Shared directories
------------------

Determine what (if any) directories to share with host system?

In ``Dockerfile``: ::

 VOLUME /tmp/app



.. vim: filetype=rst textwidth=78 foldmethod=syntax foldcolumn=3 wrap
.. vim: linebreak ruler spell spelllang=en showbreak=… shiftwidth=3 tabstop=3

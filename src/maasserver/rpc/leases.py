# Copyright 2014 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""RPC helpers relating to DHCP leases."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )

str = None

__metaclass__ = type
__all__ = [
    "update_leases",
]

from django.shortcuts import get_object_or_404
from maasserver.models.dhcplease import DHCPLease
from maasserver.models.macaddress import update_mac_cluster_interfaces
from maasserver.models.nodegroup import NodeGroup
from maasserver.utils.async import transactional
from provisioningserver.pserv_services.lease_upload_service import (
    convert_mappings_to_leases,
    )
from provisioningserver.utils.twisted import synchronous


@synchronous
@transactional
def update_leases(uuid, mappings):
    """Updates DHCP leases on a cluster given the mappings in UpdateLeases.

    :param uuid: Cluster UUID as found in
        :py:class`~provisioningserver.rpc.region.UpdateLeases`.
    :param mappings: List of pairs of (ip, mac) as defined in
        :py:class`~provisioningserver.rpc.region.UpdateLeases`.

    Converts the mappings format into a dict that
    DHCPLease.objects.update_leases needs and then calls it.
    """
    nodegroup = get_object_or_404(NodeGroup, uuid=uuid)
    leases = convert_mappings_to_leases(mappings)
    DHCPLease.objects.update_leases(nodegroup, leases)
    update_mac_cluster_interfaces(leases, nodegroup)
    return {}

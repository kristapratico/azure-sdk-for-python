# pylint: disable=line-too-long,useless-suppression
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class AgentPoolMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The mode of an agent pool. A cluster must have at least one 'System' Agent Pool at all times.
    For additional information on agent pool restrictions and best practices, see:
    https://docs.microsoft.com/azure/aks/use-system-pools.
    """

    SYSTEM = "System"
    """System agent pools are primarily for hosting critical system pods such as CoreDNS and
    metrics-server. System agent pools osType must be Linux. System agent pools VM SKU must have at
    least 2vCPUs and 4GB of memory."""
    USER = "User"
    """User agent pools are primarily for hosting your application pods."""
    GATEWAY = "Gateway"
    """Gateway agent pools are dedicated to providing static egress IPs to pods. For more details, see
    https://aka.ms/aks/static-egress-gateway."""


class AgentPoolType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of Agent Pool."""

    VIRTUAL_MACHINE_SCALE_SETS = "VirtualMachineScaleSets"
    """Create an Agent Pool backed by a Virtual Machine Scale Set."""
    AVAILABILITY_SET = "AvailabilitySet"
    """Use of this is strongly discouraged."""
    VIRTUAL_MACHINES = "VirtualMachines"
    """Create an Agent Pool backed by a Single Instance VM orchestration mode."""


class ArtifactSource(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The artifact source. The source where the artifacts are downloaded from."""

    CACHE = "Cache"
    """pull images from Azure Container Registry with cache"""
    DIRECT = "Direct"
    """pull images from Microsoft Artifact Registry"""


class BackendPoolType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of the managed inbound Load Balancer BackendPool."""

    NODE_IP_CONFIGURATION = "NodeIPConfiguration"
    """The type of the managed inbound Load Balancer BackendPool.
    https://cloud-provider-azure.sigs.k8s.io/topics/loadbalancer/#configure-load-balancer-backend."""
    NODE_IP = "NodeIP"
    """The type of the managed inbound Load Balancer BackendPool.
    https://cloud-provider-azure.sigs.k8s.io/topics/loadbalancer/#configure-load-balancer-backend."""


class Code(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Tells whether the cluster is Running or Stopped."""

    RUNNING = "Running"
    """The cluster is running."""
    STOPPED = "Stopped"
    """The cluster is stopped."""


class ConnectionStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The private link service connection status."""

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DISCONNECTED = "Disconnected"


class CreatedByType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of identity that created the resource."""

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class Expander(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The expander to use when scaling up. If not specified, the default is 'random'. See `expanders
    <https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-expanders>`_
    for more information.
    """

    LEAST_WASTE = "least-waste"
    """Selects the node group that will have the least idle CPU (if tied, unused memory) after
    scale-up. This is useful when you have different classes of nodes, for example, high CPU or
    high memory nodes, and only want to expand those when there are pending pods that need a lot of
    those resources."""
    MOST_PODS = "most-pods"
    """Selects the node group that would be able to schedule the most pods when scaling up. This is
    useful when you are using nodeSelector to make sure certain pods land on certain nodes. Note
    that this won't cause the autoscaler to select bigger nodes vs. smaller, as it can add multiple
    smaller nodes at once."""
    PRIORITY = "priority"
    """Selects the node group that has the highest priority assigned by the user. It's configuration
    is described in more details `here
    <https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/expander/priority/readme.md>`_."""
    RANDOM = "random"
    """Used when you don't have a particular need for the node groups to scale differently."""


class ExtendedLocationTypes(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of extendedLocation."""

    EDGE_ZONE = "EdgeZone"


class Format(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Format."""

    AZURE = "azure"
    """Return azure auth-provider kubeconfig. This format is deprecated in v1.22 and will be fully
    removed in v1.26. See: https://aka.ms/k8s/changes-1-26."""
    EXEC = "exec"
    """Return exec format kubeconfig. This format requires kubelogin binary in the path."""
    EXEC_ENUM = "exec"
    """Return exec format kubeconfig. This format requires kubelogin binary in the path."""


class GPUDriver(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Whether to install GPU drivers. When it's not specified, default is Install."""

    INSTALL = "Install"
    """Install driver."""
    NONE = "None"
    """Skip driver install."""


class GPUInstanceProfile(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """GPUInstanceProfile to be used to specify GPU MIG instance profile for supported GPU VM SKU."""

    MIG1_G = "MIG1g"
    MIG2_G = "MIG2g"
    MIG3_G = "MIG3g"
    MIG4_G = "MIG4g"
    MIG7_G = "MIG7g"


class IpFamily(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The IP version to use for cluster networking and IP assignment."""

    I_PV4 = "IPv4"
    I_PV6 = "IPv6"


class IstioIngressGatewayMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Mode of an ingress gateway."""

    EXTERNAL = "External"
    """The ingress gateway is assigned a public IP address and is publicly accessible."""
    INTERNAL = "Internal"
    """The ingress gateway is assigned an internal IP address and cannot is accessed publicly."""


class KeyVaultNetworkAccessTypes(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Network access of the key vault. Network access of key vault. The possible values are
    ``Public`` and ``Private``. ``Public`` means the key vault allows public access from all
    networks. ``Private`` means the key vault disables public access and enables private link. The
    default value is ``Public``.
    """

    PUBLIC = "Public"
    PRIVATE = "Private"


class KubeletDiskType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Determines the placement of emptyDir volumes, container runtime data root, and Kubelet
    ephemeral storage.
    """

    OS = "OS"
    """Kubelet will use the OS disk for its data."""
    TEMPORARY = "Temporary"
    """Kubelet will use the temporary disk for its data."""


class KubernetesSupportPlan(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Different support tiers for AKS managed clusters."""

    KUBERNETES_OFFICIAL = "KubernetesOfficial"
    """Support for the version is the same as for the open source Kubernetes offering. Official
    Kubernetes open source community support versions for 1 year after release."""
    AKS_LONG_TERM_SUPPORT = "AKSLongTermSupport"
    """Support for the version extended past the KubernetesOfficial support of 1 year. AKS continues
    to patch CVEs for another 1 year, for a total of 2 years of support."""


class LicenseType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The license type to use for Windows VMs. See `Azure Hybrid User Benefits
    <https://azure.microsoft.com/pricing/hybrid-benefit/faq/>`_ for more details.
    """

    NONE = "None"
    """No additional licensing is applied."""
    WINDOWS_SERVER = "Windows_Server"
    """Enables Azure Hybrid User Benefits for Windows VMs."""


class LoadBalancerSku(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The load balancer sku for the managed cluster. The default is 'standard'. See `Azure Load
    Balancer SKUs <https://docs.microsoft.com/azure/load-balancer/skus>`_ for more information
    about the differences between load balancer SKUs.
    """

    STANDARD = "standard"
    """Use a a standard Load Balancer. This is the recommended Load Balancer SKU. For more information
    about on working with the load balancer in the managed cluster, see the `standard Load Balancer
    <https://docs.microsoft.com/azure/aks/load-balancer-standard>`_ article."""
    BASIC = "basic"
    """Use a basic Load Balancer with limited functionality."""


class ManagedClusterPodIdentityProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The current provisioning state of the pod identity."""

    ASSIGNED = "Assigned"
    CANCELED = "Canceled"
    DELETING = "Deleting"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"
    UPDATING = "Updating"


class ManagedClusterSKUName(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The name of a managed cluster SKU."""

    BASE = "Base"
    """Base option for the AKS control plane."""


class ManagedClusterSKUTier(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The tier of a managed cluster SKU. If not specified, the default is 'Free'. See `AKS Pricing
    Tier <https://learn.microsoft.com/azure/aks/free-standard-pricing-tiers>`_ for more details.
    """

    PREMIUM = "Premium"
    """Cluster has premium capabilities in addition to all of the capabilities included in 'Standard'.
    Premium enables selection of LongTermSupport (aka.ms/aks/lts) for certain Kubernetes versions."""
    STANDARD = "Standard"
    """Recommended for mission-critical and production workloads. Includes Kubernetes control plane
    autoscaling, workload-intensive testing, and up to 5,000 nodes per cluster. Guarantees 99.95%
    availability of the Kubernetes API server endpoint for clusters that use Availability Zones and
    99.9% of availability for clusters that don't use Availability Zones."""
    FREE = "Free"
    """The cluster management is free, but charged for VM, storage, and networking usage. Best for
    experimenting, learning, simple testing, or workloads with fewer than 10 nodes. Not recommended
    for production use cases."""


class NetworkDataplane(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Network dataplane used in the Kubernetes cluster."""

    AZURE = "azure"
    """Use Azure network dataplane."""
    CILIUM = "cilium"
    """Use Cilium network dataplane. See `Azure CNI Powered by Cilium
    <https://learn.microsoft.com/azure/aks/azure-cni-powered-by-cilium>`_ for more information."""


class NetworkMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The network mode Azure CNI is configured with. This cannot be specified if networkPlugin is
    anything other than 'azure'.
    """

    TRANSPARENT = "transparent"
    """No bridge is created. Intra-VM Pod to Pod communication is through IP routes created by Azure
    CNI. See `Transparent Mode <https://docs.microsoft.com/azure/aks/faq#transparent-mode>`_ for
    more information."""
    BRIDGE = "bridge"
    """This is no longer supported"""


class NetworkPlugin(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Network plugin used for building the Kubernetes network."""

    AZURE = "azure"
    """Use the Azure CNI network plugin. See `Azure CNI (advanced) networking
    <https://docs.microsoft.com/azure/aks/concepts-network#azure-cni-advanced-networking>`_ for
    more information."""
    KUBENET = "kubenet"
    """Use the Kubenet network plugin. See `Kubenet (basic) networking
    <https://docs.microsoft.com/azure/aks/concepts-network#kubenet-basic-networking>`_ for more
    information."""
    NONE = "none"
    """No CNI plugin is pre-installed. See `BYO CNI
    <https://docs.microsoft.com/en-us/azure/aks/use-byo-cni>`_ for more information."""


class NetworkPluginMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The mode the network plugin should use."""

    OVERLAY = "overlay"
    """Used with networkPlugin=azure, pods are given IPs from the PodCIDR address space but use Azure
    Routing Domains rather than Kubenet's method of route tables. For more information visit
    https://aka.ms/aks/azure-cni-overlay."""


class NetworkPolicy(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Network policy used for building the Kubernetes network."""

    NONE = "none"
    """Network policies will not be enforced. This is the default value when NetworkPolicy is not
    specified."""
    CALICO = "calico"
    """Use Calico network policies. See `differences between Azure and Calico policies
    <https://docs.microsoft.com/azure/aks/use-network-policies#differences-between-azure-and-calico-policies-and-their-capabilities>`_
    for more information."""
    AZURE = "azure"
    """Use Azure network policies. See `differences between Azure and Calico policies
    <https://docs.microsoft.com/azure/aks/use-network-policies#differences-between-azure-and-calico-policies-and-their-capabilities>`_
    for more information."""
    CILIUM = "cilium"
    """Use Cilium to enforce network policies. This requires networkDataplane to be 'cilium'."""


class NginxIngressControllerType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Ingress type for the default NginxIngressController custom resource."""

    ANNOTATION_CONTROLLED = "AnnotationControlled"
    """The default NginxIngressController will be created. Users can edit the default
    NginxIngressController Custom Resource to configure load balancer annotations."""
    EXTERNAL = "External"
    """The default NginxIngressController will be created and the operator will provision an external
    loadbalancer with it. Any annotation to make the default loadbalancer internal will be
    overwritten."""
    INTERNAL = "Internal"
    """The default NginxIngressController will be created and the operator will provision an internal
    loadbalancer with it. Any annotation to make the default loadbalancer external will be
    overwritten."""
    NONE = "None"
    """The default Ingress Controller will not be created. It will not be deleted by the system if it
    exists. Users should delete the default NginxIngressController Custom Resource manually if
    desired."""


class NodeOSUpgradeChannel(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Node OS Upgrade Channel. Manner in which the OS on your nodes is updated. The default is
    NodeImage.
    """

    NONE = "None"
    """No attempt to update your machines OS will be made either by OS or by rolling VHDs. This means
    you are responsible for your security updates"""
    UNMANAGED = "Unmanaged"
    """OS updates will be applied automatically through the OS built-in patching infrastructure. Newly
    scaled in machines will be unpatched initially and will be patched at some point by the OS's
    infrastructure. Behavior of this option depends on the OS in question. Ubuntu and Mariner apply
    security patches through unattended upgrade roughly once a day around 06:00 UTC. Windows does
    not apply security patches automatically and so for them this option is equivalent to None till
    further notice"""
    NODE_IMAGE = "NodeImage"
    """AKS will update the nodes with a newly patched VHD containing security fixes and bugfixes on a
    weekly cadence. With the VHD update machines will be rolling reimaged to that VHD following
    maintenance windows and surge settings. No extra VHD cost is incurred when choosing this option
    as AKS hosts the images."""
    SECURITY_PATCH = "SecurityPatch"
    """AKS downloads and updates the nodes with tested security updates. These updates honor the
    maintenance window settings and produce a new VHD that is used on new nodes. On some occasions
    it's not possible to apply the updates in place, in such cases the existing nodes will also be
    re-imaged to the newly produced VHD in order to apply the changes. This option incurs an extra
    cost of hosting the new Security Patch VHDs in your resource group for just in time
    consumption."""


class NodeProvisioningDefaultNodePools(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The set of default Karpenter NodePools (CRDs) configured for node provisioning. This field has
    no effect unless mode is 'Auto'. Warning: Changing this from Auto to None on an existing
    cluster will cause the default Karpenter NodePools to be deleted, which will drain and delete
    the nodes associated with those pools. It is strongly recommended to not do this unless there
    are idle nodes ready to take the pods evicted by that action. If not specified, the default is
    Auto. For more information see aka.ms/aks/nap#node-pools.
    """

    NONE = "None"
    """No Karpenter NodePools are provisioned automatically. Automatic scaling will not happen unless
    the user creates one or more NodePool CRD instances."""
    AUTO = "Auto"
    """A standard set of Karpenter NodePools are provisioned"""


class NodeProvisioningMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The node provisioning mode. If not specified, the default is Manual."""

    MANUAL = "Manual"
    """Nodes are provisioned manually by the user"""
    AUTO = "Auto"
    """Nodes are provisioned automatically by AKS using Karpenter (See aka.ms/aks/nap for more
    details). Fixed size Node Pools can still be created, but autoscaling Node Pools cannot be.
    (See aka.ms/aks/nap for more details)."""


class OSDiskType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The OS disk type to be used for machines in the agent pool. The default is 'Ephemeral' if the
    VM supports it and has a cache disk larger than the requested OSDiskSizeGB. Otherwise, defaults
    to 'Managed'. May not be changed after creation. For more information see `Ephemeral OS
    <https://docs.microsoft.com/azure/aks/cluster-configuration#ephemeral-os>`_.
    """

    MANAGED = "Managed"
    """Azure replicates the operating system disk for a virtual machine to Azure storage to avoid data
    loss should the VM need to be relocated to another host. Since containers aren't designed to
    have local state persisted, this behavior offers limited value while providing some drawbacks,
    including slower node provisioning and higher read/write latency."""
    EPHEMERAL = "Ephemeral"
    """Ephemeral OS disks are stored only on the host machine, just like a temporary disk. This
    provides lower read/write latency, along with faster node scaling and cluster upgrades."""


class OSSKU(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Specifies the OS SKU used by the agent pool. The default is Ubuntu if OSType is Linux. The
    default is Windows2019 when Kubernetes <= 1.24 or Windows2022 when Kubernetes >= 1.25 if OSType
    is Windows.
    """

    UBUNTU = "Ubuntu"
    """Use Ubuntu as the OS for node images."""
    AZURE_LINUX = "AzureLinux"
    """Use AzureLinux as the OS for node images. Azure Linux is a container-optimized Linux distro
    built by Microsoft, visit https://aka.ms/azurelinux for more information."""
    CBL_MARINER = "CBLMariner"
    """Deprecated OSSKU. Microsoft recommends that new deployments choose 'AzureLinux' instead."""
    WINDOWS2019 = "Windows2019"
    """Use Windows2019 as the OS for node images. Unsupported for system node pools. Windows2019 only
    supports Windows2019 containers; it cannot run Windows2022 containers and vice versa."""
    WINDOWS2022 = "Windows2022"
    """Use Windows2022 as the OS for node images. Unsupported for system node pools. Windows2022 only
    supports Windows2022 containers; it cannot run Windows2019 containers and vice versa."""
    UBUNTU2204 = "Ubuntu2204"
    """Use Ubuntu2204 as the OS for node images, however, Ubuntu 22.04 may not be supported for all
    nodepools. For limitations and supported kubernetes versions, see see
    https://aka.ms/aks/supported-ubuntu-versions"""


class OSType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The operating system type. The default is Linux."""

    LINUX = "Linux"
    """Use Linux."""
    WINDOWS = "Windows"
    """Use Windows."""


class OutboundType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The outbound (egress) routing method. This can only be set at cluster creation time and cannot
    be changed later. For more information see `egress outbound type
    <https://docs.microsoft.com/azure/aks/egress-outboundtype>`_.
    """

    LOAD_BALANCER = "loadBalancer"
    """The load balancer is used for egress through an AKS assigned public IP. This supports
    Kubernetes services of type 'loadBalancer'. For more information see `outbound type
    loadbalancer
    <https://docs.microsoft.com/azure/aks/egress-outboundtype#outbound-type-of-loadbalancer>`_."""
    USER_DEFINED_ROUTING = "userDefinedRouting"
    """Egress paths must be defined by the user. This is an advanced scenario and requires proper
    network configuration. For more information see `outbound type userDefinedRouting
    <https://docs.microsoft.com/azure/aks/egress-outboundtype#outbound-type-of-userdefinedrouting>`_."""
    MANAGED_NAT_GATEWAY = "managedNATGateway"
    """The AKS-managed NAT gateway is used for egress."""
    USER_ASSIGNED_NAT_GATEWAY = "userAssignedNATGateway"
    """The user-assigned NAT gateway associated to the cluster subnet is used for egress. This is an
    advanced scenario and requires proper network configuration."""
    NONE = "none"
    """The AKS cluster is not set with any outbound-type. All AKS nodes follows Azure VM default
    outbound behavior. Please refer to
    https://azure.microsoft.com/en-us/updates/default-outbound-access-for-vms-in-azure-will-be-retired-transition-to-a-new-method-of-internet-access/"""


class PodIPAllocationMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Pod IP Allocation Mode. The IP allocation mode for pods in the agent pool. Must be used with
    podSubnetId. The default is 'DynamicIndividual'.
    """

    DYNAMIC_INDIVIDUAL = "DynamicIndividual"
    """Each node gets allocated with a non-contiguous list of IP addresses assignable to pods. This is
    better for maximizing a small to medium subnet of size /16 or smaller. The Azure CNI cluster
    with dynamic IP allocation defaults to this mode if the customer does not explicitly specify a
    podIPAllocationMode"""
    STATIC_BLOCK = "StaticBlock"
    """Each node is statically allocated CIDR block(s) of size /28 = 16 IPs per block to satisfy the
    maxPods per node. Number of CIDR blocks >= (maxPods / 16). The block, rather than a single IP,
    counts against the Azure Vnet Private IP limit of 65K. Therefore block mode is suitable for
    running larger workloads with more than the current limit of 65K pods in a cluster. This mode
    is better suited to scale with larger subnets of /15 or bigger"""


class PrivateEndpointConnectionProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The current provisioning state."""

    CANCELED = "Canceled"
    CREATING = "Creating"
    DELETING = "Deleting"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"


class Protocol(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The network protocol of the port."""

    TCP = "TCP"
    """TCP protocol."""
    UDP = "UDP"
    """UDP protocol."""


class PublicNetworkAccess(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """PublicNetworkAccess of the managedCluster. Allow or deny public network access for AKS."""

    ENABLED = "Enabled"
    DISABLED = "Disabled"


class ResourceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of identity used for the managed cluster. For more information see `use managed
    identities in AKS <https://docs.microsoft.com/azure/aks/use-managed-identity>`_.
    """

    SYSTEM_ASSIGNED = "SystemAssigned"
    """Use an implicitly created system assigned managed identity to manage cluster resources. Master
    components in the control plane such as kube-controller-manager will use the system assigned
    managed identity to manipulate Azure resources."""
    USER_ASSIGNED = "UserAssigned"
    """Use a user-specified identity to manage cluster resources. Master components in the control
    plane such as kube-controller-manager will use the specified user assigned managed identity to
    manipulate Azure resources."""
    NONE = "None"
    """Do not use a managed identity for the Managed Cluster, service principal will be used instead."""


class RestrictionLevel(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The restriction level applied to the cluster's node resource group. If not specified, the
    default is 'Unrestricted'.
    """

    UNRESTRICTED = "Unrestricted"
    """All RBAC permissions are allowed on the managed node resource group"""
    READ_ONLY = "ReadOnly"
    """Only */read RBAC permissions allowed on the managed node resource group"""


class ScaleDownMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Describes how VMs are added to or removed from Agent Pools. See `billing states
    <https://docs.microsoft.com/azure/virtual-machines/states-billing>`_.
    """

    DELETE = "Delete"
    """Create new instances during scale up and remove instances during scale down."""
    DEALLOCATE = "Deallocate"
    """Attempt to start deallocated instances (if they exist) during scale up and deallocate instances
    during scale down."""


class ScaleSetEvictionPolicy(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The Virtual Machine Scale Set eviction policy. The eviction policy specifies what to do with
    the VM when it is evicted. The default is Delete. For more information about eviction see `spot
    VMs <https://docs.microsoft.com/azure/virtual-machines/spot-vms>`_.
    """

    DELETE = "Delete"
    """Nodes in the underlying Scale Set of the node pool are deleted when they're evicted."""
    DEALLOCATE = "Deallocate"
    """Nodes in the underlying Scale Set of the node pool are set to the stopped-deallocated state
    upon eviction. Nodes in the stopped-deallocated state count against your compute quota and can
    cause issues with cluster scaling or upgrading."""


class ScaleSetPriority(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The Virtual Machine Scale Set priority."""

    SPOT = "Spot"
    """Spot priority VMs will be used. There is no SLA for spot nodes. See `spot on AKS
    <https://docs.microsoft.com/azure/aks/spot-node-pool>`_ for more information."""
    REGULAR = "Regular"
    """Regular VMs will be used."""


class ServiceMeshMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Mode of the service mesh."""

    ISTIO = "Istio"
    """Istio deployed as an AKS addon."""
    DISABLED = "Disabled"
    """Mesh is disabled."""


class SnapshotType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of a snapshot. The default is NodePool."""

    NODE_POOL = "NodePool"
    """The snapshot is a snapshot of a node pool."""


class TrustedAccessRoleBindingProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The current provisioning state of trusted access role binding."""

    CANCELED = "Canceled"
    DELETING = "Deleting"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"
    UPDATING = "Updating"


class Type(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The week index. Specifies on which week of the month the dayOfWeek applies."""

    FIRST = "First"
    """First week of the month."""
    SECOND = "Second"
    """Second week of the month."""
    THIRD = "Third"
    """Third week of the month."""
    FOURTH = "Fourth"
    """Fourth week of the month."""
    LAST = "Last"
    """Last week of the month."""


class UndrainableNodeBehavior(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Defines the behavior for undrainable nodes during upgrade. The most common cause of undrainable
    nodes is Pod Disruption Budgets (PDBs), but other issues, such as pod termination grace period
    is exceeding the remaining per-node drain timeout or pod is still being in a running state, can
    also cause undrainable nodes.
    """

    CORDON = "Cordon"
    """AKS will cordon the blocked nodes and replace them with surge nodes during upgrade. The blocked
    nodes will be cordoned and replaced by surge nodes. The blocked nodes will have label
    'kubernetes.azure.com/upgrade-status:Quarantined'. A surge node will be retained for each
    blocked node. A best-effort attempt will be made to delete all other surge nodes. If there are
    enough surge nodes to replace blocked nodes, then the upgrade operation and the managed cluster
    will be in failed state. Otherwise, the upgrade operation and the managed cluster will be in
    canceled state."""
    SCHEDULE = "Schedule"
    """AKS will mark the blocked nodes schedulable, but the blocked nodes are not upgraded. A
    best-effort attempt will be made to delete all surge nodes. The upgrade operation and the
    managed cluster will be in failed state if there are any blocked nodes."""


class UpgradeChannel(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The upgrade channel for auto upgrade. The default is 'none'. For more information see `setting
    the AKS cluster auto-upgrade channel
    <https://docs.microsoft.com/azure/aks/upgrade-cluster#set-auto-upgrade-channel>`_.
    """

    RAPID = "rapid"
    """Automatically upgrade the cluster to the latest supported patch release on the latest supported
    minor version. In cases where the cluster is at a version of Kubernetes that is at an N-2 minor
    version where N is the latest supported minor version, the cluster first upgrades to the latest
    supported patch version on N-1 minor version. For example, if a cluster is running version
    1.17.7 and versions 1.17.9, 1.18.4, 1.18.6, and 1.19.1 are available, your cluster first is
    upgraded to 1.18.6, then is upgraded to 1.19.1."""
    STABLE = "stable"
    """Automatically upgrade the cluster to the latest supported patch release on minor version N-1,
    where N is the latest supported minor version. For example, if a cluster is running version
    1.17.7 and versions 1.17.9, 1.18.4, 1.18.6, and 1.19.1 are available, your cluster is upgraded
    to 1.18.6."""
    PATCH = "patch"
    """Automatically upgrade the cluster to the latest supported patch version when it becomes
    available while keeping the minor version the same. For example, if a cluster is running
    version 1.17.7 and versions 1.17.9, 1.18.4, 1.18.6, and 1.19.1 are available, your cluster is
    upgraded to 1.17.9."""
    NODE_IMAGE = "node-image"
    """Automatically upgrade the node image to the latest version available. Consider using
    nodeOSUpgradeChannel instead as that allows you to configure node OS patching separate from
    Kubernetes version patching"""
    NONE = "none"
    """Disables auto-upgrades and keeps the cluster at its current version of Kubernetes."""


class WeekDay(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The weekday enum."""

    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class WorkloadRuntime(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Determines the type of workload a node can run."""

    OCI_CONTAINER = "OCIContainer"
    """Nodes will use Kubelet to run standard OCI container workloads."""
    WASM_WASI = "WasmWasi"
    """Nodes will use Krustlet to run WASM workloads using the WASI provider (Preview)."""

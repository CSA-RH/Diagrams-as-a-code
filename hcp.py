# Ref. main project: https://diagrams.mingrammer.com/
# Ref. aws icons: https://diagrams.mingrammer.com/docs/nodes/aws
# ref. examples: https://medium.com/@akhilesh-mishra/doagram-as-code-effortless-cloud-architecture-diagrams-with-python-aece3b1a27f1



from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, VPC, PrivateSubnet, PublicSubnet, InternetGateway, NATGateway, Endpoint, Privatelink, TransitGateway, RouteTable, SiteToSiteVpn
from diagrams.aws.storage import S3
from diagrams.aws.security import IAMRole
from diagrams.generic.network import VPN
from diagrams.aws.general import InternetAlt2

 

with Diagram("OpenShift HCP Architecture", show=False, direction="LR"):

    privatelink = Privatelink("private-link")
    vpn_s2s = SiteToSiteVpn("VPN / s2s")
    internet = InternetAlt2("Internet")

    with Cluster("ROSA HCP Service Account"):
        control_planes = [EC2("Hosted Control Plane")]

    with Cluster("Customer Account"):
        # at some moment I should add the LBs
        #external_app_nlb = ELB("External App NLB")
        #internal_app_nlb = ELB("Internal App NLB")

        with Cluster("VPC ROSA HCP (10.0.0.0/16)"):

            with Cluster("Availability Zone 1"):
                private_subnet_1 = PrivateSubnet("\nPrivate Subnet\n(10.0.24.0/21)")
                # public_subnet_1 = PublicSubnet("Public Subnet")
                worker_node_1 = EC2("Worker Node")
                
                route_table_1 = RouteTable("\nPrivate Route Table\n0.0.0.0/0 -> TGW\n10.0.0.0/16 local")
                private_subnet_1 - worker_node_1

            # for simplicity I'll work with one AZ but I'll add three more for future usage
            #with Cluster("Availability Zone 2"):
            #    private_subnet_2 = PrivateSubnet("Private Subnet (10.0.24.0/21)")
            #    worker_node_2 = EC2("Worker Node")
            #    route_table_2 = RouteTable("Private Route Table\n0.0.0.0/0 -> TGW\n10.0.0.0/16 local")
            #    private_subnet_2 - worker_node_2

            #with Cluster("Availability Zone 3"):
            #    private_subnet_3 = PrivateSubnet("Private Subnet (10.0.24.0/21)")
            #    worker_node_3 = EC2("Worker Node")
            #    route_table_3 = RouteTable("Private Route Table\n0.0.0.0/0 -> TGW\n10.0.0.0/16 local")
            #    private_subnet_3 - worker_node_3

            

        #vpc_endpoint = Endpoint("VPC Endpoint")
        private_link = Privatelink("Private Link")

    with Cluster("Egress VPC (10.2.0.0/16)"):

        private_subnet_2 = PrivateSubnet("\nPrivate Subnet\n(10.2.0.0/24)")
        inbound_resolver = EC2("\nRoute 53 Inbound Resolver")
        nat_gateway_1 = NATGateway("NAT Gateway")
        private_subnet_2 - inbound_resolver
        internet_gateway = InternetGateway("Internet Gateway")
        #worker_node_1 - nat_gateway_1 - internet_gateway
        route_table_vpn = RouteTable("\nPrivate Route Table\n0.0.0.0/0 -> TGW\n10.2.0.0/16 local")

    tgw = TransitGateway("AWS Transit Gateway")

    on_prem = EC2("\nOn Prem\n192.168.0.0/16")


# Connections
    privatelink >> control_planes
    control_planes >> private_link
    worker_node_1 >> nat_gateway_1 >> internet_gateway >> internet
    # worker_node_2 >> nat_gateway_2 >> internet_gateway >> internet
    # worker_node_3 >> nat_gateway_3 >> internet_gateway >> internet
    inbound_resolver >> route_table_vpn 
    tgw >> route_table_1
    #tgw >> route_table_2
    #tgw >> route_table_3
# Bidirectional connections with a single arrow
    route_table_vpn - Edge(color="black", style="solid", dir="both") - tgw
    tgw - Edge(color="black", style="solid", dir="both") - vpn_s2s
    vpn_s2s - Edge(color="black", style="solid", dir="both") - on_prem

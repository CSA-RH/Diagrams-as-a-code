# OpenShift HCP Architecture

This repository contains a diagram representing the architecture of OpenShift Hybrid Cloud Platform (HCP) using AWS services. The diagram is generated using the `diagrams` Python library.

## Architecture Overview

The architecture consists of the following main components:

- **ROSA HCP Service Account**: Hosted Control Planes managed by Red Hat OpenShift Service on AWS (ROSA).
- **Customer Account**: Includes VPCs, subnets, worker nodes, NAT gateways, internet gateways, and private links.
- **Egress VPC**: Contains private subnets, Route 53 Inbound Resolver, NAT Gateway, and Internet Gateway.
- **AWS Transit Gateway**: Facilitates communication between different VPCs and on-premises infrastructure.
- **On-Premises**: Represents the on-premises infrastructure connected via VPN.

## Diagram

![OpenShift HCP Architecture Diagram](https://github.com/CSA-RH/Diagrams-as-a-code/blob/main/openshift_hcp_architecture.png)

## Project Structure

- `hcp.py`: The main script to generate the architecture diagram.
- `README.md`: This documentation file.

## Requirements

- Python 3.6 or higher
- `diagrams` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/CSA-RH/Diagrams-as-a-code.git
    cd openshift-hcp-architecture
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    source venv/bin/activate  
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To generate the diagram, run the following command:

```sh
python hcp.py

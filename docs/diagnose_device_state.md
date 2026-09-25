# Fabric Device State Diagnostic

`diagnose_device_state.py` is a read-only diagnostic utility for identifying
inconsistent device state across Cisco Catalyst Center inventory,
Software-Defined Access fabric membership, SDA roles, and wired-device
provisioning.

## Why This Tool Exists

A device can appear correctly in Catalyst Center inventory while other
Catalyst Center services maintain a different view of that device.

This can occur during troubleshooting scenarios involving:

- Device reprovisioning
- Inventory changes
- Fabric role changes
- Recovery operations
- Stale or partially synchronized SDA state

Rather than checking each API independently, this tool collects and
correlates the relevant state into a single diagnostic report.

## What It Checks

For a selected fabric site and device, the tool evaluates:

1. Current Catalyst Center inventory identity
2. Site assignment
3. Fabric Devices membership
4. Assigned fabric roles
5. SDA role state by management IP
6. Wired-device provisioning state

The results are then compared to identify potential inconsistencies.

## Example Workflow


Authenticate to Catalyst Center
        |
        v
Discover Fabric Sites
        |
        v
Select Fabric Site
        |
        v
Select Device
        |
        v
Resolve Current Inventory UUID
        |
        +-------------------+
        |                   |
        v                   v
 Fabric Device State    SDA Role State
        |                   |
        +---------+---------+
                  |
                  v
          Provisioning State
                  |
                  v
          Correlate Results
                  |
                  v
          Diagnostic Report

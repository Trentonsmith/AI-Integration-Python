from enum import Enum



class Issue(Enum):
    """
    naming_inconsistency is for inconsistencies with naming of either rooms, makes, or models
    ip_address_inconsistency is for inconsistencies with IP Addresses, (wrong subnets, invalid octets) IP's do NOT use this for non-sequential IP's, that is not an issue
    mac_address_inconsistency is for inconsistencies with MAC Addresses (patterns look incorrect between devices of same type) do NOT report RLNK 0000 issues, those are not an issue
    serial_number_inconsistency is for inconsistencies with Serial Numbers ( serial number patterns or lengths look incorrect between other devices of the same model, or look wrong based on manufacturerer norms)
    other is for anything you find odd or incorrect that doesn't fit into the previous categories
    You do not report unless there is a real inconsistency
    """
    NAMING_INCONSISTENCY = "naming_inconsistency"
    IP_ADDRESS_INCONSISTENCY = "ip_address_inconsistency"
    MAC_ADDRESS_INCONSISTENCY = "mac_address_inconsistency"
    SERIAL_NUMBER_INCONSISTENCY = "serial_number_inconsistency"
    OTHER = "other"

from RentManagementSystem import RentManagementSystem

# test the rent management functions
def main():
    # Create an instance of the RentManagementSystem
    landlord_address = "0x123..."
    rent_system = RentManagementSystem(landlord_address)

    # Add rental properties
    try:
        rent_system.add_property("Property 1", 1000, 500, "2024-05-10", landlord_address)
        rent_system.add_property("Property 2", 1500, 750, "2024-05-15", landlord_address)
        rent_system.add_property("Property 3", 2000, 1000, "2024-05-20", landlord_address)
    except Exception as e:
        print(f"Error adding property: {str(e)}")

    # Add tenants to properties
    try:
        rent_system.add_tenant_to_property(1, "0xabc...", landlord_address)
        rent_system.add_tenant_to_property(2, "0xdef...", landlord_address)
        rent_system.add_tenant_to_property(3, "0xghi...", landlord_address)
    except Exception as e:
        print(f"Error adding tenant: {str(e)}")

    # Tenants pay security deposits
    try:
        rent_system.pay_security_deposit(1, "0xabc...", 500)
        rent_system.pay_security_deposit(2, "0xdef...", 750)
        rent_system.pay_security_deposit(3, "0xghi...", 1000)
    except Exception as e:
        print(f"Error paying security deposit: {str(e)}")

    # Tenants pay rent (on time)
    try:
        rent_system.pay_rent(1, "0xabc...", 1000)
        rent_system.pay_rent(3, "0xghi...", 2000)
    except Exception as e:
        print(f"Error paying rent: {str(e)}")

    # Tenant pays rent (late)
    try:
        rent_system.pay_rent(2, "0xdef...", 1500)
    except Exception as e:
        print(f"Error paying rent: {str(e)}")

    # Landlord withdraws rent
    rent_system.withdraw_rent(500, landlord_address)
    rent_system.withdraw_rent(4550, landlord_address)

    # Landlord terminates a lease
    try:
        rent_system.terminate_lease(2, landlord_address)
    except Exception as e:
        print(f"Error terminating lease: {str(e)}")

    # Output
    print("Rental Properties:")
    print(rent_system.get_rental_properties())

    print("\nTenants:")
    print(rent_system.get_tenants())

    print("\nPayment Log:")
    print(rent_system.get_payment_log())

    print("\nWithdrawal Log:")
    print(rent_system.get_withdrawal_log())

    print("\nTermination Log:")
    print(rent_system.get_termination_log())


if __name__ == "__main__":
    main()
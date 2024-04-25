from datetime import datetime


class RentManagementSystem:
    def __init__(self, landlord_address):
        self.landlord_address = landlord_address
        self.properties = {}
        self.tenants = {}
        self.payments = []
        self.withdrawals = []
        self.terminations = []

    def add_property(self, property_name, monthly_rent, security_deposit, due_date, sender_address):
        if sender_address != self.landlord_address:
            raise Exception("Only the landlord can add a property.")

        property_id = len(self.properties) + 1
        self.properties[property_id] = {
            "name": property_name,
            "monthly_rent": monthly_rent,
            "security_deposit": security_deposit,
            "due_date": due_date,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tenant": None
        }
        print(f"Property {property_name} added with ID {property_id}.")

    def add_tenant_to_property(self, property_id, tenant_address, sender_address):
        if sender_address != self.landlord_address:
            raise Exception("Only the landlord can add a tenant.")

        if property_id not in self.properties:
            raise Exception("Invalid property ID.")

        self.properties[property_id]["tenant"] = tenant_address
        self.tenants[tenant_address] = property_id
        print(f"Tenant {tenant_address} added to property {property_id}.")

    def pay_security_deposit(self, property_id, sender_address, deposit_amount):
        if sender_address not in self.tenants:
            raise Exception("Only a tenant can pay the security deposit.")

        if self.tenants[sender_address] != property_id:
            raise Exception("Tenant is not assigned to this property.")

        property_data = self.properties[property_id]
        if deposit_amount != property_data["security_deposit"]:
            raise Exception("Incorrect security deposit amount.")

        self.payments.append({"type": "security_deposit", "amount": deposit_amount,
                              "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        print("Security deposit paid successfully.")

    def pay_rent(self, property_id, sender_address, rent_amount):
        if sender_address not in self.tenants:
            raise Exception("Only a tenant can pay rent.")

        if self.tenants[sender_address] != property_id:
            raise Exception("Tenant is not assigned to this property.")

        property_data = self.properties[property_id]
        due_date = property_data["due_date"]
        current_date = datetime.now().strftime("%Y-%m-%d")

        if current_date > due_date:
            late_fee = 50  # Assuming a fixed late fee of 50
            total_amount = rent_amount + late_fee
            if rent_amount != total_amount:
                raise Exception("Rent amount does not include the late fee.")
        else:
            total_amount = rent_amount

        if total_amount != property_data["monthly_rent"]:
            raise Exception("Incorrect rent amount.")

        self.payments.append(
            {"type": "rent", "amount": total_amount, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        print("Rent paid successfully.")

    def withdraw_rent(self, amount, sender_address):
        if sender_address != self.landlord_address:
            print("Error: Only the landlord can withdraw rent.")
            return

        total_rent = sum(payment["amount"] for payment in self.payments if payment["type"] == "rent")
        if amount > total_rent:
            print("Error: Withdrawal amount exceeds total rent collected.")
            return

        # Simulating the transfer of funds to the landlord
        print(f"Transferring {amount} to {self.landlord_address}")
        self.withdrawals.append({"amount": amount, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        print(f"Rent of {amount} withdrawn successfully.")

    def terminate_lease(self, property_id, sender_address):
        if sender_address != self.landlord_address:
            raise Exception("Only the landlord can terminate the lease.")

        if property_id not in self.properties:
            raise Exception("Invalid property ID.")

        property_data = self.properties[property_id]
        tenant_address = property_data["tenant"]

        if tenant_address is None:
            raise Exception("No tenant assigned to this property.")

        security_deposit = property_data["security_deposit"]
        # Simulating the refund of the security deposit to the tenant
        print(f"Refunding {security_deposit} to {tenant_address}")

        self.properties[property_id]["tenant"] = None
        del self.tenants[tenant_address]

        self.terminations.append(
            {"property_id": property_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        print(f"Lease terminated for property {property_id}. Security deposit refunded.")

    def get_rental_properties(self):
        return list(self.properties.values())

    def get_tenants(self):
        return list(self.tenants.keys())

    def get_payment_log(self):
        return self.payments

    def get_withdrawal_log(self):
        return self.withdrawals

    def get_termination_log(self):
        return self.terminations


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
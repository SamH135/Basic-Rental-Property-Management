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



from pydantic import BaseModel
from typing import Dict, List

import json


class Parameters(BaseModel):
    apartments_json_path: str = 'data/apartments.json'
    tenants_json_path: str = 'data/tenants.json'
    transfers_json_path: str = 'data/transfers.json'
    bills_json_path: str = 'data/bills.json'


class Room(BaseModel):
    name: str
    area_m2: float


class Apartment(BaseModel):
    key: str
    name: str
    location: str
    area_m2: float
    rooms: Dict[str, Room]

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Apartment']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of apartments"
        return {key: Apartment(**apartment) for key, apartment in data.items()}

    
class Tenant(BaseModel):
    name: str
    apartment: str
    room: str
    rent_pln: float
    deposit_pln: float
    date_agreement_from: str
    date_agreement_to: str

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Tenant']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of tenants"
        return {key: Tenant(**tenant) for key, tenant in data.items()}
    

class Transfer(BaseModel):
    amount_pln: float
    date: str
    settlement_year: int | None
    settlement_month: int | None
    tenant: str

    @staticmethod
    def from_json_file(file_path: str) -> List['Transfer']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of transfers"
        return [Transfer(**transfer) for transfer in data]


class Bill(BaseModel):
    amount_pln: float
    date_due: str
    apartment: str
    settlement_year: int
    settlement_month: int
    type: str

    @staticmethod
    def from_json_file(file_path: str) -> List['Bill']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of bills"
        return [Bill(**bill) for bill in data]
    
class TenantSettlement:
    name: str
    apartment: str
    room: str
    date_due: str
    amount_pln: float


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

if __name__ == '__main__':
    parameters = Parameters()
    manager = Manager(parameters)

    for apartment in manager.apartments.values():
        print(apartment.key, "\n" , apartment.name, "\n" , apartment.location, "\n" , apartment.area_m2)
        for room in apartment.rooms.values():
            print('  ', room.name, room.area_m2)
        
        for bill in manager.bills:
            if bill.apartment == apartment.key:
                print('  ', bill.amount_pln, "\n" ,  bill.date_due, "\n" , bill.settlement_year, "\n" , bill.settlement_month,  "\n" , bill.type)

    for tenant in manager.tenants.values():
        print(tenant.name, "\n" , tenant.apartment, "\n" , tenant.room, "\n" , tenant.rent_pln, "\n" , tenant.deposit_pln, "\n" , tenant.date_agreement_from, "\n" , tenant.date_agreement_to)
        for transfer in manager.transfers:
            if transfer.tenant == tenant.name:
                print('  ', transfer.amount_pln, "\n" , transfer.date, "\n" , transfer.settlement_year, "\n" , transfer.settlement_month)
    
    for tenantSettlement in manager.tenants.values():
        print(tenant.name, "\n" , tenant.apartment, "\n" , tenant.room, "\n" , bill.date_due, "\n" , "rachunki:", "\n" , bill.amount_pln,",", "\n" , "Czynsz:", "\n" , tenant.rent_pln, ",", "\n" , "Przelew:", "\n" , transfer.amount_pln, "\n" , "saldo: ", "\n" , transfer.amount_pln-bill.amount_pln-tenant.rent_pln)

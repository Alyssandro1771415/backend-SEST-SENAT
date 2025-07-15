from models.patient_model import Patient

async def get_region_datas(estado: str):
    if estado != "all":
        patients_region_data = await Patient.find(Patient.estado == estado).to_list()
    else:
        patients_region_data = await Patient.find_all().to_list()

    return [p.model_dump(exclude={"id"}) for p in patients_region_data]
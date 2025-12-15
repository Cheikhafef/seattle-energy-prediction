import bentoml
import pandas as pd
import joblib
import os
import traceback
from pydantic import BaseModel

# Charger le modèle
model_path = os.path.join(os.path.dirname(__file__), "pipeline.joblib")
model = joblib.load(model_path)

essential_features = [
    "PrimaryPropertyType",
    "NumberofBuildings",
    "NumberofFloors",
    "PropertyGFATotal",
    "PropertyGFAParking",
    "LargestPropertyUseType",
    "ENERGYSTARScore",
    "DefaultData",
    "BuildingAge"
]

class EnergyInput(BaseModel):
    PrimaryPropertyType: str
    NumberofBuildings: float
    NumberofFloors: float
    PropertyGFATotal: float
    PropertyGFAParking: float
    LargestPropertyUseType: str
    ENERGYSTARScore: float
    DefaultData: float
    BuildingAge: float

def prepare_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])

    numeric_cols = [
        "NumberofBuildings",
        "NumberofFloors",
        "PropertyGFATotal",
        "PropertyGFAParking",
        "ENERGYSTARScore",
        "DefaultData",
        "BuildingAge"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

    categorical_cols = [
        "PrimaryPropertyType",
        "LargestPropertyUseType"
    ]

    for col in categorical_cols:
        df[col] = df.get(col, "Unknown").astype(str)

    return df[essential_features]


@bentoml.service(name="energy_model")
class EnergyService:

    @bentoml.api
    def predict(self, input_data: dict) -> dict:
        """
        input_data: dict correspondant aux colonnes du modèle
        """
        try:
            # Si l'utilisateur a envoyé Pydantic, convertir en dict
            if hasattr(input_data, "dict"):
                data_dict = input_data.dict()
            else:
                data_dict = input_data

            df = prepare_input(data_dict)
            pred = model.predict(df)
            return {"prediction": float(pred[0])}

        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            }

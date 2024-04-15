from pprint import pprint

import constants
from feast import FeatureStore

store = FeatureStore(constants.REPO_PATH)  # Initialize the feature store

feature_service = store.get_feature_service("driver_activity_v1")
feature_vector = store.get_online_features(
    features=feature_service,
    entity_rows=[
        {"driver_id": 1004},
        {"driver_id": 1005},
    ],
).to_dict()
pprint(feature_vector)

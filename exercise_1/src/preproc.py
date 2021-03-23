
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler

def preproc(data, onehot_encoder=None, scaler=None):
    this_data = data.copy()
    this_data.dropna(inplace=True) # drop all lines with missing values
    this_data.reset_index(inplace=True, drop=True)

    drops = ["education-num"] # drop this since we have education and education-num 
    this_data.drop(columns=drops, axis=1, inplace=True)

    # numericals to scale
    to_scale = ["age", "fnlwgt", "capital-gain", "capital-loss", "hours-per-week"]

    if not scaler:
        this_scaler = MinMaxScaler()
        this_scaler.fit(this_data[to_scale])
    else:
        this_scaler = scaler 
    this_data[to_scale] = this_scaler.transform(this_data[to_scale])

    # categorical columns to drop
    onehot = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex", "native-country"]

    # in case no encoder is provided we create one which can then be re-used (train-test split)
    if not onehot_encoder:
        this_enc = OneHotEncoder(handle_unknown='ignore')
        this_enc.fit(this_data[onehot])
    else:
        this_enc = onehot_encoder

    encoded = pd.DataFrame(this_enc.transform(this_data[onehot]).toarray(), columns=this_enc.get_feature_names())
    this_data = pd.concat([this_data.drop(columns=onehot),
                    encoded],
                    axis=1)

    # assert that all went well and we did not loose or add any rows...
    assert(data.dropna().shape[0] == this_data.shape[0])

    return this_data, this_enc, this_scaler

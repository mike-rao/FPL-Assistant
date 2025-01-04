import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

data = pd.read_csv('fpl_player_data.csv')

X = data[['position', 'form', 'total_pts', 'total_bonus', 'ict_index', 'tsb_percent', 'fdr']]
y = data['pts_scored']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
joblib.dump(scaler, 'scaler.pkl')

model = MLPRegressor(hidden_layer_sizes=(100, 50), activation='relu', solver='adam',
                     learning_rate='adaptive', max_iter=500, random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Squared Error: {rmse}")

joblib.dump(model, 'fpl_model.pkl')
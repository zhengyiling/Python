# Python Notebook - shipping forecast

"""
# New Notebook
"""

datasets

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import datetime

df = datasets[1]
df['SHIPPED_WEEK'] = pd.to_datetime(df['SHIPPED_WEEK'])
# print(df.head())
print(df.dtypes)

print(df.head())

def create_features(df):
    df = df.copy()
    df['weekofyear'] = df['SHIPPED_WEEK'].dt.isocalendar().week
    df['month'] = df['SHIPPED_WEEK'].dt.month
    df['year'] = df['SHIPPED_WEEK'].dt.year
    df['volume_lag1'] = df.groupby(['WAREHOUSE', 'CARRIER', 'CARRIER_SERVICE'])['SHIPPED_ORDER_VOLUME'].shift(1)
    df['volume_lag2'] = df.groupby(['WAREHOUSE', 'CARRIER', 'CARRIER_SERVICE'])['SHIPPED_ORDER_VOLUME'].shift(2)
    df['volume_lag3'] = df.groupby(['WAREHOUSE', 'CARRIER', 'CARRIER_SERVICE'])['SHIPPED_ORDER_VOLUME'].shift(3)
    return df

df = create_features(df)

# Drop rows with NaNs from lagging
df = df.dropna()


le_warehouse = LabelEncoder()
le_carrier = LabelEncoder()
le_service = LabelEncoder()

df['warehouse_enc'] = le_warehouse.fit_transform(df['WAREHOUSE'])
df['carrier_enc'] = le_carrier.fit_transform(df['CARRIER'])
df['carrier_service_enc'] = le_service.fit_transform(df['CARRIER_SERVICE'])


future_forecasts = []

group_cols = ['WAREHOUSE', 'CARRIER', 'CARRIER_SERVICE']
features = ['weekofyear', 'month', 'year', 'volume_lag1', 'volume_lag2', 'volume_lag3',
            'warehouse_enc', 'carrier_enc', 'carrier_service_enc']

for group, group_df in df.groupby(group_cols):
    if len(group_df) < 6:
      print(f"Skipping group {group} (too few rows: {len(group_df)})")
      continue
    
    print("Forecasting:", group)
    group_df = group_df.sort_values('SHIPPED_WEEK')
    latest = group_df.iloc[-3:].copy()  # last 3 weeks needed for lag features
    history = group_df.copy()
    
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(group_df[features], group_df['SHIPPED_ORDER_VOLUME'])

    future_preds = []
    current_week = group_df['SHIPPED_WEEK'].max()

    for i in range(12):
        next_week = current_week + pd.Timedelta(weeks=1)
        
        # Build row for next week
        new_row = {
            'shipped_week': next_week,
            'weekofyear': next_week.isocalendar().week,
            'month': next_week.month,
            'year': next_week.year,
            'volume_lag1': latest.iloc[-1]['SHIPPED_ORDER_VOLUME'],
            'volume_lag2': latest.iloc[-2]['SHIPPED_ORDER_VOLUME'],
            'volume_lag3': latest.iloc[-3]['SHIPPED_ORDER_VOLUME'],
            'warehouse_enc': latest.iloc[-1]['warehouse_enc'],
            'carrier_enc': latest.iloc[-1]['carrier_enc'],
            'carrier_service_enc': latest.iloc[-1]['carrier_service_enc'],
        }

        X_pred = pd.DataFrame([new_row])[features]
        pred_volume = model.predict(X_pred)[0]
        new_row['SHIPPED_ORDER_VOLUME'] = pred_volume

        # Append forecast
        future_preds.append({**new_row, **dict(zip(group_cols, group))})

        # Update lags
        latest = pd.concat([latest, pd.DataFrame([new_row])], ignore_index=True)
        current_week = next_week

    future_forecasts.extend(future_preds)

# Combine all results
forecast_df = pd.DataFrame(future_forecasts)
forecast_df = forecast_df[['shipped_week'] + group_cols + ['SHIPPED_ORDER_VOLUME']]


print(forecast_df.head(20))  # preview

# Optional: save to CSV
# forecast_df.to_csv('12_week_forecast_by_group.csv', index=False)


# Use data from just one group for simplicity
# group = df[(df['WAREHOUSE'] == 'Hong Kong 5') & (df['CARRIER'] == 'FEDEX')]

# train = group[:-12]
# test = group[-12:]

# features = ['weekofyear', 'month', 'year', 'volume_lag1', 'volume_lag2', 'volume_lag3', 
#             'warehouse_enc', 'carrier_enc', 'service_enc']

# X_train = train[features]
# y_train = train['SHIPPED_ORDER_VOLUME']

# X_test = test[features]
# y_test = test['SHIPPED_ORDER_VOLUME']


# model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
# model.fit(X_train, y_train)

# Predict
# y_pred = model.predict(X_test)

# Evaluate
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# print(f"Test RMSE: {rmse:.2f}")


# print(df['SHIPPED_ORDER_VOLUME'].mean())




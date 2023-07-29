import pandas as pd
import csv

flight_traffic = "flight_traffic.csv"
df = pd.read_csv(flight_traffic)
df.fillna(0, inplace=True)

cleaned_flight_traffic = "cleaned_flight_traffic.csv"
df.to_csv(cleaned_flight_traffic, index=False)

data = pd.read_csv('cleaned_flight_traffic.csv')

from operator import itemgetter
fname='cleaned_flight_traffic.csv'
get_columns=itemgetter('year', 'month', 'day', 'airline_id', 'origin_airport', 'destination_airport', 'scheduled_departure', 'actual_departure', 'taxi_out',
                       'wheels_off', 'taxi_in', 'scheduled_arrival', 'actual_arrival', 'cancelled', 'diverted', 'scheduled_elapsed', 'actual_elapsed', 'distance', 'airline_delay',
                       'weather_delay', 'air_system_delay', 'security_delay', 'aircraft_delay')
#testing
#with open(fname,'r') as csvfile:
    #reader = csv.DictReader(csvfile.readlines()[0:11])
    #[print(*get_columns(row)) for row in reader]


x = data[['taxi_out']]
y = data['airline_delay']

from sklearn.model_selection import train_test_split


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=None)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(x_train, y_train)

from sklearn.metrics import mean_squared_error, r2_score

# Make predictions on the test set
y_pred = model.predict(x_test)


r2 = r2_score(y_test, y_pred)

print("R-squared:", r2)

comparison_df = pd.DataFrame({'Actual Delay': y_test, 'Predicted Delay': y_pred})
print(comparison_df.head(50))


#mean2error = mean_squared_error(y_test, y_pred)

# iniciando com o projeto. importando os pacotes necessários.

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.distance import geodesic
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# importando o banco de dados

file_path = '/content/fraud_data.csv'
df = pd.read_csv(file_path)

# padronizando as variáveis

df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'], format='%d-%m-%Y %H:%M')
df['dob'] = pd.to_datetime(df['dob'], format='%d-%m-%Y')
df['age'] = df['trans_date_trans_time'].dt.year - df['dob'].dt.year
df['is_fraud'] = df['is_fraud'].str.extract('(\d)').astype(int)

# hora/dia da semana/mês
df['transaction_hour'] = df['trans_date_trans_time'].dt.hour
df['transaction_day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
df['transaction_month'] = df['trans_date_trans_time'].dt.month

def calculate_distance(row):
    trans_location = (row['lat'], row['long'])
    merch_location = (row['merch_lat'], row['merch_long'])
    return geodesic(trans_location, merch_location).kilometers

df['distance_to_merch'] = df.apply(calculate_distance, axis=1)
df['daily_transaction_count'] = df.groupby(df['trans_date_trans_time'].dt.date)['trans_num'].transform('count')
df['merchant_consistency'] = df.groupby(['job', 'merchant'])['trans_num'].transform('count')


# Exploratoria
plt.figure(figsize=(10, 6))
sns.histplot(df['amt'], bins=50, kde=True)
plt.title('Distribution of Transaction Amounts')
plt.xlabel('Transaction Amount ($)')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['age'], bins=50, kde=True)
plt.title('Distribution of Customer Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['city_pop'], bins=50, kde=True)
plt.title('Distribution of City Population')
plt.xlabel('City Population')
plt.ylabel('Frequency')
plt.show()

# Análise Bivariada
plt.figure(figsize=(10, 6))
sns.boxplot(x='is_fraud', y='amt', data=df)
plt.title('Transaction Amount by Fraud Status')
plt.xlabel('Is Fraud')
plt.ylabel('Transaction Amount ($)')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='is_fraud', y='age', data=df)
plt.title('Customer Age by Fraud Status')
plt.xlabel('Is Fraud')
plt.ylabel('Age')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='is_fraud', y='city_pop', data=df)
plt.title('City Population by Fraud Status')
plt.xlabel('Is Fraud')
plt.ylabel('City Population')
plt.show()

# Análise geoespacial
plt.figure(figsize=(12, 10))
sns.scatterplot(x='long', y='lat', hue='is_fraud', data=df, palette={0: 'blue', 1: 'red'}, alpha=0.6)
plt.title('Geographic Distribution of Transactions and Fraud')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Is Fraud', loc='upper left', labels=['Non-Fraudulent', 'Fraudulent'])
plt.show()

# Modelo
features = [
    'amt', 'age', 'city_pop', 'distance_to_merch',
    'daily_transaction_count', 'merchant_consistency',
    'transaction_hour', 'transaction_day_of_week', 'transaction_month'
]
X = df[features]
y = df['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
print(report)
print(conf_matrix) # Matriz de confusão


plt.figure(figsize=(8, 6))
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, display_labels=['Non-Fraudulent', 'Fraudulent'], cmap=plt.cm.Blues)
plt.title('Matriz de Confusão do modelo de detecção de fraude')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

# parâmetro de afinação (tuning)
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42),
                           param_grid=param_grid,
                           cv=3,
                           n_jobs=-1,
                           verbose=2)

grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

# Gráficos
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='amt', hue='is_fraud', bins=50, kde=True, palette={0: 'blue', 1: 'red'})
plt.title('Distribution of Transaction Amounts by Fraud Status')
plt.xlabel('Transaction Amount ($)')
plt.ylabel('Frequency')
plt.legend(title='Is Fraud', labels=['Non-Fraudulent', 'Fraudulent'])
plt.show()

plt.figure(figsize=(12, 8))
category_order = df['category'].value_counts().index
sns.countplot(data=df, x='category', hue='is_fraud', order=category_order, palette={0: 'blue', 1: 'red'})
plt.title('Fraud by Transaction Category')
plt.xlabel('Transaction Category')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Is Fraud', labels=['Non-Fraudulent', 'Fraudulent'])
plt.show()

plt.figure(figsize=(12, 10))
sns.scatterplot(x='long', y='lat', hue='is_fraud', data=df, palette={0: 'blue', 1: 'red'}, alpha=0.6)
plt.title('Geographic Distribution of Fraudulent Transactions')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Is Fraud', loc='upper left', labels=['Non-Fraudulent', 'Fraudulent'])
plt.show()

# fraude por tempo
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='transaction_hour', hue='is_fraud', palette={0: 'blue', 1: 'red'})
plt.title('Fraud by Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Count')
plt.legend(title='Is Fraud', labels=['Non-Fraudulent', 'Fraudulent'])
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='transaction_day_of_week', hue='is_fraud', palette={0: 'blue', 1: 'red'})
plt.title('Fraud by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Count')
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.legend(title='Is Fraud', labels=['Non-Fraudulent', 'Fraudulent'])
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='transaction_month', hue='is_fraud', palette={0: 'blue', 1: 'red'})
plt.title('Fraud by Month of the Year')
plt.xlabel('Month')
plt.ylabel('Count')
plt.legend(title='Is Fraud', labels=['Non-Fraudulent', 'Fraudulent'])
plt.show()

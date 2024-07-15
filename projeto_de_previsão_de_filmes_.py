# -*- coding: utf-8 -*-
"""Projeto de Previsão de Filmes .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TSmDClxqfz-98YSrSZ11tnqKldDrsZf8
"""

import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE, RandomOverSampler, ADASYN, BorderlineSMOTE, KMeansSMOTE, SVMSMOTE
from imblearn.under_sampling import ClusterCentroids, CondensedNearestNeighbour, EditedNearestNeighbours
from imblearn.under_sampling import RepeatedEditedNearestNeighbours, TomekLinks, AllKNN, InstanceHardnessThreshold
from imblearn.under_sampling import NearMiss, NeighbourhoodCleaningRule, OneSidedSelection, RandomUnderSampler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, roc_curve,confusion_matrix
from sklearn.impute import SimpleImputer
import seaborn as sns
import matplotlib.pyplot as plt

dados = pd.read_csv('indicium_imdb.csv')
dados.head()

dados.shape

# Filtrei os filmes com alta nota na coluna IMDB
filmes_altas_notas = dados[dados['IMDB_Rating'] >= 8.0]

# Escolhendo o que tem o maior número de votos
filme_recomendado = filmes_altas_notas.sort_values(by='No_of_Votes', ascending=False).iloc[0]

# O filme que eu recomendaria para as pessoas, seria o ?
print(f"O Filme que eu recomendadaria para uma pessoa que não conheço é: {filme_recomendado['Series_Title']}")
print(f"Ano de lançamento: {filme_recomendado['Released_Year']}")
print(f"Classificação etária: {filme_recomendado['Certificate']}")
print(f"Tempo de duração: {filme_recomendado['Runtime']}")
print(f"Gênero: {filme_recomendado['Genre']}")
print(f"Nota do IMDB: {filme_recomendado['IMDB_Rating']}")
print(f"Overview: {filme_recomendado['Overview']}")
print(f"Média ponderada das críticas (Meta_score): {filme_recomendado['Meta_score']}")
print(f"Diretor: {filme_recomendado['Director']}")
print(f"Atores: {filme_recomendado['Star1']}, {filme_recomendado['Star2']}, {filme_recomendado['Star3']}, {filme_recomendado['Star4']}")
print(f"Número de votos: {filme_recomendado['No_of_Votes']}")
print(f"Faturamento: {filme_recomendado['Gross']}")

print(dados.isnull().sum())

most_frequent_certificate = dados['Certificate'].mode()[0]
dados['Certificate'].fillna(most_frequent_certificate, inplace=True)


meta_score_mean = dados['Meta_score'].mean()
dados['Meta_score'].fillna(meta_score_mean, inplace=True)


dados['Gross'] = dados['Gross'].astype(str).str.replace(',', '').astype(float)


gross_mean = dados['Gross'].mean()
dados['Gross'].fillna(gross_mean, inplace=True)

print(dados.isnull().sum())

# Distribuição do faturamento
sns.histplot(dados['Gross'].dropna(), kde=True)
plt.title('Distribuição do Faturamento')
plt.xlabel('Faturamento')
plt.ylabel('Frequência')
plt.show()

dados.head()

genre_dummies = pd.get_dummies(dados['Genre'], prefix='Genre')


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
dados['Certificate_encoded'] = le.fit_transform(dados['Certificate'])


dados.drop(['Genre', 'Certificate'], axis=1, inplace=True)


dados = pd.concat([dados, genre_dummies], axis=1)


scaler = MinMaxScaler()
dados[['IMDB_Rating', 'Meta_score', 'No_of_Votes', 'Gross']] = scaler.fit_transform(dados[['IMDB_Rating', 'Meta_score', 'No_of_Votes', 'Gross']])


print(dados.head())

dados.head()

numeric_cols = ['IMDB_Rating', 'Meta_score', 'No_of_Votes', 'Gross']


scaler = MinMaxScaler()


dados[numeric_cols] = scaler.fit_transform(dados[numeric_cols])

print(dados.head())

dados.head()

dados_1 = []  # This should be a list of indices you want to exclude
indices = ~dados.index.isin(dados_1)  # Now dados_1 should contain indices
df_teste = dados[indices]
df_teste.head(15)

dados['IMDB_Rating_Category'] = pd.cut(dados['IMDB_Rating'], bins=[0, 3, 6, 9, 10], labels=['Low', 'Medium', 'High', 'Very High'])

x = dados.drop(columns={'IMDB_Rating', 'IMDB_Rating_Category'}) # Remove both original and categorized rating
#O drop se utiliza para remover colunas.
y = dados['IMDB_Rating_Category'] # Use the categorized rating as the target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

object_columns = x_train.select_dtypes(include='object').columns

for col in object_columns:
    # Example: Fill missing values and convert to numerical representation
    x_train[col] = x_train[col].fillna('Unknown')  # Replace missing values with 'Unknown'
    x_train[col] = x_train[col].astype('category').cat.codes  # Convert categories to numerical codes

    # Apply the same transformation to x_test
    x_test[col] = x_test[col].fillna('Unknown')
    x_test[col] = x_test[col].astype('category').cat.codes

x_train = x_train.apply(pd.to_numeric, errors='coerce')
x_test = x_test.apply(pd.to_numeric, errors='coerce')

min_max = MinMaxScaler()
min_max.fit(x_train)
x_train_norm = min_max.transform(x_train)
x_test_norm = min_max.transform(x_test)

df_teste['IMDB_Rating'].value_counts()

y_train = y_train.astype('category').cat.codes

random_under = RandomUnderSampler(random_state=42)
X_under, y_under = random_under.fit_resample(x_train_norm, y_train)
X_under.shape

y_under.value_counts()

imputer = SimpleImputer(strategy='mean')

X_under_imputed = imputer.fit_transform(X_under)

imputer = SimpleImputer(strategy='mean')
X_under_imputed = imputer.fit_transform(X_under)

x_test_norm_imputed = imputer.transform(x_test_norm)

modelo_knn2 = KNeighborsClassifier(n_neighbors=3)
modelo_knn2.fit(X_under_imputed, y_under)
y_pred = modelo_knn2.predict(x_test_norm_imputed) # Predict using imputed test data

y_pred_codes = y_pred  # No need for .codes as y_pred is already numerical
y_test_codes = y_test.cat.codes

print('Acuracia:', accuracy_score(y_test_codes, y_pred_codes))
print('Revocação', recall_score(y_test_codes, y_pred_codes, average='weighted'))
print('precisão:', precision_score(y_test_codes, y_pred_codes,average='weighted'))

cm = confusion_matrix(y_test_codes, y_pred_codes)
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Previsões')
plt.ylabel('Valores Reais')
plt.title('Matriz de Confusão')
plt.show()

from sklearn.metrics import classification_report

print(classification_report(y_test_codes, y_pred_codes))

from sklearn.metrics import roc_curve, auc


y_pred_proba = modelo_knn2.predict_proba(x_test_norm_imputed)


y_test_codes_adjusted = [1 if code == 0 else 0 for code in y_test_codes]

fpr, tpr, thresholds = roc_curve(y_test_codes_adjusted, y_pred_proba[:, 1])
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

from sklearn.metrics import precision_recall_curve


y_pred_proba = modelo_knn2.predict_proba(x_test_norm_imputed)


y_test_codes_adjusted = [1 if code == 0 else 0 for code in y_test_codes]

precision, recall, thresholds = precision_recall_curve(y_test_codes_adjusted, y_pred_proba[:, 1])

plt.plot(recall, precision, label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.show()


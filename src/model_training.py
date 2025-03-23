from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
from sklearn.multioutput import MultiOutputRegressor, MultiOutputClassifier
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score, accuracy_score

def entrenar_modelo_clasificacion(x_train, y_train):
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'n_estimators': [100, 250, 500],
        'min_samples_leaf': [5, 15, 25],
        'max_features': [3, 5, 7, 9]
    }
    etc = ExtraTreesClassifier(random_state=21)
    model = GridSearchCV(etc, param_grid, cv=3, n_jobs=-1)
    model.fit(x_train, y_train)
    print("\nthe best ", model.best_estimator_, " the best scors ", model.best_score_)
    return model

def entrenar_modelo_regresion(x_train, y_train):
    regresor = ExtraTreesRegressor(n_estimators=150, random_state=42)
    model = MultiOutputRegressor(regresor)
    model.fit(x_train, y_train)
    return model

def realizar_predicciones(model, datos):
    predicciones = model.predict(datos)
    return predicciones

def evaluar_modelo(model, x_test, y_test, tipo='clasificacion'):
    if tipo == 'clasificacion':
        y_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Precisión: {accuracy:.3f}')
    elif tipo == 'regresion':
        y_pred = model.predict(x_test)
        mse = root_mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f'RMSE: {mse:.3f}, MAE: {mae:.3f}, R²: {r2:.3f}')
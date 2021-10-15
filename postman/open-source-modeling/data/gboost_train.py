target = df_data_card.columns[0]
class_inputs = list(df_data_card.select_dtypes(include=['object']).columns)

# impute data
df_data_card = df_data_card.fillna(df_data_card.median())
df_data_card['JOB'] = df_data_card.JOB.fillna('Other')

# dummy the categorical variables
df_data_card_ABT = pd.concat([df_data_card, pd.get_dummies(df_data_card[class_inputs])], axis = 1).drop(class_inputs, axis = 1)
df_all_inputs = df_data_card_ABT.drop(target, axis=1)

X_train, X_valid, y_train, y_valid = train_test_split(
    df_all_inputs, df_data_card_ABT[target], test_size=0.33, random_state=54321)

gb = GradientBoostingClassifier(random_state=54321)
gb.fit(X_train, y_train)

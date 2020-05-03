import pickle
import re
import sys
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def load_data(db_fpath: str, table_name: str):
    """Load a table from the database into a pandas DataFrame

    Args:
        db_fpath: str. The path to sqlite database.
        table_name str. The name of the table.
    Returns: 
        X: pd.DataFrame, Y: pd.DataFrame, category_names list(str)
    """
    engine = create_engine(f'sqlite:///{db_fpath}')
    df = pd.read_sql_table(table_name, engine)
    X = df['message']
    Y = df.iloc[:, 4:]
    category_names = Y.columns.tolist().best_estimator_.steps[1][1].coef_
    return X, Y, category_names


def tokenizer(text: str):
    """Normalize, tokenize and lemmatize text.

    Args:
        text: str. A body of text.

    Returns:
        tokens: list(str). A list of normalised and lemmatized words.
    """
    # Replace url with 'website'.
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    found_urls = re.findall(url_regex, text)
    for url in found_urls:
        text = text.replace(url, "website")

    # Convert to lower case and remove punctuation
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())

    # Lemmatize and remove stop words.
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')

    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return tokens


def build_model():
    """Build the machine learning pipeline with cross validation
    and gridsearch

    Args:
        None

    Returns:
        GridSearchCV(...)
    """
    lr_pipeline = Pipeline([
        ('vect', TfidfVectorizer(tokenizer=tokenizer)),
        ('clf', MultiOutputClassifier(LogisticRegression()))
    ])

    parameters = {
        'clf__estimator__penalty': ['l2', None],
        'clf__estimator__C': [0.1, 1, 10]
    }

    return GridSearchCV(lr_pipeline, param_grid=parameters)


def generate_classification_report(y_test: pd.DataFrame, y_pred: pd.DataFrame):
    """Create a classification report for each column including:
    accuracy, precision, recall and f1 score. 

    Args:
        y_test: pandas.DataFrame The test dataset, values of (0,1) for each class.
        y_pred: pandas.DataFrame Predictions, values of (0,1) for each class.
    Returns:
        df: pandas.DataFrame. A dataframe of metrics for each label.
    """    
    metrics = []

    for col in y_test.columns:
        accuracy = accuracy_score(y_test[col], y_pred[col])
        precision = precision_score(y_test[col], y_pred[col], average='macro')
        recall = recall_score(y_test[col], y_pred[col], average='macro')
        f1 = f1_score(y_test[col], y_pred[col], average='macro')

        metrics.append([accuracy, precision, recall, f1])

    return pd.DataFrame(
        data=metrics,
        index=y_test.columns,
        columns=['accuracy', 'precision', 'recall', 'f1']
        ).round(2)


def evaluate_model(model, X_test: pd.DataFrame, Y_test: pd.DataFrame, category_names: list):
    """Evaluate a model accuracy, precision, recail and f1 score.

    Args:
        model: Fitted model (must be able to call 'predict' method).
        X_test: pd.DataFrame. Dataframe of messages.
        Y_test: pd.DataFrame. Dataframe of labels. 
    Returns:
        None
    """
    y_pred = model.predict(X_test)
    y_pred = pd.DataFrame(y_pred, columns=Y_test.columns)
    generate_classification_report(Y_test, y_pred)


def save_model(model, model_filepath):
    """Save the model as a pickle file.

    Args:
        model: Fitted model (must be able to call 'predict' method).
        model_fpath: str. Path to save the file to.
    Returns:
        None
    """
    with open(model_filepath, 'wb') as fh:
        pickle.dump(model, fh)


def main():
    if len(sys.argv) == 4:
        db_fpath, model_filepath, table_name = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(db_fpath))
        print('Loading data...\n    DATABASE: {}'.format(table_name))
        X, Y, category_names = load_data(db_fpath, table_name)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
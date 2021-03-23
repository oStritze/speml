
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score
#from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
#from sklearn.metrics import average_precision_score

def classify(X_train, y_train, X_test, y_test):   
    names = ["SVC", "RandomForest", "GaussianNB"]

    classifiers = [
        SVC(gamma=2, C=1),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        GaussianNB()]

    results = pd.DataFrame(columns=names, index=["f1", "roc_auc"])

    for i in enumerate(classifiers):
        cname = names[i[0]]
        c = i[1]

        print("Fitting {} now...".format(cname))
        s = time.time()
        c.fit(X_train, y_train)
        print("--- Done! Took {:1.4f}s".format(time.time()-s))
        y_pred = c.predict(X_test)
    
        results[cname]["f1"] = f1_score(y_test, y_pred, average='micro')
        results[cname]["roc_auc"] = roc_auc_score(y_test, y_pred)
    
    return results

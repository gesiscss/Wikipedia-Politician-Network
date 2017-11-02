
# coding: utf-8


import pandas as pd
import sys

def clean(x):
    """ Returns a dictionary with gender related information only 
    """
    try:
        return x["face"][0]["attribute"]["gender"]
    except:
        return {}


def get_gender(x):
    """ extracts gender from passed dictionary 
    """
    if x == {}:
        return "Unknown"
    else:
        return str(x['value'])


def asign_score(dic, thres):
    """ Returns gender score for every passed dictionary (representing one image)
        with a certain confidence specified by the thres argument
    """
    if dic == {}:
        return 0
    elif dic['confidence'] < thres:
        return 0
    elif dic["value"] == "Male":
        return 1
    elif dic['value'] == "Female":
        return -1


def name_gender_lsit(df, names):
    """ Returns a DataFrame with two columns: NAME and GENDER
        gender is assigned based on total gender score, female if < 0, unknown if 0 and male if > 0
    """
    lst = []
    for name in names:
        sub_list = []
        x = df[df["name"] == name]
        dic = dict(x.gender.value_counts())
        sub_list.append(name)
        gend_score = x["gend_score"].sum()
        if gend_score == 0:
            sub_list.append("Unknown")
        elif gend_score < 0:
            sub_list.append("Female")
        elif gend_score > 0:
            sub_list.append("Male")
        lst.append(sub_list)
    rdf = pd.DataFrame(lst)
    rdf.columns = ['name', 'gender']
    return rdf


def stats(d, total):
    """ Returns relative frequency of each gender
    """
    for key, value in d.items():
        d[key] = value / total
    return d


def gender_df(path, path_save, thres=70, encoding='utf-8'):
    """ Returns df with assigned gender with specified confidence, and also saves df
        in a csv file.
    """
    df = pd.read_json(path, lines=True)
    df.columns = ["name", "props"]
    df["props"] = df["props"].apply(clean)
    df["gender"] = df["props"].apply(lambda x: get_gender(x))
    df["gend_score"] = df.props.apply(lambda x: asign_score(x, thres))
    names = df.name.unique()
    print("Total names:", len(names))
    print("Saving: " + path_save)
    df = name_gender_lsit(df, names)
    df.to_csv(path_save, index=False, encoding=encoding)
    dic = df.gender.value_counts().to_dict()
    print(dic)
    print(stats(dic, len(names)))
    return df


if __name__ == "__main__":

    path_read = sys.argv[1]
    path_write = sys.argv[2]

    df = gender_df(path_read,path_write,70)

    # health = gender_df("google_img/health.json","google_img/health.csv")

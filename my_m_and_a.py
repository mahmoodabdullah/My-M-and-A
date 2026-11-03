import pandas as pd
from io import StringIO
from my_ds_babel import csv_to_sql


def inspect_csv_1(csv_1):
    df = pd.read_csv(csv_1)

    df = df.rename(columns={
        'Gender': 'Gender',
        'FirstName': 'FirstName',
        'LastName': 'LastName',
        'Email': 'Email',
        'Age': 'Age',
        'City': 'City',
        'Country': 'Country'
    })

    df = df.drop(columns='UserName')

    df['FirstName'] = df['FirstName'].str.title().str.replace(
        r'[\"\\]', '', regex=True
    ).str.strip(" '")

    df['LastName'] = df['LastName'].str.title().str.replace(
        r'[\"\\]', '', regex=True
    ).str.strip(" '")

    df['Email'] = df['Email'].str.lower().str.strip(" '")

    df['City'] = df['City'].str.title().str.replace(
        r'[_-]', ' ', regex=True
    ).str.strip(" '")

    df['Country'] = df['Country'].str.upper().replace({
        'US': 'USA',
        'UNITED STATE OF AMERICA': 'USA',
        'U.S.A.': 'USA',
        '12': 'USA'
    }).fillna('USA')

    df['Gender'] = df['Gender'].replace({
        'M': 'Male',
        'F': 'Female',
        '0': 'Male',
        '1': 'Female'
    })

    df['Email'] = df['Email'].replace(
        "forgottoask@woodinc", pd.NA
    )


    df['Age'] = df['Age'].astype(str)

    return df


def inspect_csv_2(csv_2):
    col_names = ['Age', 'City', 'Gender', 'Name', 'Email']

    
    df = pd.read_csv(csv_2, sep=";", names=col_names)

    df[['FirstName', 'LastName']] = df['Name'].str.split(
        ' ', n=1, expand=True
    )

    df = df.drop(columns='Name')

    df['FirstName'] = df['FirstName'].str.title().str.replace(
        r'[\"\\]', '', regex=True
    ).str.strip(" '")

    df['LastName'] = df['LastName'].str.title().str.replace(
        r'[\"\\]', '', regex=True
    ).str.strip(" '")

    df['Email'] = df['Email'].str.lower().str.strip(" '")

    df['City'] = df['City'].str.title().str.replace(
        r'[_-]', ' ', regex=True
    ).str.strip(" '")

    df['Country'] = 'USA'

    df['Gender'] = df['Gender'].replace({
        'M': 'Male',
        'F': 'Female',
        '0': 'Male',
        '1': 'Female'
    })

    df['Age'] = df['Age'].str.replace(
        r"\s*(?:years|year|yo)\b", "", regex=True
    )

    
    df['Age'] = df['Age'].astype(str)

    col_order = [
        'Gender', 'FirstName', 'LastName',
        'Email', 'Age', 'City', 'Country'
    ]

    df = df[col_order]

    return df


def inspect_csv_3(csv_3):
    col_names = [
        'Gender', 'Name', 'Email',
        'Age', 'City', 'Country'
    ]

    
    df = pd.read_csv(
        csv_3,
        sep='\t',
        skiprows=1,
        names=col_names
    )

    df['Name'] = df['Name'].str.replace(
        '^string_', '', regex=True
    )

    df[['FirstName', 'LastName']] = df['Name'].str.split(
        ' ', n=1, expand=True
    )

    df['Gender'] = df['Gender'].str.replace(
        '^string_', '', regex=True
    )

    df['Email'] = df['Email'].str.replace(
        '^string_', '', regex=True
    )

    df['City'] = df['City'].str.replace(
        '^string_', '', regex=True
    )

    df['Country'] = df['Country'].str.replace(
        '^string_', '', regex=True
    )

    df['Age'] = df['Age'].str.replace(
        '^integer_', '', regex=True
    )

    df = df.drop(columns='Name')

    df['FirstName'] = df['FirstName'].str.title().str.replace(
        r'[\"\\]', '', regex=True
    ).str.strip(" '")

    df['LastName'] = df['LastName'].str.title().str.replace(
        r'[\"\\]', '', regex=True
    ).str.strip(" '")

    df['Email'] = df['Email'].str.lower().str.strip(" '")

    df['City'] = df['City'].str.title().str.replace(
        r'[_-]', ' ', regex=True
    ).str.strip(" '")

    df['Country'] = df['Country'].str.upper().replace({
        'US': 'USA',
        'U.S.A.': 'USA',
        'U.S.': 'USA',
        'UNITED STATE OF AMERICA': 'USA',
        'UNITED-STATE-OF-AMERICA': 'USA',
        'UNITED_STATE_OF_AMERICA': 'USA',
        '1': 'USA'
    })

    df['Gender'] = df['Gender'].str.replace(
        '^character_', '', regex=True
    )

    df['Gender'] = df['Gender'].replace({
        'M': 'Male',
        'boolean_0': 'Female',
        'boolean_1': 'Male'
    })

    df['Age'] = df['Age'].str.replace(
        r"\s*(?:years|year|yo)\b", "", regex=True
    )

    
    df['Age'] = df['Age'].astype(str)

    col_order = [
        'Gender', 'FirstName', 'LastName',
        'Email', 'Age', 'City', 'Country'
    ]

    df = df[col_order]

    return df


def my_m_and_a(content_database_1, content_database_2, content_database_3):

    first_csv = inspect_csv_1(content_database_1)
    second_csv = inspect_csv_2(content_database_2)
    third_csv = inspect_csv_3(content_database_3)

    combined_df = pd.concat(
        [first_csv, second_csv, third_csv],
        ignore_index=True
    )

    
    combined_df['FirstName'] = combined_df['FirstName'].fillna('').astype(str)
    combined_df['LastName'] = combined_df['LastName'].fillna('').astype(str)

    
    combined_df['FirstName'] = combined_df['FirstName'].str.replace(
        'string_', '', regex=False
    )
    combined_df['LastName'] = combined_df['LastName'].str.replace(
        'string_', '', regex=False
    )

    combined_df['created_at'] = pd.NA
    combined_df['referral'] = pd.NA

    return combined_df


def main():
    with open('only_wood_customer_us_1.csv') as file:
        csv_1 = file.read()

    with open('only_wood_customer_us_2.csv') as file:
        csv_2 = file.read()

    with open('only_wood_customer_us_3.csv') as file:
        csv_3 = file.read()

    combined_df = my_m_and_a(
        StringIO(csv_1),
        StringIO(csv_2),
        StringIO(csv_3)
    )

    print(type(combined_df))
    print(combined_df.shape)
    print(combined_df.columns.tolist())

    merged_csv = combined_df.to_csv(index=False)

    csv_to_sql(
        StringIO(merged_csv),
        'plastic_free_boutique.sql',
        'customers'
    )


if __name__ == '__main__':
    main()

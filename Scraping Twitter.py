import twint
import pandas as pd
from collections import Counter

# List of users to scrape
users = [
    'shakira',
    'KimKardashian',
    'rihanna',
    'jtimberlake',
    'KingJames',
    'neymarjr',
]

# Function to get a list of followings for a given user
def get_followings(username):
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    c.Hide_output = True  # Suppress output from twint
    try:
        twint.run.Following(c)  # Get followings
        list_of_followings = twint.storage.panda.Follow_df
        return list_of_followings['following'].tolist()  # Return a list of following
    except KeyError as e:
        print(f"KeyError for user {username}: {e}")
        return []
    except Exception as e:
        print(f"An error occurred with user {username}: {e}")
        return []

# Scrape followings for each user
followings = {}
following_list = []
for person in users:
    print(f"#####\nStarting: {person}\n#####")
    try:
        followings[person] = get_followings(person)
        following_list += followings[person]
    except Exception as e:
        print(f"An error occurred while processing {person}: {e}")

# Get the 10 most common followed accounts
most_common_followings = Counter(following_list).most_common(10)
print("Most common followings:", most_common_followings)

# Analyze follow relationships among our group
follow_relations = {}
for following_user in followings:
    follow_relation_list = []
    for followed_user in followings:
        if followed_user in followings[following_user]:
            follow_relation_list.append(True)
        else:
            follow_relation_list.append(False)
    follow_relations[following_user] = follow_relation_list

# Create a pandas DataFrame to represent the following relationships
following_df = pd.DataFrame.from_dict(
    follow_relations,
    orient='index',
    columns=followings.keys()
)

print("Following relationships:\n", following_df)

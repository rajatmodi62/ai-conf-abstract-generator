import requests

# Function to fetch all papers for a given task ID
def fetch_all_papers(task_id):
    papers = []
    page = 1
    ct = 0
    while True:
        # Construct endpoint for fetching papers
        endpoint_papers = f"https://paperswithcode.com/api/v1/tasks/{task_id}/papers/?page={page}"

        # Make request to API
        response = requests.get(endpoint_papers)
        papers_data = response.json()

        # Add papers from current page to the list
        papers.extend(papers_data['results'])

        # Check if there are more pages to fetch
        if papers_data['next'] is not None:
            page += 1
        else:
            break
        ct+=1
        print(ct)
        # print("dump the file")
        # break
    return papers

# Step 1: Find the task ID for Representation Learning
task_id = "representation-learning"  # This is from the URL you provided

# Step 2: Fetch all papers associated with the task
all_papers = fetch_all_papers(task_id)

# Output file name
output_file = "representation_learning_papers.txt"

# Write titles to a text file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Total Papers related to 'Representation Learning': {len(all_papers)}\n")
    for paper in all_papers:
        f.write(f"{paper['title']}\n")

print(f"Titles of papers have been saved to {output_file}.")







# import requests

# # Step 1: Find the task ID for Representation Learning
# task_id = "representation-learning"  # This is from the URL you provided

# # Step 2: Retrieve papers associated with the task
# endpoint_papers = f"https://paperswithcode.com/api/v1/tasks/{task_id}/papers/"

# response_papers = requests.get(endpoint_papers)
# papers_data = response_papers.json()

# # Print the names of papers associated with the task
# print(f"Papers related to 'Representation Learning':")
# count = 0
# for paper in papers_data['results']:
#     print(paper['title'])
#     count+=1
# print(count)
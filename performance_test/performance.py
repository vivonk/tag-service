import requests
import time
import re

# Base URLs
BASE_URL = "http://ab375f2b3c43e44099cd13254ae94934-30142821.ap-south-1.elb.amazonaws.com"
STACK_EXCHANGE_API_URL = "https://api.stackexchange.com/2.3/questions"

# Endpoints
POST_TAG_ENDPOINT = f"{BASE_URL}/post/tag"
GET_POST_ENDPOINT = f"{BASE_URL}/post/{{}}"

# Function to fetch questions from Stack Exchange API
def fetch_stackoverflow_questions(pagesize):
  params = {
    "pagesize": pagesize,
    "order": "desc",
    "sort": "activity",
    "site": "stackoverflow",
    "filter": "withbody"
  }
  response = requests.get(STACK_EXCHANGE_API_URL, params=params, timeout=30)
  return response.json()

# Function to post content
def post_content(post_id, content):
  response = requests.post(POST_TAG_ENDPOINT, json={"post_id": post_id, "content": content}, timeout=30)
  return response

# Function to get post
def get_post(post_id):
  response = requests.get(GET_POST_ENDPOINT.format(post_id), timeout=30)
  return response

def remove_unicode_and_special_characters(content):
  # Remove Unicode characters
  content = content.encode('ascii', 'ignore').decode()
  # Remove special characters except space
  content = re.sub(r'[^a-zA-Z0-9\s]', ' ', content)
  # Replace multiple spaces with a single space
  content = re.sub(r'\s+', ' ', content)

  return content
# Function to measure time for requests
def measure_time_for_requests(num_requests, questions):
  times = []
  start_index = num_requests-1000

  # check num_requests is greater than start_index
  if num_requests < start_index:
    print("num_requests should be greater than or equal to %d" % start_index)
    return

  for i in range(start_index, num_requests + 1):
    start_time = time.time()

    # Fetch a question for this request
    question = questions[i % len(questions)]
    post_id = f"{i}"  # Incremental counter for post_id
    content = remove_unicode_and_special_characters(question["body"])

    # Post the content
    post_response = post_content(post_id, content)
    if post_response.status_code != 201:
      print(f"POST request failed for request {i}: {post_response.status_code}")
      continue

    # Poll the GET endpoint to check if tags are generated
    retry_count = 0
    max_retries = 60  # Max retries to wait for 60 seconds
    while retry_count < max_retries:
      get_response = get_post(post_id)
      if get_response.status_code == 200 and 'tags' in get_response.json():
        print(f"Tags generated for request {i}")
        break
      time.sleep(1)  # Sleep for 1 second before retrying
      retry_count += 1

    if retry_count == max_retries:
      print(f"Request {i} timed out waiting for tags to be generated")

    end_time = time.time()
    time_taken = end_time - start_time
    times.append(time_taken)

    # Print the time taken for the first, 100th, and 1000th requests
    if i in [start_index + 1, start_index + 100, start_index + 1000]:
      print(f"Time taken for request {i}: {time_taken} seconds")

  return times



def main():
  all_questions = []

  # Fetch questions for page sizes from 1 to 1000
  for pagesize in range(11, 12):
    questions_data = fetch_stackoverflow_questions(pagesize)
    questions = questions_data["items"]
    all_questions.extend(questions)
    time.sleep(1)  # To avoid hitting the rate limit

  # Measure time for the first, 100th, and 1000th requests
  measure_time_for_requests(14000, all_questions)

if __name__ == "__main__":
  main()

summarize_prompt = """
You are an AI capable of analyzing files provided as attachments. Given a file attachment and a unique Content Identifier (CID), analyze the file's content. If the file is an image, analyze its visual content. Generate a concise summary of the file's content in 200 words or less. Return the response in JSON format with two keys: "summary" containing the summary, and "cid" containing the provided CID.

**Input:**
- File: Provided as an attachment
- CID: {provided_cid}

**Task:**
1. Read and analyze the content of the provided file attachment.
2. If the file is an image, describe its key visual elements, context, and any notable details.
3. Summarize the content in 200 words or less.
4. Return the result as a JSON object.

**Output Format:**
```json
{"summary": "<200-word summary of the file content>","cid": "{provided_cid}"}
"""


retrieve_prompt = """You are provided with a JSON text containing an array of objects under the key "data". Each object has a "summary" field describing a program's content and a "cid" field with a unique identifier. Your task is to analyze the summaries and identify the top five CIDs whose summaries best match the user's query in terms of relevance, content, and context.

**Input:**
- The JSON file with the structure: 
  ```json
  {

    "<unique CID>": "<summary of file>?
  }
  ```
- The user's query: "{USER_QUERY}"

**Instructions:**
1. Read and parse the JSON file to extract the "summary" and "cid" fields from each object in the "data" array.
2. Evaluate the relevance of each summary to the user's query by analyzing the content, keywords, and context. Consider the programming language, functionality, and purpose described in the summary.
3. Rank the summaries based on how closely they match the user's query.
4. Select the top five CIDs corresponding to the most relevant summaries.
5. If fewer than five entries exist, return all available CIDs in order of relevance.
6. If no summaries match the query, return an empty list.

**Output Format:**
Return a JSON array containing up to five CIDs in order of relevance (most relevant first):
```json
["cid1", "cid2", "cid3", "cid4", "cid5"]
```

**Example:**
- JSON file:
  ```json
  {
  "cid_python_1":"A simple Python program that prints 'Hello World!' to the console.",
  "cid_c_1": "A C program that prints 'Hello World' using printf."
  }
  ```
- User query: "Python hello world program"
- Output: `["cid_python_1"]`

**User Query:** "{USER_QUERY}"

Now, process the JSON file and return the top five matching CIDs as a JSON array."""
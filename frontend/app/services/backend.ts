import axios from 'axios';
import useSWR from 'swr';

const isBrowser = typeof window !== 'undefined';
const BACKEND_URL = isBrowser ? `${window.location.protocol}//${window.location.hostname}:8000` : 'http://localhost:8000';
const GET_WORKFLOW_URL = `${BACKEND_URL}/workflow`;
const POST_MESSAGE_URL = `${BACKEND_URL}/next`;

export async function getWorkflow() {
  const response = await axios.get(GET_WORKFLOW_URL);
  return response.data;
}

export function getWorkflowSWR() {
  return useSWR(GET_WORKFLOW_URL, getWorkflow);
}

export async function sendMessage(input: string): Promise<ReadableStreamDefaultReader<Uint8Array>> {
  return fetch(POST_MESSAGE_URL, {
    method: 'POST', // specify the HTTP method
    headers: {
      'Content-Type': 'application/json' // set the content type to JSON
    },
    body: JSON.stringify({ text: input }) // attach the JSON payload
  })
  .then(async (response: Response) => {
    // Check if the fetch was successful
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    if (!response.body) {
      throw new Error('Response body is undefined');
    }
    
    // Get a ReadableStream from the fetch response
    return response.body.getReader();
  })
  .catch((error: Error) => {
    // Handle any errors
    console.error('Fetch Error:', error);
    throw new Error('Fetch Error')
  });
}

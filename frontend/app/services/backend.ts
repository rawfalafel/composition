import ky from 'ky';
import useSWR from 'swr';

const BACKEND_URL = `${window.location.protocol}//${window.location.hostname}:8000`;
const GET_WORKFLOW_URL = `${BACKEND_URL}/workflow`;
const POST_MESSAGE_URL = `${BACKEND_URL}/next`;

export async function getWorkflow() {
  const rest = await ky.get(GET_WORKFLOW_URL);
  const data = await rest.json();
  return data;
}

export function getWorkflowSWR() {
  return useSWR(GET_WORKFLOW_URL, getWorkflow);
}

export async function sendMessage(input: string) {
  await ky.post(POST_MESSAGE_URL, { json: { text: input }});
}

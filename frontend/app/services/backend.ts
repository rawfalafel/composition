import ky from 'ky';
import useSWR from 'swr';

const DOMAIN = "http://localhost:8000";
const GET_WORKFLOW_URL = `${DOMAIN}/workflow`;
const POST_MESSAGE_URL = `${DOMAIN}/next`;

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
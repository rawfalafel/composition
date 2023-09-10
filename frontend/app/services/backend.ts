import useSWR from 'swr';

const ENDPOINT = "http://localhost:8000/workflow"

export async function getWorkflow() {
  const rest = await fetch(ENDPOINT);
  const data = await rest.json();
  return data;
}

export function getWorkflowSWR() {
  return useSWR(ENDPOINT, getWorkflow);
}
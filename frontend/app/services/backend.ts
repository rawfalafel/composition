export async function getWorkflow() {
    const rest = await fetch("/workflow");
    const data = await rest.json();
    return data;
}
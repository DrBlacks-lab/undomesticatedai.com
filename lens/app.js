import {checkRegistry, compileCapsule, responseTemplate, validateEnvelope} from './core.js';
const $ = id => document.getElementById(id);
let registry = null;
let compiled = null;
let busy = false;
let importedRegistry = false;
function invalidate() {
  compiled = null;
  $('capsule').value = '';
  $('template').value = '';
  $('download').disabled = true;
  $('validate').disabled = true;
  $('result').textContent = 'No current review result.';
}
function showBinding() {
  const errors = checkRegistry(registry);
  $('binding').textContent = errors.length ? `HOLD — ${errors.join('; ')}` : 'Bound for local preparation. Source custody and authenticity require external review.';
  $('compile').disabled = busy || errors.length > 0;
}
async function readFile(id) {
  const file = $(id).files[0];
  if (!file || file.size > 1024 * 1024) throw new Error(`${id}: select a file under 1 MiB`);
  return new Uint8Array(await file.arrayBuffer());
}
$('registryFile').addEventListener('change', async () => {
  importedRegistry = true;
  invalidate();
  try { registry = JSON.parse(new TextDecoder('utf-8', {fatal:true}).decode(await readFile('registryFile'))); }
  catch (error) { registry = null; $('binding').textContent = `HOLD — ${error.message}`; }
  showBinding();
});
for (const id of ['ceaFile', 'taxonomyFile', 'runId', 'mode', 'workerId', 'evaluatorId', 'steps', 'subject']) {
  $(id).addEventListener('input', invalidate);
  $(id).addEventListener('change', invalidate);
}
$('response').addEventListener('input', () => { $('result').textContent = 'Response changed — check again.'; });
$('compile').addEventListener('click', async () => {
  if (busy) return;
  invalidate(); busy = true; showBinding();
  // Disable inputs during async digest checks so results cannot bind stale form state.
  const controls = [...document.querySelectorAll('#inputs input, #inputs textarea, #inputs select')];
  controls.forEach(x => { x.disabled = true; });
  try {
    const request = {run_id: $('runId').value, mode: $('mode').value, worker_id: $('workerId').value, evaluator_id: $('evaluatorId').value, max_steps: Number($('steps').value), subject: $('subject').value};
    const cea = await readFile('ceaFile');
    const taxonomy = await readFile('taxonomyFile');
    compiled = await compileCapsule(registry, cea, taxonomy, request);
    $('capsule').value = compiled.capsule_json;
    $('template').value = JSON.stringify(responseTemplate(compiled), null, 2);
    $('binding').textContent = `Compiled locally. Capsule SHA-256: ${compiled.capsule_sha256}. Review required; no execution authorization.`;
    $('download').disabled = false; $('validate').disabled = false;
  } catch (error) { $('binding').textContent = `HOLD — ${error.message}`; }
  finally { busy = false; controls.forEach(x => { x.disabled = false; }); $('compile').disabled = checkRegistry(registry).length > 0; }
});
$('download').addEventListener('click', () => {
  if (!compiled) return;
  const url = URL.createObjectURL(new Blob([compiled.capsule_json], {type:'application/json;charset=utf-8'}));
  const link = document.createElement('a'); link.href = url; link.download = `${compiled.capsule.run_id}-capsule.json`; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
$('validate').addEventListener('click', async () => {
  const expected = compiled;
  try {
    if (!expected) throw new Error('Compile a current capsule first');
    const input = $('response').value;
    if (new TextEncoder().encode(input).length > 1024 * 1024) throw new Error('Response exceeds 1 MiB');
    const envelope = JSON.parse(input);
    const result = await validateEnvelope(envelope, expected, registry);
    if (compiled !== expected || $('response').value !== input) throw new Error('Inputs changed; compile and check again');
    $('result').textContent = JSON.stringify(result, null, 2);
  } catch (error) { $('result').textContent = `INVALID — ${error.message}`; }
});
try {
  const response = await fetch('../protocol/manifest-v1.json', {cache:'no-store', credentials:'omit'});
  if (!response.ok) throw new Error('Registry unavailable');
  const initialRegistry = await response.json();
  if (!importedRegistry) { registry = initialRegistry; showBinding(); }
} catch (error) { if (!importedRegistry) $('binding').textContent = `HOLD — ${error.message}`; }

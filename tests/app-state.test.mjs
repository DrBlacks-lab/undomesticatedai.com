import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {sha256, responseTemplate} from '../lens/core.js';

// A minimal DOM adapter tests state transitions. This is not a real browser test.
class Control {
  constructor(value='') { this.value=value; this.disabled=false; this.textContent=''; this.files=[]; this.handlers=new Map(); }
  addEventListener(name,handler) { this.handlers.set(name,handler); }
  async event(name) { await this.handlers.get(name)?.(); }
}
const ids=['binding','capsule','template','download','validate','result','registryFile','ceaFile','taxonomyFile','runId','mode','workerId','evaluatorId','steps','subject','compile','response'];
const controls=Object.fromEntries(ids.map(k=>[k,new Control()]));
Object.assign(controls.runId,{value:'ui-test-1'});
controls.mode.value='ANALYZE'; controls.workerId.value='worker'; controls.evaluatorId.value='reviewer'; controls.steps.value='4'; controls.subject.value='Prepare an isolated comparison.';
const defaults=JSON.parse(await readFile(new URL('../protocol/manifest-v1.json',import.meta.url)));
globalThis.document={getElementById:id=>controls[id],querySelectorAll:()=>['registryFile','ceaFile','taxonomyFile','runId','mode','workerId','evaluatorId','steps','subject'].map(id=>controls[id])};
globalThis.fetch=async()=>({ok:true,json:async()=>structuredClone(defaults)});
await import('../lens/app.js');

test('default UI reaches binding HOLD with compilation disabled',()=>{
  assert.match(controls.binding.textContent,/HOLD.*SOURCE_BINDING_HOLD/);
  assert.equal(controls.compile.disabled,true);
});
test('local imports compile; reviewed response checks; edits invalidate stale artifacts',async()=>{
  const cea=new TextEncoder().encode('SYNTHETIC UI PROCEDURE ONLY');
  const taxonomy=new TextEncoder().encode('SYNTHETIC UI TAXONOMY ONLY');
  const r=structuredClone(defaults);
  r.revision='synthetic-ui-1';r.binding_status='BOUND';
  r.cea={version:'v5',sha256:await sha256(cea),source_ref:'SYNTHETIC_NOT_CANONICAL'};
  r.taxonomy={version:'test',namespace:'TEST_ONLY',sha256:await sha256(taxonomy),source_ref:'SYNTHETIC_NOT_CANONICAL'};
  r.valid_until=new Date(Date.now()+60000).toISOString();
  controls.registryFile.files=[new Blob([JSON.stringify(r)])];
  controls.ceaFile.files=[new Blob([cea])];controls.taxonomyFile.files=[new Blob([taxonomy])];
  await controls.registryFile.event('change');
  assert.equal(controls.compile.disabled,false);
  await controls.compile.event('click');
  assert.equal(controls.download.disabled,false);
  assert.equal(controls.validate.disabled,false);
  const compiled={capsule:JSON.parse(controls.capsule.value),capsule_json:controls.capsule.value,capsule_sha256:await sha256(controls.capsule.value)};
  const e=responseTemplate(compiled);e.analysis='Synthetic analysis';e.evidence.missing=['Live source custody is not established.'];
  controls.response.value=JSON.stringify(e);
  await controls.validate.event('click');
  assert.equal(JSON.parse(controls.result.textContent).status,'STRUCTURALLY_VALID_FOR_REVIEW');
  assert.equal(JSON.parse(controls.result.textContent).execution_authorized,false);
  controls.subject.value='Changed task';await controls.subject.event('input');
  assert.equal(controls.capsule.value,'');assert.equal(controls.template.value,'');
  assert.equal(controls.validate.disabled,true);assert.equal(controls.download.disabled,true);
  assert.equal(controls.result.textContent,'No current review result.');
});
test('bad replacement registry revokes prior readiness',async()=>{
  controls.registryFile.files=[new Blob(['not json'])];
  await controls.registryFile.event('change');
  assert.equal(controls.compile.disabled,true);
  assert.match(controls.binding.textContent,/HOLD/);
});

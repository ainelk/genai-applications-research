#!/usr/bin/env python3
"""Build an offline relationship graph with auditable, conservative counts."""
from pathlib import Path
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]

# Explicit aliases are matched case-insensitively at word boundaries.
# Longer overlapping terms win: 'prompt injection' is not also a 'prompt'.
TERMS = [
    ('llm', 'Large language model', ['large language model', 'large language models', 'LLM', 'LLMs'], []),
    ('prompt', 'Prompt', ['prompt', 'prompts'], ['a written brief']),
    ('token', 'Token', ['token', 'tokens'], []),
    ('context', 'Context window', ['context window', 'context windows'], ['exceed the available input budget']),
    ('rag', 'RAG', ['retrieval-augmented generation', 'RAG'], ['look up approved articles before composing an answer']),
    ('embedding', 'Embedding', ['embedding', 'embeddings'], ['turn a question into a numeric representation']),
    ('vector', 'Vector database', ['vector database', 'vector databases'], ['search a store of vectors for similar passages']),
    ('grounding', 'Grounding', ['grounding'], ['Each factual claim should be supported by a retrieved passage']),
    ('hallucination', 'Hallucination', ['hallucination', 'hallucinations'], ['An invented refund policy', 'invent a library method', 'introduce a fabricated claim', 'a convincing but incorrect explanation']),
    ('injection', 'Prompt injection', ['prompt injection', 'prompt injections'], ['Instructions hidden in a support ticket', 'malicious instructions inside a retrieved document']),
    ('finetune', 'Fine-tuning', ['fine-tuning', 'fine tuning'], ['Updating learned weights using curated examples']),
    ('inference', 'Inference', ['inference'], ['generating a response with the trained model']),
    ('latency', 'Latency', ['latency'], ['time spent searching, generating, validating, and waiting']),
    ('multimodal', 'Multimodal model', ['multimodal model', 'multimodal models'], ['combine a written brief with a reference image']),
    ('structured', 'Structured output', ['structured output', 'structured outputs'], ['Return a record with predefined fields and types']),
    ('tools', 'Tool calling', ['tool calling'], []),
    ('guardrails', 'Guardrails', ['guardrail', 'guardrails'], []),
    ('human', 'Human-in-the-loop', ['human-in-the-loop', 'human in the loop'], ['a staff member approves refunds', 'A developer inspects the diff and authorizes merging', 'An editor checks that names, numbers, and commitments match the source', 'a designer must inspect the final asset', 'A teacher reviews misleading explanations', 'Participants should confirm decisions and task owners', 'cases go to a person for review']),
    ('evaluation', 'Evaluation', ['evaluation', 'evaluations'], ['Test with representative questions and expert-reviewed expected answers', 'Compare outputs against a representative reference set and track regressions']),
    ('provenance', 'Data provenance', ['data provenance'], ['a record of source assets, permissions, generation settings, and edits', 'a link from each extracted value to its source page']),
]


def explicit_mentions(sentence):
    candidates = []
    for key, _, aliases, _ in TERMS:
        for alias in aliases:
            for match in re.finditer(r'(?<!\w)' + re.escape(alias) + r'(?!\w)', sentence, re.I):
                candidates.append((match.start(), match.end(), key, match.group()))
    selected = []
    for candidate in sorted(candidates, key=lambda c: (-(c[1] - c[0]), c[0], c[2])):
        if not any(candidate[0] < x[1] and candidate[1] > x[0] for x in selected):
            selected.append(candidate)
    return sorted(selected)


def analyse(report):
    body = report.split('<!-- ANALYSIS_START -->', 1)[1].split('<!-- ANALYSIS_END -->', 1)[0]
    sections = []
    for block in re.split(r'(?m)^## ', body)[1:]:
        title, _, remainder = block.partition('\n')
        key = 'crosscut' if title.startswith('Cross-cutting') else 'case' + title.split('.')[0]
        # Only the two analysis paragraphs; product lists/headings are excluded.
        prose = remainder.split('**Existing implementations**', 1)[0].strip()
        paragraphs = [re.sub(r'\*\*[^*]+\*\*\s*', '', p).strip() for p in re.split(r'\n\s*\n', prose) if p.strip()]
        sentences = []
        for pi, paragraph in enumerate(paragraphs, 1):
            for si, sentence in enumerate(re.split(r'(?<=[.!?])\s+(?=[A-Z])', paragraph), 1):
                sentences.append({'id': f'{key}-p{pi}-s{si}', 'text': sentence})
        sections.append({'id': key, 'title': title, 'sentences': sentences})
    evidence = []
    for section in sections:
        for sentence in section['sentences']:
            mentions = explicit_mentions(sentence['text'])
            explicit_keys = {m[2] for m in mentions}
            for start, end, key, matched in mentions:
                evidence.append({'term': key, 'section': section['id'], 'kind': 'explicit', 'sentence_id': sentence['id'], 'sentence': sentence['text'], 'matched': matched, 'start': start, 'end': end})
            for key, _, _, phrases in TERMS:
                # One implicit occurrence per term per sentence, and only if
                # that term has no explicit mention anywhere in the sentence.
                if key in explicit_keys:
                    continue
                found = next((p for p in phrases if p.casefold() in sentence['text'].casefold()), None)
                if found:
                    evidence.append({'term': key, 'section': section['id'], 'kind': 'implicit', 'sentence_id': sentence['id'], 'sentence': sentence['text'], 'matched': found})
    terms = []
    edges = []
    for key, label, aliases, phrases in TERMS:
        terms.append({'id': key, 'label': label, 'aliases': aliases, 'implicit_phrases': phrases,
                      'explicit': sum(e['term'] == key and e['kind'] == 'explicit' for e in evidence),
                      'implicit': sum(e['term'] == key and e['kind'] == 'implicit' for e in evidence)})
        for section in sections:
            counts = {kind: sum(e['term'] == key and e['section'] == section['id'] and e['kind'] == kind for e in evidence) for kind in ['explicit', 'implicit']}
            if sum(counts.values()):
                edges.append({'term': key, 'section': section['id'], **counts})
    return {'report_sha256': hashlib.sha256(report.encode()).hexdigest(),
            'method': {'scope': 'Only analysis paragraphs of the eight use cases and cross-cutting section between ANALYSIS markers; titles, product lists, introduction, and references excluded.',
                       'explicit': 'Case-insensitive whole-word alias occurrences. Longest overlapping match wins; each occurrence is counted once.',
                       'implicit': 'Conservative, analyst-selected descriptive phrases. One mention per term per sentence, only if the sentence has no explicit alias for that term. Phrase rules and full evidence are provided. This is an operational estimate, not an exhaustive semantic frequency.',
                       'edges': 'A term-to-section link means at least one explicit or implicit mention. Solid green = explicit; dashed orange = implicit. Width is fixed; counts are shown in nodes and evidence.',
                       'zero': 'Zero means no match under these rules, not proof that the concept is absent.'},
            'terms': terms, 'sections': [{'id': s['id'], 'title': s['title']} for s in sections], 'edges': edges, 'evidence': evidence}


def build_html(data):
    embedded = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return TEMPLATE.replace('__DATA__', embedded)


TEMPLATE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Generative AI vocabulary · Relationship graph</title>
<style>
:root{color-scheme:light;--ink:#16372b;--muted:#51655b;--bg:#f4f7f4;--paper:#fff;--line:#dae4dc;--explicit:#176346;--implicit:#a44b10}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:40px 24px 64px}h1{font-size:34px;line-height:1.2;margin:8px 0 16px}h2{font-size:23px;margin:0 0 12px}p{margin:8px 0 18px}.eyebrow{font-size:13px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}.muted{color:var(--muted)}.legend{display:flex;gap:24px;flex-wrap:wrap;margin:22px 0}.legend span{display:inline-flex;align-items:center;gap:8px}.sample{width:32px;border-top:3px solid var(--explicit)}.sample.implicit{border-top:3px dashed var(--implicit)}.panel{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:24px;margin:24px 0}.controls{display:flex;align-items:center;gap:16px;flex-wrap:wrap}select,button{font:inherit;color:var(--ink);border:1px solid #a8bbae;background:var(--paper);border-radius:8px;padding:8px 12px;max-width:100%}select:focus-visible,button:focus-visible{outline:3px solid var(--implicit);outline-offset:3px}.graph-scroll{overflow-x:auto;margin-top:20px}svg{width:100%;min-width:780px;display:block}.node{cursor:pointer}.node rect{fill:#f3f8f4;stroke:var(--line)}.node.active rect{fill:#dceee2;stroke:var(--explicit);stroke-width:2}.node text{font-size:15px;fill:var(--ink)}.node .counts{font-size:13px;fill:var(--muted)}.edge{fill:none;stroke-width:1.6}.edge.explicit{stroke:var(--explicit)}.edge.implicit{stroke:var(--implicit);stroke-dasharray:5 5}.faded{opacity:.08}.evidence{padding:14px 0;border-top:1px solid var(--line)}.kind{font-size:13px;font-weight:600}.kind.explicit{color:var(--explicit)}.kind.implicit{color:var(--implicit)}.evidence p{margin:6px 0}.sentence-id{font:12px ui-monospace,monospace;color:var(--muted)}table{width:100%;border-collapse:collapse}th,td{text-align:left;border-bottom:1px solid var(--line);padding:10px 12px;font-size:14px}th{background:#eff5ef}.num{font-variant-numeric:tabular-nums;text-align:right}.table-scroll{overflow-x:auto}details summary{cursor:pointer;font-weight:600}code{font-size:13px;overflow-wrap:anywhere}footer{color:var(--muted);font-size:13px}@media(max-width:600px){main{padding:24px 14px}h1{font-size:27px}.panel{padding:16px}}@media print{.controls{display:none}.graph-scroll{overflow:visible}svg{min-width:0}.panel{break-inside:avoid}body{background:white}}
</style></head><body><main>
<div class="eyebrow">EPAM Tech Orda · Course introduction · 02 Nov 2026</div>
<h1>How the vocabulary connects to real use cases</h1>
<p class="muted">Twenty terms linked to the eight use cases and cross-cutting analysis in the research report. Select a term to inspect its connections and the exact evidence behind its counts.</p>
<div class="legend"><span><i class="sample"></i>Explicit: direct term mentions (E)</span><span><i class="sample implicit"></i>Implicit: descriptive references (I)</span></div>
<section class="panel"><div class="controls"><label for="focus">Focus on a term</label><select id="focus"><option value="">All terms</option></select><button id="reset" type="button">Show all</button></div>
<p id="focus-summary" class="muted" aria-live="polite"></p>
<div class="graph-scroll"><svg id="graph" viewBox="0 0 1080 1060" role="img" aria-label="Term-to-use-case relationship graph; complete counts and evidence are provided below"></svg></div></section>
<section class="panel"><h2>Usage counts</h2><p class="muted">E counts literal occurrences; I counts annotated sentences. These are separate measures, not interchangeable units.</p><div class="table-scroll"><table><thead><tr><th>Vocabulary term</th><th class="num">Explicit (E)</th><th class="num">Implicit (I)</th><th class="num">Connected sections</th></tr></thead><tbody id="counts"></tbody></table></div></section>
<section class="panel"><h2 id="evidence-title">Evidence</h2><div id="evidence"></div></section>
<section class="panel"><details open><summary>Counting method and limitations</summary><div id="method"></div></details></section>
<footer>AI-assisted research and phrase annotation. Counts are reproducible with Python's standard library; no external scripts, fonts, or network requests are needed. HTML and JSON were generated from the same report.</footer>
</main><script type="application/json" id="data">__DATA__</script>
<script>
'use strict';
const data=JSON.parse(document.getElementById('data').textContent);
const svg=document.getElementById('graph'),focus=document.getElementById('focus');
const ns='http://www.w3.org/2000/svg';
function element(tag,attributes={},text){const n=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attributes))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;return n;}
function wrap(text,limit){const words=text.split(' '),lines=[''];for(const word of words){const i=lines.length-1;if((lines[i]+' '+word).trim().length>limit&&lines[i])lines.push(word);else lines[i]=(lines[i]+' '+word).trim();}return lines;}
for(const term of data.terms){const o=document.createElement('option');o.value=term.id;o.textContent=term.label;focus.append(o);const tr=document.createElement('tr');for(const [i,v]of [term.label,term.explicit,term.implicit,data.edges.filter(e=>e.term===term.id).length].entries()){const td=document.createElement('td');td.textContent=v;if(i)td.className='num';tr.append(td);}document.getElementById('counts').append(tr);}
const leftY=id=>58+data.terms.findIndex(t=>t.id===id)*50;
const rightY=id=>90+data.sections.findIndex(s=>s.id===id)*115;
function draw(){svg.replaceChildren();svg.append(element('title',{},'Vocabulary term usage by report section'));for(const edge of data.edges){for(const kind of ['explicit','implicit']){if(!edge[kind])continue;const shift=kind==='implicit'?4:-4;const y1=leftY(edge.term)+shift,y2=rightY(edge.section)+shift;svg.append(element('path',{d:`M 300 ${y1} C 500 ${y1}, 560 ${y2}, 760 ${y2}`,class:`edge ${kind} ${focus.value&&edge.term!==focus.value?'faded':''}`}));}}
for(const term of data.terms){const y=leftY(term.id),g=element('g',{class:`node ${focus.value===term.id?'active':''}`,'data-term':term.id});g.append(element('rect',{x:0,y:y-23,width:300,height:46,rx:8}));g.append(element('text',{x:14,y:y-3},term.label));g.append(element('text',{x:14,y:y+15,class:'counts'},`E ${term.explicit}   ·   I ${term.implicit}`));g.addEventListener('click',()=>{focus.value=term.id;update();});svg.append(g);}
for(const section of data.sections){const y=rightY(section.id),g=element('g');g.append(element('rect',{x:760,y:y-43,width:318,height:86,rx:9,fill:'#f3f8f4',stroke:'#dae4dc'}));const lines=wrap(section.title,35);for(let i=0;i<lines.length;i++)g.append(element('text',{x:776,y:y-20+i*19,'font-size':15,fill:'#16372b'},lines[i]));const edges=data.edges.filter(e=>e.section===section.id&&(!focus.value||e.term===focus.value));const totals=edges.reduce((a,e)=>({e:a.e+e.explicit,i:a.i+e.implicit}),{e:0,i:0});g.append(element('text',{x:776,y:y+28,'font-size':13,fill:'#51655b'},`E ${totals.e}   ·   I ${totals.i}`));svg.append(g);}}
function update(){draw();const term=data.terms.find(t=>t.id===focus.value),entries=data.evidence.filter(e=>!term||e.term===term.id);document.getElementById('focus-summary').textContent=term?`${term.label}: ${term.explicit} explicit occurrences, ${term.implicit} implicit sentence references.`:'All connections shown. E and I totals appear below each term and section.';document.getElementById('evidence-title').textContent=term?`Evidence · ${term.label}`:'Evidence · all terms';const box=document.getElementById('evidence');box.replaceChildren();for(const e of entries){const row=document.createElement('div');row.className='evidence';const badge=document.createElement('div');badge.className='kind '+e.kind;badge.textContent=`${e.kind.toUpperCase()} · ${data.terms.find(t=>t.id===e.term).label} · ${data.sections.find(s=>s.id===e.section).title}`;const p=document.createElement('p');p.textContent=e.sentence;const meta=document.createElement('div');meta.className='sentence-id';meta.textContent=`${e.sentence_id} · matched: “${e.matched}”`;row.append(badge,p,meta);box.append(row);}if(!entries.length)box.textContent='No matches under the documented counting rules.';}
focus.addEventListener('change',update);document.getElementById('reset').addEventListener('click',()=>{focus.value='';update();});
for(const [label,value]of Object.entries(data.method)){const p=document.createElement('p');const b=document.createElement('strong');b.textContent=label+': ';p.append(b,document.createTextNode(value));document.getElementById('method').append(p);}const hash=document.createElement('p');hash.textContent='Source report SHA-256: '+data.report_sha256;document.getElementById('method').append(hash);update();
</script></body></html>'''


def main():
    report = (ROOT / 'research_report.md').read_text(encoding='utf-8')
    data = analyse(report)
    (ROOT / 'graph_data.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (ROOT / 'vocabulary_graph.html').write_text(build_html(data), encoding='utf-8')
    print(json.dumps({'terms': len(data['terms']), 'sections': len(data['sections']), 'links': len(data['edges']),
                      'explicit': sum(t['explicit'] for t in data['terms']), 'implicit': sum(t['implicit'] for t in data['terms']),
                      'report_sha256': data['report_sha256']}))


if __name__ == '__main__':
    main()
